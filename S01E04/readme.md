Przeprogramuj robota w taki sposób, aby dotarł on do celu, jakim jest komputer z danymi fabryki.

Istnieją minimum dwa sposoby na osiągnięcie tego celu - możesz zaprogramować samobieżnego, autonomicznego robota, który będzie przemieszczał się po fabryce (wersja ambitna), ale możesz także poinstruować robota, jak należy poruszać się pomiędzy półkami. Nie ma znaczenia, której metody użyjesz.

Link do panelu sterowania robotem (wraz z instrukcją):
https://banan.ag3nts.org/ 


Co trzeba zrobić w zadaniu?

1. Twoim celem jest doprowadzenie robota przemysłowego do komputera z danymi. 
2. Wchodzisz w swojej przeglądarce do panelu sterowania robotem w firmie BanAN. Robisz to osobiście, nie programistycznie. To zadanie nie polaga na programowaniu, ale na napisaniu promptu który wygeneruje odpowiedni program dla robota.
3. Czytasz instrukcję obsługi robota, z której dowiadujesz się, że robot potrafi wykonywać tylko cztery polecenia: LEFT / RIGHT / UP / DOWN
4. Musisz napisać prompt, który zwraca strukturę JSON z krokami do wykonania. Kroki te będą zawarte w polu o nazwie “steps”. Wszystkie pozostałe pola w JSON-ie zostaną pominięte. Możesz więc w swoim prompcie kazać wygenerować bardziej rozbudowany JSON, byle tylko w polu "steps" znalazły się kroki które doprowadzą robota do celu. 
5. Twój prompt będzie interpretowany przez model GPT-4o-mini (nie jest on tak sprytny, jak się początkowo wydaje. Trzeba uprościć polecenia!). Model pracuje z parametrami: temperatura = 0, max tokens = 2000
6. Czasami warto wrzucić wnioskowanie robota to dodatkowego pola w JSON, ale PRZED ostateczną odpowiedzią. Podniesie to skuteczność wnioskowania oraz pozwoli Ci lepiej zrozumieć jak myśli LLM + pozwoli na poprawienie błędów. Czyli Twój prompt może na przykład wygenerować takiego JSON: 
{ 
"thinking": "skoro magazyn wygląda tak... to najpierw....", 
"steps": "UP, UP, RIGHT, ... 
} 
lub w formacie widocznym na instrukcji na stronie zadania.
7. Zadanie można rozwiązać na dwa sposoby

    1. poinstruuj robota, jak ma iść. Po prostu powiedz mu to, ale w sprytny sposób. Próby przekazania instrukcji wprost zostaną uznane za oszukiwanie.

    2. (hard!) naucz go poruszać się po labiryncie. Pamiętaj tylko, że robot nie widzi ścian. Trzeba więc opowiedzieć mu w zrozumiały dla LLM-a sposób, jak wygląda pomieszczenie, gdzie się on znajduje, gdzie ma dojść itp. Magazyn nie zmienia się. W jaki sposób możesz przekazać do LLM jego wygląd w sposób tekstowy?
8. Wersja HARD może zająć Ci nawet 1-2h, ale da niebywałą satysfakcję
9. Kiedy robot dotrze bez wypadków do celu, otrzymasz flagę

Wskazówki:

- pamiętaj że Twoim zadaniem jest wpisanie promptu w polu "program dla robota". Ten prompt ma wygenerować JSON z krokami do wykonania.
- niektóre słowa i zwroty są zakazane, będą powodować błędy wykonania (kod: -66). Niestety nie możemy ujawnić listy zakazanych słów, ale na tej liście jest między innymi "prompt".
- dla wygody, swój prompt możesz testować w playground OpenAI pod adresem https://platform.openai.com/playground/prompts?models=gpt-4o-mini - jeśli masz na swoim koncie OpenAI parę dolarów. Pamiętaj żeby ustawić temperaturę na 0 i max tokens na 2000. 
- w wersji prostszej, nie możesz w swoim prompcie po prostu podać ścieżki w formie "UP, UP, RIGHT, ..." bo zostanie to uznane za oszukiwanie. W jaki sposób można sprytnie zakodować trasę?
- w wersji trudniejszej, w jaki sposób przekazać modelowi wygląd labirytu w formie tekstowej? Jak zmusić go do poprawnego wymyślenia kroków po labiryncie? 
- pamiętaj o resetowaniu mapy między próbami. Backend i frontend weryfikują trasę niezależnie. Niezgodności między wynikami weryfikacji powodują niezaliczenie zadania. Reset mapy powoduje że backend i frontend "widzą to samo".
- warto przeczytać instrukcję na stronie zadania