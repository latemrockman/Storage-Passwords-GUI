import pprint

import main
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from form_generator import *
#import src_rc
import random
import pyperclip

generate_dict = main.generate_dict
correct_pass = "привет"
#generate_dict = {
#    "pass_len"          : 7,
#    "is_eng"            : True,
#    "is_rus"            : False,
#    "is_lower"          : True,
#    "is_upper"          : True,
#    "is_digit"          : True,
#    "is_simbol"         : False,
#    "exc_repeat"        : True,
#    "exc_rus_like_eng"  : True,
#    "exc_eng_like_rus"  : True,
#    "exc_Vowels"        : False,
#    "exc_Consonants"    : False}



class Password():

    def checkLen(self,alpha,exc_repeat,pass_len):
        if exc_repeat and pass_len > len(alpha):
            return False
        else:
            return True

    def generatePass(self, pass_len, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol, exc_repeat, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants):
        alpha = Alpha().createAlpha(pass_len, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol, exc_repeat, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants)

        if alpha == "":
            return "Измените настройки!"

        if self.checkLen(alpha, exc_repeat, pass_len):
            result = ""

            for i in range(0, pass_len):
                r = random.randint(0, len(alpha) - 1)
                result += alpha[r]

                if exc_repeat:
                    alpha = alpha.replace(result[-1], "")

            return result
        else:
            return "Не хватает уникальных символов!"

class Alpha():
    lettersRusVowels = "аеёиоуыэюя"
    lettersRusConsonants = "бвгджзйклмнпрстфхцчшщъь"
    lettersEngVowels = "aeiouy"
    lettersEngConsonants = "bcdfghjklmnpqrstvwxz"

    rusLikeEng = "аеиоубвкмнрсх"
    engLikeRus = "aeouybchkmptx"

    numbers = "0123456789"
    simbols = """!?@#$%&(){}[]<>^_+-*=~.,:;`"'/|\\"""

    def createSet(self, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol):
        self.set_alpha = ""

        if is_eng:
            self.set_alpha += self.lettersEngVowels + self.lettersEngConsonants
        if is_rus:
            self.set_alpha += self.lettersRusVowels + self.lettersRusConsonants
        if is_digit:
            self.set_alpha += self.numbers
        if is_simbol:
            self.set_alpha += self.simbols

        if is_lower and is_upper:
            for letter in self.set_alpha:
                if letter.isalpha():
                    self.set_alpha += letter.upper()
        elif not is_lower and is_upper:
            for letter in self.set_alpha:
                if letter.isalpha():
                    self.set_alpha = self.set_alpha.replace(letter, letter.upper())

        return self.set_alpha

    def createExc(self, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants):
        self.exc_alpha = ""

        if exc_eng_like_rus:
            self.exc_alpha += self.engLikeRus + self.engLikeRus.upper()
        if exc_rus_like_eng:
            self.exc_alpha += self.rusLikeEng + self.rusLikeEng.upper()
        if exc_Vowels:
            self.exc_alpha += self.lettersRusVowels + self.lettersRusVowels.upper() + self.lettersEngVowels + self.lettersEngVowels.upper()
        if exc_Consonants:
            self.exc_alpha += self.lettersRusConsonants + self.lettersRusConsonants.upper() + self.lettersEngConsonants + self.lettersEngConsonants.upper()

        return self.exc_alpha

    def createAlpha(self,pass_len, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol, exc_repeat, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants):
        self.alpha = ""

        set = Alpha.createSet(self, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol)
        exc = Alpha.createExc(self, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants)

        for letter in set:
            if not letter in exc:
                self.alpha += letter

        return self.alpha


class MyWin(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.set_settings()

        self.ui.btnGenerate.clicked.connect(self.printPassword)
        self.ui.btnCopy.clicked.connect(self.copyPass)


        self.ui.spinLen.valueChanged.connect(self.spinLen_change)

        self.ui.checkEng.stateChanged.connect(self.checkEng_change)
        self.ui.checkRus.stateChanged.connect(self.checkRus_change)
        self.ui.checkNumbers.stateChanged.connect(self.checkNumbers_change)
        self.ui.checkBig.stateChanged.connect(self.checkBig_change)
        self.ui.checkSmall.stateChanged.connect(self.checkSmall_change)
        self.ui.checkSimbols.stateChanged.connect(self.checkSimbols_change)

        self.ui.checkReplays.stateChanged.connect(self.checkReplays_change)
        self.ui.checkRuslikeEng.stateChanged.connect(self.checkRuslikeEng_change)
        self.ui.checkEngLikeRus.stateChanged.connect(self.checkEngLikeRus_change)
        self.ui.checkVowels.stateChanged.connect(self.checkVowels_change)
        self.ui.checkConsonants.stateChanged.connect(self.checkConsonants_change)




    def set_settings(self):
        dict_settings = {
            self.ui.checkEng        : "is_eng",
            self.ui.checkRus        : "is_rus",
            self.ui.checkNumbers    : "is_digit",
            self.ui.checkBig        : "is_upper",
            self.ui.checkSmall      : "is_lower",
            self.ui.checkSimbols    : "is_simbol",
            self.ui.checkReplays    : "exc_repeat",
            self.ui.checkRuslikeEng : "exc_rus_like_eng",
            self.ui.checkEngLikeRus : "exc_eng_like_rus",
            self.ui.checkVowels     : "exc_Vowels",
            self.ui.checkConsonants : "exc_Consonants"}

        self.ui.spinLen.setValue(main.generate_dict["pass_len"])

        for obj, key in dict_settings.items():
            obj.setChecked(main.generate_dict[key])




    def spinLen_change(self):
        generate_dict["pass_len"] = self.ui.spinLen.value()
        pprint.pprint(generate_dict)
    def checkEng_change(self):
        generate_dict["is_eng"] = self.ui.checkEng.isChecked()
        pprint.pprint(main.generate_dict)
    def checkRus_change(self):
        generate_dict["is_rus"] = self.ui.checkRus.isChecked()
        pprint.pprint(main.generate_dict)
    def checkNumbers_change(self):
        generate_dict["is_digit"] = self.ui.checkNumbers.isChecked()
        pprint.pprint(main.generate_dict)
    def checkBig_change(self):
        generate_dict["is_upper"] = self.ui.checkBig.isChecked()
        pprint.pprint(main.generate_dict)
    def checkSmall_change(self):
        generate_dict["is_lower"] = self.ui.checkSmall.isChecked()
        pprint.pprint(main.generate_dict)
    def checkSimbols_change(self):
        generate_dict["is_simbol"] = self.ui.checkSimbols.isChecked()
        pprint.pprint(main.generate_dict)
    def checkReplays_change(self):
        generate_dict["exc_repeat"] = self.ui.checkReplays.isChecked()
        pprint.pprint(main.generate_dict)
    def checkRuslikeEng_change(self):
        generate_dict["exc_rus_like_eng"] = self.ui.checkRuslikeEng.isChecked()
        pprint.pprint(main.generate_dict)
    def checkEngLikeRus_change(self):
        generate_dict["exc_eng_like_rus"] = self.ui.checkEngLikeRus.isChecked()
        pprint.pprint(main.generate_dict)
    def checkVowels_change(self):
        generate_dict["exc_Vowels"] = self.ui.checkVowels.isChecked()
        pprint.pprint(main.generate_dict)
    def checkConsonants_change(self):
        generate_dict["exc_Consonants"] = self.ui.checkConsonants.isChecked()
        pprint.pprint(main.generate_dict)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        main.save_file(main.file_name)
        main.open_file(main.file_name)
        main.update_password_settings()
        print("by")


    def printPassword(self):

        # Длина пароля
        pass_len = self.ui.spinLen.value()

        # Настройки
        is_eng = self.ui.checkEng.isChecked()
        is_rus = self.ui.checkRus.isChecked()
        is_lower = self.ui.checkSmall.isChecked()
        is_upper = self.ui.checkBig.isChecked()
        is_digit = self.ui.checkNumbers.isChecked()
        is_simbol = self.ui.checkSimbols.isChecked()

        # Исключения
        exc_repeat = self.ui.checkReplays.isChecked()
        exc_rus_like_eng = self.ui.checkRuslikeEng.isChecked()
        exc_eng_like_rus = self.ui.checkEngLikeRus.isChecked()
        exc_Vowels = self.ui.checkVowels.isChecked()
        exc_Consonants = self.ui.checkConsonants.isChecked()

        password = Password().generatePass(pass_len, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol,
                                           exc_repeat, exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants)
        self.ui.labelPassword.setText(password)



    def copyPass(self):
        password = self.ui.labelPassword.text()
        pyperclip.copy(password)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())