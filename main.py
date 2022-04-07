import sys
import os
import encryption
import generator
import pyperclip
import pprint
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from form import *
from enterform import *
import rec_rc

default_dict = {
        "cards"     : {
            "Вконтакте" : ["www.vk.com", "latemrockman", "qwerty", "номре телефона 8 926 555 40 02\ne-mail 5554002@mail.ru"],
            "Яндекс"    : ["yandex.ru", "latemrockman", "Qwe123", "запасная почта 6strunoff@yandex.ru\nсекретный вопрос: Яичница"],
            "Мейл"      : ["mailru", "latemrockman", "QQQAAaa1", "запасная почта 5554002@mail.ru\nсекретный вопрос: Соловьева"],
            "Работа.ру" : ["rabota.ru", "latemrockman", "TREGFD", "всем привет"],
            "ГОСУСЛУГИ" : ["gosuslugi.ru", "latemrockman", "NashaRasha!_+", "СНЛС 34535367778\nИНН 6464768"],
            "Хед хантер": ["hh.ru", "latemrockman", "QwepRIVET", "ищу работу"]
        },
        "settings"  : {
            "x"     : 10,
            "y"     : 10,
            "height": 460,
            "width" : 475
        },
        "generate_pass" : {
            "pass_len"          : 7,
            "is_eng"            : True,
            "is_rus"            : False,
            "is_lower"          : True,
            "is_upper"          : True,
            "is_digit"          : True,
            "is_simbol"         : False,
            "exc_repeat"        : True,
            "exc_rus_like_eng"  : True,
            "exc_eng_like_rus"  : True,
            "exc_Vowels"        : False,
            "exc_Consonants"    : False
        }}

def update_password_settings():
    general["generate_pass"] = generator.generate_dict

def generate_password(dict):
    pass_len = dict["pass_len"]
    is_eng = dict["is_eng"]
    is_rus = dict["is_rus"]
    is_lower = dict["is_lower"]
    is_upper = dict["is_upper"]
    is_digit = dict["is_digit"]
    is_simbol = dict["is_simbol"]
    exc_repeat = dict["exc_repeat"]
    exc_rus_like_eng = dict["exc_rus_like_eng"]
    exc_eng_like_rus = dict["exc_eng_like_rus"]
    exc_Vowels = dict["exc_Vowels"]
    exc_Consonants = dict["exc_Consonants"]

    password = generator.Password().generatePass(pass_len, is_eng, is_rus, is_lower, is_upper, is_digit, is_simbol, exc_repeat,
                                       exc_rus_like_eng, exc_eng_like_rus, exc_Vowels, exc_Consonants)
    return password

def assembly_dict(dict, filter):
    result = {}
    if filter:
        for title, data in dict.items():
            card = title + data[0] + data[1] + data[2] + data[3]
            if filter.lower() in card.lower():
                result[title] = data
    else:
        result = dict

    return result

def sort_dict_in_alpha(dict):
    list_dict = []
    for key in dict.keys():
        list_dict.append(key)
    list_dict.sort(key=lambda x: x.lower())
    return list_dict

def check_for_availability_card(dict, title):
    if title in dict:
        return True
    else:
        return False

def add_new_card(dict, title, link, login, password, additionally):
    dict[title] = [link, login, password, additionally]

def edit_catd(dict, temp, title, link, login, password, additionally):
    del dict[temp]
    dict[title] = [link, login, password, additionally]

def delete_card(dict, title):
    del dict[title]

def open_file(file):
    with open(file) as open_file:
        str_from_file = open_file.read()
        str_from_file = json.loads(str_from_file)
        str_decrypt = encryption.encrypt(str_from_file, False)
        general = json.loads(str_decrypt)

        return general

def packing_general_dict():
    pass

def save_file(file):
    general["generate_pass"] = generator.generate_dict

    general_to_str = json.dumps(general)
    str_crypt = encryption.encrypt(general_to_str, True)

    with open(file, "w") as save_file:
        json.dump(str_crypt, save_file)

def create_file(file):
    general_to_str = json.dumps(default_dict)
    str_crypt = encryption.encrypt(general_to_str, True)
    with open(file, "w") as create_file:
        json.dump(str_crypt, create_file)

def export_current_card(card, file):
    with open(file, 'w') as export_file:
        export_file.write(f"{card}\n")
        underline = "=" * len(card)
        export_file.write(f"{underline}\n")
        export_file.write(f"Ссылка  : {source_dict[card][0]}\n")
        export_file.write(f"Логин     : {source_dict[card][1]}\n")
        export_file.write(f"Пароль  : {source_dict[card][2]}\n\n")
        export_file.write(f"Дополнительно:\n{source_dict[card][3]}")

def export_all_card(file):
    os.remove(file)

    string_all_cards = ""
    for card, data in source_dict.items():
        string_all_cards += f"{card}\n"
        underline = "=" * len(card)
        string_all_cards += f"{underline}\n"
        string_all_cards += f"Ссылка  : {source_dict[card][0]}\n"
        string_all_cards += f"Логин     : {source_dict[card][1]}\n"
        string_all_cards += f"Пароль  : {source_dict[card][2]}\n\n"
        string_all_cards += f"Дополнительно:\n{source_dict[card][3]}\n\n"

    with open(file, "a") as export_file:
        export_file.write(string_all_cards)

access = False
file_name = "pro.qwe"

if os.path.exists(file_name):
    open_file(file_name)
else:
    create_file(file_name)

general = open_file(file_name)
source_dict = general["cards"]
settings_dict = general["settings"]
generate_dict = general["generate_pass"]

class MyWin(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.line_find.setFixedWidth(140)
        self.ui.listWidget.setFixedWidth(140)
        self.ui.btn_exit_create.setToolTip("Завершить редактирование")
        self.ui.btn_create.setToolTip("Создать")
        self.ui.btn_read.setToolTip("Просмотр")
        self.ui.btn_edit.setToolTip("Редактировать")
        self.ui.btn_save.setToolTip("Сохранить")
        self.ui.btn_delete.setToolTip("Удалить")
        self.ui.btn_generate.setToolTip("Генерировать пароль")
        self.ui.btn_settings.setToolTip("Настройки пароля")

        self.ui.label_title.setToolTip("Копировать название")
        self.ui.label_link.setToolTip("Копировать ссылку")
        self.ui.label_login.setToolTip("Копировать логин")
        self.ui.label_password.setToolTip("Копировать пароль")
        self.ui.label_additionally.setToolTip("Копировать дополнительную информацию")

        self.set_settings()
        window = modal_window(self)
        window.show()


        # СОБЫТИЯ
        # нажатия кнопок
        self.ui.listWidget.itemClicked.connect(self.change_card_in_list)

        self.ui.btn_exit_create.clicked.connect(self.btn_exit_create)
        self.ui.btn_create.clicked.connect(self.btn_create)
        self.ui.btn_read.clicked.connect(self.btn_read)
        self.ui.btn_edit.clicked.connect(self.btn_edit)
        self.ui.btn_save.clicked.connect(self.btn_save)
        self.ui.btn_delete.clicked.connect(self.btn_delete)
        self.ui.btn_generate.clicked.connect(self.btn_generate)
        self.ui.btn_settings.clicked.connect(self.btn_settings)

        self.ui.label_title.clicked.connect(lambda: pyperclip.copy(self.ui.line_title.text()))
        self.ui.label_link.clicked.connect(lambda: pyperclip.copy(self.ui.line_link.text()))
        self.ui.label_login.clicked.connect(lambda: pyperclip.copy(self.ui.line_login.text()))
        self.ui.label_password.clicked.connect(lambda: pyperclip.copy(self.ui.line_password.text()))
        self.ui.label_additionally.clicked.connect(lambda: pyperclip.copy(self.ui.text_additionally.toPlainText()))

        self.ui.current_card.triggered.connect(self.export_current_card)
        self.ui.all_card.triggered.connect(self.export_all_card)
        self.ui.actionprint.triggered.connect(lambda: pprint.pprint(generate_dict))

        # редактирование полей ввода
        self.ui.line_find.textEdited.connect(self.editing_find)

        self.ui.line_title.textEdited.connect(self.editing_title)
        self.ui.line_link.textEdited.connect(self.editing_link)
        self.ui.line_login.textEdited.connect(self.editing_login)
        self.ui.line_password.textEdited.connect(self.editing_password)
        self.ui.text_additionally.textChanged.connect(self.editing_additionally)

        # таймер для мониторринга
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.monitoring)
        self.timer.start(1)
        #self.ui.label_monitorring_dict.hide()

        # ПЕРЕМЕННЫЕ
        self.editing = False
        self.changed = False
        self.mode = "reading"
        self.all_list_lines = {
            "title"     :   self.ui.line_title,
            "link"      :   self.ui.line_link,
            "login"     :   self.ui.line_login,
            "password"  :   self.ui.line_password}


        self.temp = ""
        self.curent_row = 0
        self.read_mode()
        self.load_cards()
        self.firs_set_focus()

    # настройки
    def set_settings(self):
        x = settings_dict["x"]+10
        y = settings_dict["y"]+35
        width = settings_dict["width"]
        height = settings_dict["height"]

        self.setGeometry(x, y, width, height)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        width = self.width()
        height = self.height()
        x = self.x()
        y = self.y()

        settings_dict["width"] = width
        settings_dict["height"] = height
        settings_dict["x"] = x
        settings_dict["y"] = y

        save_file(file_name)

    # заполнение полей
    def load_cards(self):
        self.ui.listWidget.clear()
        filter_word = self.ui.line_find.text()

        base = assembly_dict(source_dict, filter_word)
        base_list = sort_dict_in_alpha(base)

        for card in base_list:
            self.ui.listWidget.addItem(card)

        self.set_focus()
        self.load_data()

    def firs_set_focus(self):
        count_row = self.ui.listWidget.count()

        if count_row == 0:
            self.temp = ""
            return
        else:
            self.temp = self.ui.listWidget.item(0).text()

    def set_focus(self):
        count_row = self.ui.listWidget.count()

        if count_row == 0:
            self.temp = ""
            return

        list_cards = []
        for index_card in range(0, count_row):
            current_title = self.ui.listWidget.item(index_card).text()
            list_cards.append(current_title)
            if current_title == self.temp:
                self.ui.listWidget.setCurrentRow(index_card)

        if not self.temp in list_cards or self.temp == "":
            self.temp = ""
            self.ui.listWidget.setCurrentRow(0)

    def load_data(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row == -1:
            self.clear_all_line_edits()
            self.set_mode()
            return

        title = self.ui.listWidget.currentItem().text()
        link = source_dict[title][0]
        login = source_dict[title][1]
        password = source_dict[title][2]
        additionally = source_dict[title][3]

        self.ui.line_title.setText(title)
        self.ui.line_link.setText(link)
        self.ui.line_login.setText(login)
        self.ui.line_password.setText(password)
        self.ui.text_additionally.setText(additionally)
        self.set_mode()

    def clear_all_line_edits(self):
        for line in self.all_list_lines.values():
            line.clear()
        self.ui.text_additionally.clear()

    # экспорт
    def export_current_card(self):
        card = self.ui.line_title.text()
        for simbol in '\|/:*?"<>.,':
            if simbol in card:
                card = card.replace(simbol, "")

        file_path = QtWidgets.QFileDialog.getSaveFileName(self, '"Экспортировать карточку"', f'{card}', 'Text files *.txt')[0]

        if file_path:
            export_current_card(card, file_path)

    def export_all_card(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, '"Экспортировать карточку"', "Данные", 'Text files *.txt')[0]

        if file_path:
            export_all_card(file_path)

    ####################################################################################
    # редактирование полей ввода
    def change_card_in_list(self, card):
        current_row = self.ui.listWidget.currentRow()
        self.temp = card.text()
        self.load_data()

    def editing_find(self):
        self.load_cards()

    def any_text_edited(self):
        self.changed = True

        self.ui.btn_read.setDisabled(True)
        self.ui.btn_save.setDisabled(False)

    def copy_title(self):
        title = self.ui.label_title.text()
        pyperclip.copy(title)

    def editing_title(self, text):
        self.any_text_edited()

    def editing_link(self, text):
        self.any_text_edited()

    def editing_login(self, text):
        self.any_text_edited()

    def editing_login(self, text):
        self.any_text_edited()

    def editing_password(self, text):
        self.any_text_edited()

    def editing_additionally(self):
        self.any_text_edited()

    # нажатия кнопок
    def btn_generate(self):
        def write_password():
            general["generate_pass"] = generator.generate_dict
            new_password = generate_password(generate_dict)
            if new_password == "Измените настройки!":
                QtWidgets.QMessageBox.warning(self, "Генерация пароля", "Измените настройки генериции пароля!")
                self.btn_settings()
            else:

                self.ui.line_password.setText(new_password)
                self.changed = True
                self.ui.btn_read.setDisabled(True)
                self.ui.btn_save.setDisabled(False)

        current_password = self.ui.line_password.text()
        if current_password:
            answer = QtWidgets.QMessageBox.question(self, "Генерация пароля",
                                                    f'Заменить существующий пароль "{current_password}" на новый?',
                                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                write_password()

            elif answer == QtWidgets.QMessageBox.No:
                return
        else:
            write_password()

    def btn_settings(self):
        window = generator.MyWin(self)
        window.show()

    def btn_exit_create(self):
        if self.changed:
            answer = QtWidgets.QMessageBox.question(self, "Редактирование карточки",
                                                    f'Сохранить изменения?',
                                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                self.btn_save()
            elif answer == QtWidgets.QMessageBox.No:
                self.editing = False
                self.changed = False

        self.editing = False
        self.changed = False
        self.load_cards()

    def btn_create(self):
        self.ui.line_find.clear()
        self.clear_all_line_edits()
        self.temp = ""

        self.create_mode()

    def btn_edit(self):
        self.editing = True
        self.changed = False
        self.set_mode()

    def btn_read(self):
        self.editing = False
        self.set_mode()

    def btn_save(self):
        temp = self.temp
        title = self.ui.line_title.text()
        link = self.ui.line_link.text()
        login = self.ui.line_login.text()
        password = self.ui.line_password.text()
        additionally = self.ui.text_additionally.toPlainText()

        if not title:                                                                                                   # 1 нет заголовка - вернуться к редактированию и установить иходное название
            QtWidgets.QMessageBox.warning(self, "Сохранение карточки", "Введите название карточки")
            self.ui.line_title.setText(self.temp)
            self.ui.line_title.setFocus()
            self.editing = True
            self.changed = True
            return

        data = title + link + login + password + additionally                                                           # если в строке поиск есть слово и если измененная карточка не попадает под фильтр, очистить фильтр
        filter = self.ui.line_find.text()
        if filter:
            if not filter in data:
                self.ui.line_find.clear()

        if title == self.temp:                                                                                          # 2 название осталось таким же - просто редактируем содержание
            edit_catd(source_dict, temp, title, link, login, password, additionally)
            self.editing = False
            self.changed = False
            self.load_cards()
            save_file(file_name)
            return

        else:

            if title in source_dict:                                                                                    # (?) название изменилось и карточка с таким именем уже существует. заменить?

                answer = QtWidgets.QMessageBox.question(self, "Сохранение карточки",
                                                        f'Карточка с именем "{title}" уже существует.\nЗаменить?',
                                                        QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:                                                                 # 3 ДА - заменяем карточку на новую
                    if self.mode == "creating":
                        add_new_card(source_dict, title, link, login, password, additionally)
                    else:
                        edit_catd(source_dict, temp, title, link, login, password, additionally)
                    self.editing = False
                    self.changed = False
                    self.temp = title
                    self.load_cards()
                    save_file(file_name)
                    return

                elif answer == QtWidgets.QMessageBox.No:                                                                # 4 НЕТ - вернуться к редактированию
                    self.ui.line_title.setText(self.temp)
                    self.ui.line_title.setFocus()
                    self.editing = True
                    self.changed = True
                    save_file(file_name)
                    return

            else:                                                                                                       # 5 карточки с таким названием нет - сохраняем эту с новым названием
                if self.mode == "creating":
                    add_new_card(source_dict, title, link, login, password, additionally)
                    save_file(file_name)

                else:
                    edit_catd(source_dict, temp, title, link, login, password, additionally)
                    save_file(file_name)
                self.editing = False
                self.changed = False
                self.temp = title
                self.load_cards()
                return

    def btn_delete(self):
        count_row = self.ui.listWidget.count() - 1

        if count_row == -1:
            QtWidgets.QMessageBox.warning(self, "Удаление карточки", "Выберите карточку для удаления")
            return

        current_row = self.ui.listWidget.currentRow()
        current_title = self.ui.listWidget.item(current_row).text()

        answer = QtWidgets.QMessageBox.question(self, "Удаление карточки",
                                                f'Вы действительно хотите удалить карточку с именем "{current_title}"?',
                                                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            delete_card(source_dict, current_title)

            if count_row == 0:
                self.temp = ""
            elif current_row == count_row:
                self.temp = self.ui.listWidget.item(current_row-1).text()
            elif current_row >= 0:
                self.temp = self.ui.listWidget.item(current_row+1).text()

            self.load_cards()
        else:
            return

####################################################################################
    # режимы (видимости/активация полей и кнопок)
    def set_mode(self):
        current_row = self.ui.listWidget.currentRow()
        if not source_dict:
            self.standby_mode()
            return
        elif current_row == -1:
            self.nobody_mode()
            return

        if self.editing:
            self.edit_mode()
            if self.changed:
                self.ui.btn_read.setDisabled(True)
                self.ui.btn_save.setDisabled(False)
            else:
                self.ui.btn_read.setDisabled(False)
                self.ui.btn_save.setDisabled(True)
        else:
            self.read_mode()

    def read_mode(self):
        self.mode = "reading"

        self.ui.listWidget.setDisabled(False)
        self.ui.label_list.setDisabled(False)

        self.ui.line_find.setDisabled(False)
        self.ui.line_title.setDisabled(False)
        self.ui.line_title.setReadOnly(True)
        self.ui.line_link.setDisabled(False)
        self.ui.line_link.setReadOnly(True)
        self.ui.line_login.setDisabled(False)
        self.ui.line_login.setReadOnly(True)
        self.ui.line_password.setDisabled(False)
        self.ui.line_password.setReadOnly(True)

        self.ui.text_additionally.setDisabled(False)
        self.ui.text_additionally.setReadOnly(True)

        self.ui.btn_exit_create.hide()
        self.ui.btn_create.setDisabled(False)
        self.ui.btn_read.setDisabled(True)
        self.ui.btn_edit.setDisabled(False)
        self.ui.btn_save.setDisabled(True)
        self.ui.btn_delete.setDisabled(False)
        self.ui.btn_generate.setDisabled(True)
        self.ui.btn_settings.setDisabled(True)

        self.ui.label_list.setDisabled(False)
        self.ui.label_title.setDisabled(False)
        self.ui.label_link.setDisabled(False)
        self.ui.label_login.setDisabled(False)
        self.ui.label_password.setDisabled(False)
        self.ui.label_additionally.setDisabled(False)

    def edit_mode(self):
        self.mode = "editing"

        self.ui.listWidget.setDisabled(True)
        self.ui.label_list.setDisabled(True)

        self.ui.line_find.setDisabled(True)
        self.ui.line_title.setDisabled(False)
        self.ui.line_title.setReadOnly(False)
        self.ui.line_link.setDisabled(False)
        self.ui.line_link.setReadOnly(False)
        self.ui.line_login.setDisabled(False)
        self.ui.line_login.setReadOnly(False)
        self.ui.line_password.setDisabled(False)
        self.ui.line_password.setReadOnly(False)

        self.ui.text_additionally.setDisabled(False)
        self.ui.text_additionally.setReadOnly(False)

        self.ui.btn_exit_create.show()
        self.ui.btn_create.setDisabled(True)
        self.ui.btn_read.setDisabled(False)
        self.ui.btn_edit.setDisabled(True)
        self.ui.btn_save.setDisabled(True)
        self.ui.btn_delete.setDisabled(True)
        self.ui.btn_generate.setDisabled(False)
        self.ui.btn_settings.setDisabled(False)

        self.ui.label_list.setDisabled(True)
        self.ui.label_title.setDisabled(False)
        self.ui.label_link.setDisabled(False)
        self.ui.label_login.setDisabled(False)
        self.ui.label_password.setDisabled(False)
        self.ui.label_additionally.setDisabled(False)

    def nobody_mode(self):
        self.mode = "nobody_mode"

        self.ui.listWidget.setDisabled(False)
        self.ui.label_list.setDisabled(False)

        self.ui.line_find.setDisabled(False)
        self.ui.line_title.setDisabled(True)
        self.ui.line_title.setReadOnly(True)

        self.ui.line_link.setDisabled(True)
        self.ui.line_link.setReadOnly(True)
        self.ui.line_login.setDisabled(True)
        self.ui.line_login.setReadOnly(True)
        self.ui.line_password.setDisabled(True)
        self.ui.line_password.setReadOnly(True)

        self.ui.text_additionally.setDisabled(True)
        self.ui.text_additionally.setReadOnly(True)

        self.ui.btn_exit_create.hide()
        self.ui.btn_create.setDisabled(True)
        self.ui.btn_read.setDisabled(True)
        self.ui.btn_edit.setDisabled(True)
        self.ui.btn_save.setDisabled(True)
        self.ui.btn_delete.setDisabled(True)
        self.ui.btn_generate.setDisabled(True)
        self.ui.btn_settings.setDisabled(True)

        self.ui.label_list.setDisabled(False)
        self.ui.label_title.setDisabled(True)
        self.ui.label_link.setDisabled(True)
        self.ui.label_login.setDisabled(True)
        self.ui.label_password.setDisabled(True)
        self.ui.label_additionally.setDisabled(True)

    def standby_mode(self):
        self.mode = "standby_mode"

        self.ui.listWidget.setDisabled(True)
        self.ui.label_list.setDisabled(True)

        self.ui.line_find.setDisabled(True)
        self.ui.line_title.setDisabled(True)
        self.ui.line_title.setReadOnly(True)

        self.ui.line_link.setDisabled(True)
        self.ui.line_link.setReadOnly(True)
        self.ui.line_login.setDisabled(True)
        self.ui.line_login.setReadOnly(True)
        self.ui.line_password.setDisabled(True)
        self.ui.line_password.setReadOnly(True)

        self.ui.text_additionally.setDisabled(True)
        self.ui.text_additionally.setReadOnly(True)

        self.ui.btn_exit_create.hide()
        self.ui.btn_create.setDisabled(False)
        self.ui.btn_read.setDisabled(True)
        self.ui.btn_edit.setDisabled(True)
        self.ui.btn_save.setDisabled(True)
        self.ui.btn_delete.setDisabled(True)
        self.ui.btn_generate.setDisabled(True)
        self.ui.btn_settings.setDisabled(True)

        self.ui.label_list.setDisabled(True)
        self.ui.label_title.setDisabled(True)
        self.ui.label_link.setDisabled(True)
        self.ui.label_login.setDisabled(True)
        self.ui.label_password.setDisabled(True)
        self.ui.label_additionally.setDisabled(True)

    def create_mode(self):
        self.mode = "creating"

        self.ui.listWidget.setDisabled(True)
        self.ui.label_list.setDisabled(True)

        self.ui.line_find.setDisabled(True)
        self.ui.line_title.setDisabled(False)
        self.ui.line_title.setReadOnly(False)

        self.ui.line_link.setDisabled(False)
        self.ui.line_link.setReadOnly(False)
        self.ui.line_login.setDisabled(False)
        self.ui.line_login.setReadOnly(False)
        self.ui.line_password.setDisabled(False)
        self.ui.line_password.setReadOnly(False)

        self.ui.text_additionally.setDisabled(False)
        self.ui.text_additionally.setReadOnly(False)

        self.ui.btn_exit_create.show()
        self.ui.btn_create.setDisabled(True)
        self.ui.btn_read.setDisabled(True)
        self.ui.btn_edit.setDisabled(True)
        self.ui.btn_save.setDisabled(True)
        self.ui.btn_delete.setDisabled(True)
        self.ui.btn_generate.setDisabled(False)
        self.ui.btn_settings.setDisabled(False)

        self.ui.label_list.setDisabled(True)
        self.ui.label_title.setDisabled(False)
        self.ui.label_link.setDisabled(False)
        self.ui.label_login.setDisabled(False)
        self.ui.label_password.setDisabled(False)
        self.ui.label_additionally.setDisabled(False)

    def monitoring(self):
        mode = {
            "standby_mode"  : "Карточек нет",
            "nobody_mode"   : "Карточка не выбрана",
            "creating"      : "Создание",
            "reading"       : "Чтение",
            "editing"       : "Редактирование"}

        self.ui.statusBar.showMessage(f'Режим: {mode[self.mode]} | temp: {self.temp} | Редактирование: {self.editing} | Изменён: {self.changed}', 10)

        text = ""
        for card, data in source_dict.items():
            text = text + f'<h5>{card}:</h5>\n{data[0]} | {data[1]} | {data[2]} | {data[3]}\n\n'

class modal_window(QtWidgets.QWidget):
    def __init__(self,parent=MyWin):
        super().__init__(parent,QtCore.Qt.Window)           # (parent) для того чтобы окно открывалось внутри существующего, (parent,QtCore.Qt.Window) чтобы открывалось отдельно
        self.modal = Ui_Form()
        self.modal.setupUi(self)
        self.setWindowModality(1)

        print(" modal", settings_dict)
        # Переменные
        self.attempt = 0
        self.wait = 0

        # таймер для мониторринга
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.waiting)

        # обработка событий
        self.modal.btn_enter.clicked.connect(self.enter_in_program)

    def enter_in_program(self):
        current_pass = self.modal.line_enter.text()

        if generator.correct_pass == current_pass:
            global access
            access = True
            self.hide()
            myapp.show()




        else:
            self.attempt += 1
            if self.attempt >= 3:
                self.attempt = 0
                self.wait = 0
                self.message_error()
                self.set_waiting_mode()
                self.timer.start(1000)
            else:
                self.message_error()
            self.modal.line_enter.clear()
            self.modal.line_enter.setFocus()

    def message_error(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Неправильный пароль")

    def set_waiting_mode(self):
        self.modal.line_enter.setDisabled(True)
        self.modal.btn_enter.setDisabled(True)
        self.modal.label_img.setDisabled(True)
        self.modal.label_enter.setDisabled(True)

        self.setCursor(QCursor(QtCore.Qt.WaitCursor))

    def return_enterring_mode(self):
        self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        self.modal.line_enter.setDisabled(False)
        self.modal.btn_enter.setDisabled(False)
        self.modal.label_img.setDisabled(False)
        self.modal.label_enter.setDisabled(False)

    def waiting(self):
        self.wait += 1
        if self.wait == 10:
            self.return_enterring_mode()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    if access:
        myapp.show()
    sys.exit(app.exec_())