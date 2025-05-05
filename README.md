# Wypisz Ojczyzna Alfa
## Interpreter w Python autorskiego języka ezoterycznego
Wypisz Ojczyzna (wersja) Alfa. Autorski projekt języka ezoterycznego w ramach projektu. Język używa języka polskiego jako źródła słów kluczowych, nie języka angielskiego, jak to ma miejsce w standardowych językach programowania. Charakterystyczną cechą można by określić brak znaków w języku typu `,`, `.`, `-`, `(`, itp. Język składa się z słów, cyfr, enterów, spacji i tabów, które odgrywają tu istatną rolę, jak w przypadku języka Python. Teoretycznie powinien być Turing-kompletny. Jak się pisze w tym języku najlepiej zobaczyć na przykładach poniżej.

Jest to wersja Alfa, przez co może wciąż mieć wiele błędów. Jeśli ktoś tu zajrzy i stwierdzi, że wygląda całkiem ciekawie, może śmiało podjąć się rozbudowywania tego języka i interpretera w ramach forków czy w jakiejś innej formie, jeśli ma taką ochotę. To repozytorium nie będzie raczej aktualizowane.

> Aby uruchomić interpreter należy mieć zainstalowany Python na komputerze i uruchomić poprzez konsolę wpisując `python interpreter.py` będąc w folderze z plikiem .py. Ewentualnie skompilować to do pliku .exe.

## SŁOWA KLUCZOWE:

```
utwórz zmienną

dodać, odjąć, razy, przez, mod

jeśli
inaczej jeśli
inaczej

równe, różne, mniejsze, większe, mniejszeRówne, większeRówne, i, lub

powtarzaj
```


#### należy pamiętać, że język jest wrażliwy na wcięcia poprzez tab, podobnie jak python

## tworzenie zmiennej X:

### tworzy zmienną null
```
utwórz zmienną X 
```
### tworzy zmienną o wartości 5
```
utwórz zmienną X równe 5 
```
### tworzy zmienną o wartości 4
```
utwórz zmienną X równe 2 dodać 2 
```

## manipulacja zmienną X:
### przypisze do zmiennej wartość 5
```
X równe 5 
```
### podwoi wartość X
```
X równe X razy 2 
```

## Instrukcja warunkowa:
```
jeśli <waunek>
	<blok instrukcji>
```
### wykonuje się jeśli X jest mniejsze niż 5
```
jeśli X mniejsze 5 
	<blok instrukcji>
```
### elif
```
inaczej jeśli X mniejsze 10
	<blok instrukcji>
```
### else, brak warunków
```
inaczej 
	<blok instrukcji>
```

## Pętla:
```
powtarzaj <warunek>
	<blok instrukcji>
```
### blok instrukcji będzie wykonywał się tak długo, jak będzie spełniany warunek
```
powtarzaj X mniejsze 10 
	<blok instrukcji>
```


## PRZYKŁADOWY KOD:
```
utwórz zmienną X równe 0
powtarzaj X mniejsze 5
	wypisz pętla X
	X równe X dodać 1
	jeśli X równe 5
		wypisz potwierdzam 5
	inaczej jeśli X równe 4
		wypisz potwierdzam 4
	inaczej
		wypisz nie równa się 4 lub 5
wypisz koniec działań
```
Co powinno wypisać:
```
pętla 0
nie równa się 4 lub 5
pętla 1
nie równa się 4 lub 5
pętla 2
nie równa się 4 lub 5
pętla 3
potwierdzam 4
pętla 4
potwierdzam 5
koniec działań
```

### Nie skończone rzeczy:
W kodzie znajduje się wstępnie przygotowane miejsce na funkcję w postaci `utwórz funkcję`, ale jest nie ruszone poza sam wstęp.
