from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QTextEdit, QPushButton, QLabel
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class Highlighter(QSyntaxHighlighter):
    """Podświetlanie składni dla języka"""
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF4500"))  # Pomarańczowy
        keyword_format.setFontWeight(QFont.Weight.Bold)

        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor("#008000"))  # Zielony

        operation_format = QTextCharFormat()
        operation_format.setForeground(QColor('#0000FF')) #niebieski
        operation_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)wypisz(?!\w)"), keyword_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)utwórz(?!\w)"), keyword_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)zmienną(?!\w)"), keyword_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)jeśli(?!\w)"), keyword_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)inaczej(?!\w)"), keyword_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)powtarzaj(?!\w)"), keyword_format))

        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)dodać(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)odjąć(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)razy(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)przez(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)mod(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)równe(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)mniejsze(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)większe(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)różne(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)mniejszeRówne(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)większeRówne(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)i(?!\w)"), operation_format))
        self.highlighting_rules.append((QRegularExpression(r"(?<!\w)lub(?!\w)"), operation_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), char_format)

class Interpreter(QWidget):
    """Główny edytor z interpreterem"""
    def __init__(self):
        super().__init__()
        self.variables = {}  # Słownik przechowujący zmienne
        self.code_matrix = []  # Tablica dwuwymiarowa na kod
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier", 14))  # Większa czcionka
        self.highlighter = Highlighter(self.editor.document())
        layout.addWidget(self.editor)

        self.run_button = QPushButton("Uruchom kod")
        self.run_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.run_button.clicked.connect(self.parse_code)  # Teraz najpierw parsujemy kod
        layout.addWidget(self.run_button)

        self.output_label = QLabel("Output:")
        self.output_label.setFont(QFont("Courier", 14))  # Większa czcionka dla wyników
        layout.addWidget(self.output_label)

        self.setLayout(layout)
        self.setWindowTitle("Wypisz Ojczyzna Alfa")
        self.resize(600, 400)




    def parse_code(self):
        """Parsowanie kodu do tablicy dwuwymiarowej"""
        self.code_matrix = []
        lines = self.editor.toPlainText().splitlines()

        for line in lines:
            depth_count = [0]
            while depth_count[0] < len(line) and line[depth_count[0]] == '\t':
                depth_count[0] += 1
            tokens = line.strip().split()
            if tokens:
                self.code_matrix.append(depth_count + tokens)  # Każda linia to lista tokenów

        #print(self.code_matrix)
        self.interpret() #odpalenie interpretera kodu





    def get_value(self, token):
        """Zwraca wartość zmiennej lub liczbę"""
        if token.startswith("wartość"):
            var_name = token.split()[1]
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                return f"Błąd: zmienna '{var_name}' nie istnieje"
        try:
            return int(token)
        except ValueError:
            return token  # Jeśli to tekst, zwraca go bez zmian


    def interpret(self):
        """Interpreter kodu na podstawie code_matrix"""
        self.output = [] # tablica przechowująca zwracany rezultat

        self.keyworlds = []
        self.operations = ["dodać", "odjąć", "razy", "przez", "mod"]
        self.comparators = ["równe", "mniejsze", "większe", "różne", "mniejszeRówne", "większeRówne", "i", "lub"]

        lines_count = len(self.code_matrix) # ilość linii kodu
        print()
        print()
        print("ROZPOCZYNAM NOWA SEKWENCJE")
        print()
        self.execute_lines(0, lines_count, 0)

        """for tokens in self.code_matrix:
            if not tokens:
                continue

            if tokens[0] == "wypisz":
                result = ""
                i = 1
                while i < len(tokens):
                    if tokens[i] == "wartość":
                        value = self.get_value(" ".join(tokens[i:i+2]))
                        i += 2
                    elif tokens[i] == "dodaj":
                        if result == "":
                            output.append("Błąd: brak wartości przed 'dodaj'")
                            break
                        i += 1
                        value = self.get_value(" ".join(tokens[i:i+2]))
                        i += 2
                        if isinstance(result, int) and isinstance(value, int):
                            result += value
                        else:
                            result = str(result) + str(value)
                    else:
                        value = tokens[i]
                        i += 1

                    if result == "":
                        result = value
                output.append(str(result))

            elif tokens[0] == "zmienna":
                if len(tokens) >= 3:
                    var_name = tokens[1]
                    var_value = " ".join(tokens[2:])
                    try:
                        var_value = int(var_value)
                    except ValueError:
                        pass  # Zostaw jako string
                    self.variables[var_name] = var_value
                else:
                    output.append("Błąd: nie podano wartości dla zmiennej")

            elif tokens[0] == "wartość":
                if len(tokens) >= 4 and tokens[2] == "dodaj":
                    var_name = tokens[1]
                    add_value = " ".join(tokens[3:])

                    if var_name not in self.variables:
                        output.append(f"Błąd: zmienna '{var_name}' nie istnieje")
                        continue

                    value1 = self.variables[var_name]
                    value2 = self.get_value(add_value)

                    if isinstance(value1, int) and isinstance(value2, int):
                        self.variables[var_name] += value2
                    else:
                        self.variables[var_name] = str(value1) + str(value2)
                else:
                    output.append("Błąd składni: użyj 'wartość zmienna dodaj coś'")#"""

        self.output_label.setText("\n".join(self.output) if self.output else "Brak wyników")
    

    # wykonuje blok kodu \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def execute_lines(self, start_line:int, stop_line:int, depth:int):
        main_line = start_line # rozpatrywana linia kodu
        
        # pętla sprawdzająca linie kodu------------------------------------\\\
        while main_line < stop_line: 
            tokens = self.code_matrix[main_line]

            if tokens[0] == depth:
                if tokens[1] == "wypisz":
                    self.wypisz(main_line)
                elif tokens[1] == "utwórz":
                    self.utwórz(main_line)
                elif tokens[1] in self.variables:
                    self.variable_handler(main_line)
                elif tokens[1] == "jeśli":
                    if self.jeśli(main_line):
                        #znaleźć ilość linii wykonywanych
                        tmp_stop = main_line
                        while tmp_stop < stop_line:
                            if tmp_stop+1 >= len(self.code_matrix):
                                break
                            if self.code_matrix[tmp_stop+1][0] > depth:
                                tmp_stop += 1
                            else:
                                break
                        self.execute_lines(main_line+1, tmp_stop+1, depth+1)
                        main_line = tmp_stop
                    else:
                        tmp_stop = main_line
                        while tmp_stop < stop_line:
                            if tmp_stop+1 >= len(self.code_matrix):
                                break
                            if self.code_matrix[tmp_stop+1][0] > depth:
                                tmp_stop += 1
                            else:
                                break
                        main_line = tmp_stop
                        while self.code_matrix[main_line+1][1] == "inaczej":
                            if len(self.code_matrix[main_line+1]) > 2:
                                if self.jeśli(main_line+1):
                                    tmp_stop = main_line+1
                                    while tmp_stop < stop_line:
                                        if self.code_matrix[tmp_stop+1][0] > depth:
                                            tmp_stop += 1
                                        else:
                                            break
                                    self.execute_lines(main_line+2, tmp_stop+1, depth+1)
                                    main_line = tmp_stop
                                    break
                                else:
                                    tmp_stop = main_line+1
                                    while tmp_stop < stop_line:
                                        if tmp_stop+1 >= len(self.code_matrix):
                                            break
                                        if self.code_matrix[tmp_stop+1][0] > depth:
                                            tmp_stop += 1
                                        else:
                                            break
                                    main_line = tmp_stop
                            else:
                                tmp_stop = main_line+1
                                while tmp_stop < stop_line:
                                    if tmp_stop+1 >= len(self.code_matrix):
                                        break
                                    if self.code_matrix[tmp_stop+1][0] > depth:
                                        tmp_stop += 1
                                    else:
                                        break
                                self.execute_lines(main_line+2, tmp_stop+1, depth+1)
                                main_line = tmp_stop
                    # pętla elif i else
                elif tokens[1] == "powtarzaj":
                    tmp_stop = main_line
                    while tmp_stop < stop_line:
                            if tmp_stop+1 >= len(self.code_matrix):
                                break
                            if self.code_matrix[tmp_stop+1][0] > depth:
                                tmp_stop += 1
                            else:
                                break
                    while True:
                        if self.jeśli(main_line) == False:
                            break
                        self.execute_lines(main_line+1, tmp_stop+1, depth+1)
                    main_line = tmp_stop
            main_line += 1
        # koniec pętli ----------------------------------------------------///
    # ////////////////////////////////////////////////////////////
    

    def wypisz(self, line:int): # tylko nowa linia
        wypisz_output = ""
        tokens = self.code_matrix[line]
        for token in range(2, len(tokens)):
            addition = ""
            # miejsce na działania i analizę tokens[token], sprawdzanie czy to nie zmienna, czy nie zachodzi działanie
            if tokens[token] in self.variables:
                addition = str(self.variables[tokens[token]])
            else:
                addition = str(tokens[token])
            wypisz_output = wypisz_output + " " + addition
        self.output.append(wypisz_output)


    def utwórz(self, line: int):  # tylko nowa linia
        tokens = self.code_matrix[line]

        if len(tokens) > 2 and tokens[2] == "zmienną":
            if len(tokens) > 3:
                var_name = tokens[3]
            else:
                self.output.append(f"BŁĄD! Nie podano nazwy zmiennej w linii {line}.")
                return

            if len(tokens) > 4 and tokens[4] == "równe":  # jeśli jest znak równości
                if len(tokens) > 5:
                    self.variables[var_name] = self.execute_operation(line, 5, len(tokens))
                else:
                    self.output.append(f"BŁĄD! Nie podano wartości w linii {line}. Wartość ustawiona na None.")
                    self.variables[var_name] = None
            else:
                self.variables[var_name] = None  # nie ma "równe"

        elif len(tokens) > 2 and tokens[2] == "funkcję":
            pass
        else:
            self.output.append(f"BŁĄD! Niepoprawna składnia w linii {line}.")
    

    def variable_handler(self, line:int): # gdy w nowej linii jest zmienna, obsługa działań
        tokens = self.code_matrix[line]
        if tokens[2] == "równe": # sprawdza czy następuje przypisywanie wartości
            self.variables[tokens[1]] = self.execute_operation(line, 3, len(tokens))


    # wykonuje działanie lub szereg działań
    def execute_operation(self, line:int, operation_start:int, operation_stop:int):
        tokens = self.code_matrix[line]
        # gdy jest jedna wartość
        if operation_start == operation_stop:
            var_value = tokens[operation_start]
            try:
                var_value = int(var_value)
            except ValueError:
                try:
                    var_value = float(var_value)
                except ValueError:
                    pass
            return var_value
        # gdy jest więcej wartości
        else:
            # sprawdzanie czy któraś wartość nie jest stringiem
            counter = operation_start
            while(counter <= operation_stop):
                var_tmp = None
                if tokens[counter] in self.variables:
                    var_tmp = self.variables[tokens[counter]]
                else:
                    var_tmp = tokens[counter]
                try:
                    var_tmp = float(var_tmp)
                except ValueError:
                    self.output.append(f"BŁĄD! Zmienna lub wartość w lini {line} jest stringiem, a powinna być liczbą. \nZmienna ustawiona na None.")
                    return None
                counter += 2
            
            # wykonywanie operacji
            operation = ""
            counter = operation_start
            while(counter <= operation_stop): # utworzenie stringa z działaniami
                if tokens[counter] in self.variables:
                    operation += str(self.variables[tokens[counter]])
                else:
                    operation += str(tokens[counter])
                
                if counter+1 < operation_stop: # sprawdzanie, czy następna pozycja istnieje
                    if tokens[counter+1] in self.operations: # sprawdzanie czy token jest działaniem
                        if tokens[counter+1] == "dodać":
                            operation += str("+")
                        elif tokens[counter+1] == "odjąć":
                            operation += str("-")
                        elif tokens[counter+1] == "razy":
                            operation += str("*")
                        elif tokens[counter+1] == "przez":
                            operation += str("/")
                        elif tokens[counter+1] == "mod":
                            operation += str("%")
                    else:
                        self.output.append(f"BŁĄD! Linia {line} zawiera token nie będący operatorem. \nSpodziewane: {self.operations}")

                counter += 2
            return eval(operation)


    def jeśli(self, line:int) -> bool:
        operation = ""
        tokens = self.code_matrix[line]
        counter = 2
        if tokens[1] == "inaczej":
            counter = 3
        while counter < len(tokens):
            if tokens[counter] in self.variables:
                operation += str(self.variables[tokens[counter]])
            elif tokens[counter] in self.comparators:
                match tokens[counter]:
                    case "równe":
                        operation += " == "
                    case "mniejsze":
                        operation += " < "
                    case "większe":
                        operation += " > "
                    case "różne":
                        operation += " != "
                    case "mniejszeRówne":
                        operation += " <= "
                    case "większeRówne":
                        operation += " >= "
                    case "i":
                        operation += " and "
                    case "lub":
                        operation += " or "
            else:
                operation += str(tokens[counter])
            counter += 1
        return eval(operation)


#########################################################################################
app = QApplication([])
window = Interpreter()
window.show()
app.exec()
