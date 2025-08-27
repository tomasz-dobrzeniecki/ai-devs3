#!/usr/bin/env python3
"""
S04E02 - Wykrywanie sfałszowanych wyników badań przy użyciu fine-tuningu
Multi-engine: openai, lmstudio, anything, gemini, claude
Wykorzystuje fine-tuning modelu do klasyfikacji danych z czujników robotów
"""
import argparse
import json
import logging
import os
import sys
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict

import requests
from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 1. Konfiguracja i wykrywanie silnika
load_dotenv(override=True)

parser = argparse.ArgumentParser(
    description="Wykrywanie sfałszowanych danych (multi-engine)"
)
parser.add_argument(
    "--engine",
    choices=["openai", "lmstudio", "anything", "gemini", "claude"],
    help="LLM backend to use",
)
parser.add_argument(
    "--skip-training",
    action="store_true",
    help="Pomiń trening i użyj istniejącego modelu",
)
parser.add_argument("--model-id", type=str, help="ID wytrenowanego modelu do użycia")
parser.add_argument("--job-id", type=str, help="ID istniejącego zadania fine-tuningu (pomiń tworzenie nowego)")
args = parser.parse_args()

ENGINE: Optional[str] = None
if args.engine:
    ENGINE = args.engine.lower()
elif os.getenv("LLM_ENGINE"):
    ENGINE = os.getenv("LLM_ENGINE").lower()
else:
    # Dla fine-tuningu najlepiej używać OpenAI
    ENGINE = "openai"

if ENGINE not in {"openai", "lmstudio", "anything", "gemini", "claude"}:
    print(f"❌ Nieobsługiwany silnik: {ENGINE}", file=sys.stderr)
    sys.exit(1)

# Dla fine-tuningu wymagany jest OpenAI
if not args.skip_training and ENGINE != "openai":
    print("⚠️  Fine-tuning jest dostępny tylko dla OpenAI. Przełączam na OpenAI.")
    ENGINE = "openai"

print(f"🔄 ENGINE wykryty: {ENGINE}")

# Sprawdzenie zmiennych środowiskowych
LAB_DATA_URL: str = os.getenv("LAB_DATA_URL")
REPORT_URL: str = os.getenv("REPORT_URL")
CENTRALA_API_KEY: str = os.getenv("CENTRALA_API_KEY")

if not all([LAB_DATA_URL, REPORT_URL, CENTRALA_API_KEY]):
    print(
        "❌ Brak wymaganych zmiennych: LAB_DATA_URL, REPORT_URL, CENTRALA_API_KEY",
        file=sys.stderr,
    )
    sys.exit(1)

# Konfiguracja modelu
if ENGINE == "openai":
    MODEL_NAME: str = os.getenv("MODEL_NAME") or os.getenv(
        "MODEL_NAME_OPENAI", "gpt-4o-mini"
    )
    BASE_MODEL_FOR_FINETUNING: str = (
        "gpt-4o-mini-2024-07-18"  # Model bazowy do fine-tuningu
    )

print(f"✅ Model: {MODEL_NAME}")

# Sprawdzenie API keys
if ENGINE == "openai" and not os.getenv("OPENAI_API_KEY"):
    print("❌ Brak OPENAI_API_KEY", file=sys.stderr)
    sys.exit(1)


# 2. Typowanie stanu pipeline
class PipelineState(TypedDict, total=False):
    lab_data_dir: Path
    training_file_path: Path
    training_file_id: Optional[str]
    fine_tune_job_id: Optional[str]
    fine_tuned_model_id: Optional[str]
    verification_results: List[Tuple[str, bool]]  # (id, is_correct)
    correct_ids: List[str]
    result: Optional[str]


# 3. Funkcje pomocnicze
def download_and_extract_data(dest_dir: Path) -> None:
    """Pobiera i rozpakowuje dane laboratoryjne"""
    # Sprawdź czy pliki już istnieją (z dokumentów)
    expected_files = ["correct.txt", "incorrect.txt", "verify.txt"]
    root_files_exist = all((Path(f).exists() for f in expected_files))

    if root_files_exist:
        logger.info("📂 Znaleziono pliki lokalne w katalogu głównym, kopiuję...")
        dest_dir.mkdir(parents=True, exist_ok=True)
        for filename in expected_files:
            src = Path(filename)
            dst = dest_dir / filename
            if src.exists():
                dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                logger.info(f"   ✅ Skopiowano {filename}")
        return

    # Jeśli nie ma lokalnych plików, pobierz z URL
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "lab_data.zip"

    logger.info(f"📥 Pobieranie danych z {LAB_DATA_URL}...")

    try:
        response = requests.get(LAB_DATA_URL, stream=True)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info("📦 Rozpakowywanie archiwum...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            # Sprawdź zawartość archiwum
            file_list = zf.namelist()
            logger.info(f"   Pliki w archiwum: {file_list}")

            # Rozpakuj wszystko
            zf.extractall(dest_dir)

        # Sprawdź czy pliki są w podkatalogu i przenieś je do głównego katalogu
        for subdir in dest_dir.iterdir():
            if subdir.is_dir():
                for file in subdir.iterdir():
                    if file.name in expected_files:
                        target = dest_dir / file.name
                        file.rename(target)
                        logger.info(f"   ✅ Przeniesiono {file.name} z {subdir.name}")

        # Usuń archiwum
        zip_path.unlink()

        # Po rozpakowaniu, jeśli brakuje incorrect.txt, a jest incorect.txt, kopiuj/pliku
        incorrect_path = dest_dir / "incorrect.txt"
        incorect_path = dest_dir / "incorect.txt"
        if not incorrect_path.exists() and incorect_path.exists():
            incorect_path.rename(incorrect_path)
            logger.info("   ✅ Skorygowano nazwę pliku: incorect.txt -> incorrect.txt")

        # Sprawdź czy wszystkie pliki są obecne
        for filename in expected_files:
            if not (dest_dir / filename).exists():
                logger.error(f"❌ Brak pliku: {filename}")
                raise FileNotFoundError(
                    f"Nie znaleziono pliku {filename} po rozpakowaniu"
                )

        logger.info("✅ Dane rozpakowane pomyślnie")

    except Exception as e:
        logger.error(f"❌ Błąd podczas pobierania/rozpakowywania: {e}")
        raise


def prepare_training_data(data_dir: Path, output_file: Path) -> int:
    """Przygotowuje dane treningowe w formacie JSONL"""
    logger.info("📝 Przygotowywanie danych treningowych...")

    entries = []

    # Wczytaj dane poprawne
    correct_file = data_dir / "correct.txt"
    with open(correct_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(
                    {
                        "messages": [
                            {"role": "system", "content": "validate data"},
                            {"role": "user", "content": line},
                            {"role": "assistant", "content": "1"},
                        ]
                    }
                )

    logger.info(f"✅ Załadowano {len(entries)} poprawnych próbek")

    # Wczytaj dane niepoprawne - sprawdź różne warianty nazwy
    incorrect_count = 0
    incorrect_variants = ["incorrect.txt", "incorect.txt"]  # Z błędem w nazwie
    incorrect_file = None

    for variant in incorrect_variants:
        test_file = data_dir / variant
        if test_file.exists():
            incorrect_file = test_file
            logger.info(f"   Znaleziono plik z nieprawidłowymi danymi: {variant}")
            break

    if not incorrect_file:
        logger.error(
            "❌ Nie znaleziono pliku z nieprawidłowymi danymi (incorrect.txt lub incorect.txt)"
        )
        return 0

    with open(incorrect_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(
                    {
                        "messages": [
                            {"role": "system", "content": "validate data"},
                            {"role": "user", "content": line},
                            {"role": "assistant", "content": "0"},
                        ]
                    }
                )
                incorrect_count += 1

    logger.info(f"✅ Załadowano {incorrect_count} niepoprawnych próbek")

    # Zapisz do pliku JSONL
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    logger.info(f"💾 Zapisano {len(entries)} próbek do {output_file}")
    return len(entries)


def upload_training_file(file_path: Path) -> Optional[str]:
    """Uploaduje plik treningowy do OpenAI"""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    logger.info("📤 Wysyłanie pliku treningowego do OpenAI...")

    try:
        with open(file_path, "rb") as f:
            response = client.files.create(file=f, purpose="fine-tune")

        file_id = response.id
        logger.info(f"✅ Plik wysłany pomyślnie. ID: {file_id}")
        return file_id

    except Exception as e:
        logger.error(f"❌ Błąd podczas wysyłania pliku: {e}")
        return None


def start_fine_tuning(training_file_id: str) -> Optional[str]:
    """Rozpoczyna proces fine-tuningu"""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    logger.info("🚀 Rozpoczynanie fine-tuningu...")

    try:
        response = client.fine_tuning.jobs.create(
            training_file=training_file_id,
            model=BASE_MODEL_FOR_FINETUNING,
            suffix="lab-data-validator",
            seed=42,  # Dodanie seed zgodnie z dokumentacją
        )

        job_id = response.id
        logger.info(f"✅ Fine-tuning rozpoczęty. Job ID: {job_id}")
        return job_id

    except Exception as e:
        logger.error(f"❌ Błąd podczas rozpoczynania fine-tuningu: {e}")
        return None


def wait_for_fine_tuning(job_id: str) -> Optional[str]:
    """Czeka na zakończenie fine-tuningu i zwraca ID modelu"""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    logger.info("⏳ Czekam na zakończenie fine-tuningu...")

    while True:
        try:
            job = client.fine_tuning.jobs.retrieve(job_id)
            status = job.status

            logger.info(f"   Status: {status}")

            if status == "succeeded":
                model_id = job.fine_tuned_model
                logger.info(f"✅ Fine-tuning zakończony! Model: {model_id}")
                return model_id
            elif status == "failed":
                logger.error(f"❌ Fine-tuning zakończony niepowodzeniem")
                logger.error(f"   Szczegóły: {job}")
                return None
            elif status == "cancelled":
                logger.error(f"❌ Fine-tuning został anulowany")
                return None

        except Exception as e:
            logger.error(f"❌ Błąd podczas sprawdzania statusu: {e}")
            return None

        # Czekaj 30 sekund przed kolejnym sprawdzeniem
        time.sleep(30)


def verify_sample(model_id: str, sample: str) -> bool:
    """Weryfikuje próbkę używając wytrenowanego modelu"""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "validate data"},
                {"role": "user", "content": sample},
            ],
            temperature=0,
            max_tokens=1,
        )

        result = response.choices[0].message.content.strip()
        return result == "1"

    except Exception as e:
        logger.error(f"❌ Błąd podczas weryfikacji próbki: {e}")
        return False


# 4. Nodes dla LangGraph
def download_data_node(state: PipelineState) -> PipelineState:
    """Pobiera i rozpakowuje dane laboratoryjne"""
    logger.info("📁 Przygotowywanie katalogu na dane...")

    data_dir = Path("lab_data")

    # Jeśli istnieją pliki w dokumentach, użyj ich
    if (
        Path("correct.txt").exists()
        and Path("incorect.txt").exists()
        and Path("verify.txt").exists()
    ):
        logger.info("📂 Znaleziono pliki lokalne, kopiuję do katalogu roboczego...")
        data_dir.mkdir(parents=True, exist_ok=True)

        # Kopiuj pliki zachowując oryginalne nazwy i poprawiając błędne
        Path("correct.txt").read_text(encoding="utf-8")
        (data_dir / "correct.txt").write_text(
            Path("correct.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )

        # Kopiuj incorect.txt jako incorrect.txt (poprawiona nazwa)
        (data_dir / "incorrect.txt").write_text(
            Path("incorect.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )
        (data_dir / "incorect.txt").write_text(
            Path("incorect.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )  # Zachowaj też oryginalną nazwę

        (data_dir / "verify.txt").write_text(
            Path("verify.txt").read_text(encoding="utf-8"), encoding="utf-8"
        )

        logger.info("✅ Pliki skopiowane pomyślnie")
    else:
        # Jeśli nie ma lokalnych plików, pobierz z URL
        download_and_extract_data(data_dir)

    state["lab_data_dir"] = data_dir
    return state


def prepare_training_node(state: PipelineState) -> PipelineState:
    """Przygotowuje dane treningowe"""
    data_dir = state.get("lab_data_dir")
    if not data_dir:
        logger.error("❌ Brak katalogu z danymi")
        return state

    training_file = data_dir / "training_data.jsonl"
    sample_count = prepare_training_data(data_dir, training_file)

    if sample_count < 10:
        logger.error(f"❌ Za mało próbek treningowych: {sample_count} (minimum 10)")
        return state

    state["training_file_path"] = training_file
    return state


def upload_training_file_node(state: PipelineState) -> PipelineState:
    """Wysyła plik treningowy do OpenAI"""
    if args.skip_training:
        logger.info("⏭️  Pomijam wysyłanie pliku treningowego (--skip-training)")
        return state

    training_file = state.get("training_file_path")
    if not training_file:
        logger.error("❌ Brak pliku treningowego")
        return state

    file_id = upload_training_file(training_file)
    state["training_file_id"] = file_id
    return state


def start_fine_tuning_node(state: PipelineState) -> PipelineState:
    """Rozpoczyna fine-tuning"""
    if args.skip_training:
        logger.info("⏭️  Pomijam fine-tuning (--skip-training)")
        if args.model_id:
            state["fine_tuned_model_id"] = args.model_id
            logger.info(f"📌 Używam modelu: {args.model_id}")
        else:
            logger.error("❌ Brak --model-id przy --skip-training")
        return state

    # Jeśli użytkownik podał istniejący job-id, nie twórz nowego zadania
    if args.job_id:
        logger.info(f"📌 Używam istniejącego job-id: {args.job_id}")
        state["fine_tune_job_id"] = args.job_id
        return state

    file_id = state.get("training_file_id")
    if not file_id:
        logger.error("❌ Brak ID pliku treningowego")
        return state

    job_id = start_fine_tuning(file_id)
    state["fine_tune_job_id"] = job_id
    return state


def wait_for_training_node(state: PipelineState) -> PipelineState:
    """Czeka na zakończenie treningu"""
    if args.skip_training:
        logger.info("⏭️  Pomijam czekanie na trening (--skip-training)")
        return state

    job_id = state.get("fine_tune_job_id")
    if not job_id:
        logger.error("❌ Brak ID zadania fine-tuningu")
        return state

    model_id = None
    if args.model_id:
        # Gdy mamy już gotowy model-id, pomiń polling
        logger.info(f"📌 Pomijam oczekiwanie — używam podanego modelu: {args.model_id}")
        model_id = args.model_id
    else:
        model_id = wait_for_fine_tuning(job_id)
    state["fine_tuned_model_id"] = model_id

    if model_id:
        logger.info(f"💡 Aby pominąć trening w przyszłości, użyj:")
        logger.info(f"   python {sys.argv[0]} --skip-training --model-id {model_id}")

    return state


def verify_samples_node(state: PipelineState) -> PipelineState:
    """Weryfikuje próbki z pliku verify.txt"""
    model_id = state.get("fine_tuned_model_id")
    if not model_id:
        logger.error("❌ Brak ID wytrenowanego modelu")
        return state

    data_dir = state.get("lab_data_dir")
    if not data_dir:
        logger.error("❌ Brak katalogu z danymi")
        return state

    verify_file = data_dir / "verify.txt"
    if not verify_file.exists():
        logger.error(f"❌ Nie znaleziono pliku: {verify_file}")
        return state

    logger.info("🔍 Weryfikacja próbek...")

    results = []
    correct_ids = []

    with open(verify_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parsuj linię: ID=dane
            parts = line.split("=", 1)
            if len(parts) != 2:
                logger.warning(f"⚠️  Nieprawidłowy format linii: {line}")
                continue

            sample_id = parts[0]
            sample_data = parts[1]

            # Weryfikuj próbkę
            is_correct = verify_sample(model_id, sample_data)
            results.append((sample_id, is_correct))

            if is_correct:
                correct_ids.append(sample_id)
                logger.info(f"   ✅ {sample_id}: POPRAWNE")
            else:
                logger.info(f"   ❌ {sample_id}: SFAŁSZOWANE")

    state["verification_results"] = results
    state["correct_ids"] = correct_ids

    logger.info(f"📊 Wyniki: {len(correct_ids)}/{len(results)} poprawnych")

    return state


def send_answer_node(state: PipelineState) -> PipelineState:
    """Wysyła wyniki do centrali"""
    correct_ids = state.get("correct_ids", [])

    if not correct_ids:
        logger.warning("⚠️  Brak poprawnych próbek do wysłania")

    payload = {"task": "research", "apikey": CENTRALA_API_KEY, "answer": correct_ids}

    logger.info(f"📡 Wysyłam {len(correct_ids)} poprawnych identyfikatorów...")
    logger.info(f"   IDs: {correct_ids}")

    try:
        response = requests.post(REPORT_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        logger.info(f"✅ Odpowiedź centrali: {result}")

        # Sprawdż czy jest flaga
        if "FLG" in str(result):
            print(f"🏁 {result.get('message', result)}")
            state["result"] = result.get("message", str(result))

    except Exception as e:
        logger.error(f"❌ Błąd wysyłania: {e}")
        if hasattr(e, "response") and e.response:
            logger.error(f"   Szczegóły: {e.response.text}")

    return state


def build_graph() -> Any:
    """Buduje graf LangGraph"""
    graph = StateGraph(state_schema=PipelineState)

    # Dodaj nodes
    graph.add_node("download_data", download_data_node)
    graph.add_node("prepare_training", prepare_training_node)
    graph.add_node("upload_training_file", upload_training_file_node)
    graph.add_node("start_fine_tuning", start_fine_tuning_node)
    graph.add_node("wait_for_training", wait_for_training_node)
    graph.add_node("verify_samples", verify_samples_node)
    graph.add_node("send_answer", send_answer_node)

    # Dodaj edges
    graph.add_edge(START, "download_data")
    graph.add_edge("download_data", "prepare_training")
    graph.add_edge("prepare_training", "upload_training_file")
    graph.add_edge("upload_training_file", "start_fine_tuning")
    graph.add_edge("start_fine_tuning", "wait_for_training")
    graph.add_edge("wait_for_training", "verify_samples")
    graph.add_edge("verify_samples", "send_answer")
    graph.add_edge("send_answer", END)

    return graph.compile()


def main() -> None:
    print("=== Zadanie 16: Wykrywanie sfałszowanych danych ===")
    print(f"🚀 Używam silnika: {ENGINE}")
    print(f"🔧 Model: {MODEL_NAME}")

    if args.skip_training:
        print(f"⏭️  Tryb: Pomijam trening")
        if args.model_id:
            print(f"📌 Model do użycia: {args.model_id}")
        else:
            print("❌ Brak --model-id. Wymagany przy --skip-training")
            sys.exit(1)
    else:
        print(f"🎯 Model bazowy do fine-tuningu: {BASE_MODEL_FOR_FINETUNING}")

    # Sprawdź dostępność plików
    local_files = (
        Path("correct.txt").exists()
        and Path("incorect.txt").exists()
        and Path("verify.txt").exists()
    )
    if local_files:
        print("📂 Znaleziono pliki lokalne - będą użyte zamiast pobierania")
    else:
        print(f"🌐 Pliki będą pobrane z: {LAB_DATA_URL}")

    print("Startuje pipeline...\n")

    try:
        graph = build_graph()
        result: PipelineState = graph.invoke({})

        if result.get("result"):
            print(f"\n🎉 Zadanie zakończone!")
        else:
            print("\n✅ Proces zakończony")

            # Pokaż podsumowanie
            if result.get("correct_ids"):
                print(
                    f"\n📊 Znaleziono {len(result['correct_ids'])} poprawnych próbek:"
                )
                print(f"   {result['correct_ids']}")

            if result.get("fine_tuned_model_id") and not args.skip_training:
                print(f"\n💾 Wytrenowany model: {result['fine_tuned_model_id']}")
                print(f"   Możesz go użyć później z flagą:")
                print(f"   --skip-training --model-id {result['fine_tuned_model_id']}")

    except Exception as e:
        print(f"❌ Błąd: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()