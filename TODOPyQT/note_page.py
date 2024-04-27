import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget, QTextEdit, QListWidgetItem, QLineEdit, QPushButton, QMessageBox
from ui_elements import setup_ui_elements

class NotePage:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.sidebar_list_widget = QListWidget(self.parent)
        self.sidebar_list_widget.setGeometry(10, 10, 150, 650)
        self.sidebar_list_widget.setStyleSheet("background-color: #F2FAFD;")
        self.sidebar_list_widget.show()

        self.note_title_edit = QLineEdit(self.parent)
        self.note_title_edit.setGeometry(170, 10, 320, 30)
        self.note_title_edit.setPlaceholderText("Название заметки")
        self.note_title_edit.show()

        self.notes_text_edit = QTextEdit(self.parent)
        self.notes_text_edit.setGeometry(170, 50, 320, 610)
        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")
        self.notes_text_edit.show()

        save_notes_button = QPushButton("Сохранить заметку", self.parent)
        save_notes_button.setGeometry(340, 600, 150, 30)
        save_notes_button.clicked.connect(self.parent.save_notes_to_file)
        save_notes_button.show()

        delete_note_button = QPushButton("Удалить заметку", self.parent)
        delete_note_button.setGeometry(190, 600, 150, 30)
        delete_note_button.clicked.connect(self.parent.delete_current_note)
        delete_note_button.show()

        self.add_new_note_button()
        self.load_note_titles()

    def add_new_note_button(self):
        new_note_button = QPushButton("Создать новую заметку", self.parent)
        new_note_button.setGeometry(10, 600, 150, 30)
        new_note_button.clicked.connect(self.parent.create_new_note)
        new_note_button.show()

    def load_note_titles(self):
        self.sidebar_list_widget.clear()
        for note in self.parent.notes.keys():
            item = QListWidgetItem(note)
            self.sidebar_list_widget.addItem(item)
        self.sidebar_list_widget.itemClicked.connect(self.parent.on_note_selected)