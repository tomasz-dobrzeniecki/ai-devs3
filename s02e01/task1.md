Twoim zadaniem jest ustalenie nazwy ulicy, na której znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj. Informacje potrzebne do rozwiązania zadania znajdują się w nagraniach z przesłuchań świadków.

<objective>
Przygotuj skrypt Python rozwiązujący zadanie.
</objective>

<prompt_designing_steps>
Wykonaj drobiazgowo poniższe kroki:

1. Zapoznaj się z plikami audio w formacie m4a. 
Jeśli nie umiesz jeszcze tego zrobić, powiedz o tym.

2. Wygeneruj transkrypcje nagrań. 
Użyj modelu Whisper od OpenAI do wygenerowania transkrypcji każdego z nagrań.

3. Zbuduj wspólny kontekst dla LLM. 
Możesz połączyć wszystkie transkrypcje w jeden tekst. Ten tekst będzie stanowił kontekst dla Twojego promptu.

4. Sformułuj prompt
Przygotuj prompt dla LLM, który nakłoni go do znalezienia konkretnej ulicy, na której znajduje się konkretny instytut, w którym pracuje Andrzej Maj. Aby szybciej uzyskać bardziej stabilne wyniki, możesz użyć "myślenia na głos". Prompt powinien zawierać następujące elementy:

   *   Informację o tym, że model ma ustalić, na jakiej ulicy znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj. Pamiętaj, że zadaniem jest znalezienie ulicy, na której znajduje się instytut, a nie główna siedziba uczelni.

   *   Cały tekst z transkrypcjami nagrań (jako kontekst).

   *   Prośbę o to, żeby model krok po kroku analizował transkrypcje i wyciągał wnioski.

   *   Polecenie, żeby model użył swojej wiedzy na temat tej konkretnej uczelni, aby ustalić nazwę ulicy.

Zastanów się czy sformułowanie promptu po polsku pomaga, czy przeszkadza uzyskać prawidłowy wynik?

5. Wyślij odpowiedź do Centrali
Wyślij nazwę ulicy do https://c3ntrala.ag3nts.org/report w formacie JSON. Upewnij się, że wysyłasz dane zakodowane w UTF-8 Przykładowy payload:

{
  "task": "mp3",
  "apikey": "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948",
  "answer": "ul. Jana Długosza"
}

Jeśli Twoja odpowiedź będzie poprawna, uzyskasz flagę do wpisania do Centrali. Przykładowa response:

{
  "code": 0,
  "message": "{{FLG:....}}"
}

Use clear, direct language aligned with Grice's Maxims. Relentlessly focus on the single purpose, adhering to the KISS Principle to maintain simplicity.
</prompt_designing_steps>

<wskazówki>
- Skup się na tym, żeby prompt był jasny i precyzyjny. Model powinien wiedzieć, że ma analizować transkrypcje i użyć swojej wewnętrznej wiedzy o uczelniach. 
- Uważaj na to, że jedno z nagrań jest bardziej chaotyczne. Model może mieć problemy z jego interpretacją. Niektóre nagrania mogą wprowadzać w błąd — uwzględnij tę informację w prompcie. 
- Pamiętaj, że całą wiedzę musisz wyciągnąć z transkrypcji i swojej wiedzy o uczelniach w Polsce.
</wskazówki>

<keywords_that_may_be_useful>
- Prompt Engineering: Chain-of-Thought, Zero-Shot Learning, Instruction Tuning, Tree of Thoughts, Contextual Embedding, Meta-Prompting
- Communication: Grice's Maxims, Active Listening, Ethos/Pathos/Logos, Socratic Method
- Problem-Solving: First Principles, Inversion, Second-Order Thinking, OODA Loop, Fermi Estimation
- Mental Models: Occam's Razor, Pareto Principle, Hanlon's Razor, Map vs. Territory, Antifragility
- Cognitive Biases: Confirmation Bias, Survivorship Bias, Dunning-Kruger Effect, Availability Heuristic
- Decision Making: Expected Value, Opportunity Cost, Asymmetric Risk-Reward, Bayesian Updating
- Systems Thinking: Feedback Loops, Emergence, Network Effects, Chaos Theory, Butterfly Effect
- Design Principles: SOLID, DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid)
- Cognitive Concepts: Cognitive Load Theory, Semantic Networks, Chunking, Distributed Cognition
</keywords_that_may_be_useful>

<best_practices_for_writing_prompts>
- Be Specific and Clear: Use the SMART Criteria to ensure objectives and instructions are clear and attainable.
- Utilize Structured Thinking: Apply the Chain-of-Thought Prompting technique to encourage logical progression in responses.
- Engage in Active Communication: Follow Grice's Maxims and the Cooperative Principle to make interactions effective and cooperative.
- Incorporate Relevant Frameworks: Leverage Design Patterns and Agile Methodology principles to structure prompts efficiently.
- Consider Cognitive Load: Be mindful of Cognitive Load Theory to avoid overwhelming the model with too much information at once.
- Iterative Refinement: Employ the PDCA Cycle (Plan, Do, Check, Act) to continually refine and improve prompts.
- Embrace Simplicity: Follow the KISS Principle to keep prompts straightforward and focused.
- Avoid Ambiguity: Use precise language and define terms clearly to prevent misunderstandings.
- Test with Diverse Examples: Ensure prompts perform well across different scenarios by testing with varied inputs, including edge cases.
</best_practices_for_writing_prompts>