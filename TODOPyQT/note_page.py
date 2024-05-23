import json
from PyQt5.QtWidgets import QListWidget, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
from ui_elements import setup_ui_elements


class NotePage:
    def __init__(self, main_win):
        self.main_win = main_win
        self.sidebar_list_widget = QListWidget(main_win)
        self.sidebar_list_widget.itemClicked.connect(self.on_note_selected)
        self.note_title_edit = QLineEdit(main_win)
        self.notes_text_edit = QTextEdit(main_win)
        self.notes = {}
        self.load_notes_from_file()
        self.setup_note_page_ui()

    def setup_note_page_ui(self):
        self.sidebar_list_widget.setGeometry(10, 10, 150, 650)
        self.sidebar_list_widget.setStyleSheet("background-color: #F2FAFD;")
        self.load_note_titles()

        self.sidebar_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sidebar_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.note_title_edit.setGeometry(170, 10, 320, 30)
        self.note_title_edit.setPlaceholderText("Название заметки")

        self.notes_text_edit.setGeometry(170, 50, 320, 610)
        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")

        save_notes_button = QPushButton("Сохранить заметку", self.main_win)
        save_notes_button.setGeometry(340, 600, 150, 30)
        save_notes_button.clicked.connect(self.save_notes_to_file)

        delete_note_button = QPushButton("Удалить заметку", self.main_win)
        delete_note_button.setGeometry(190, 600, 150, 30)
        delete_note_button.clicked.connect(self.delete_current_note)

        new_note_button = QPushButton("Создать новую заметку", self.main_win)
        new_note_button.setGeometry(10, 600, 150, 30)
        new_note_button.clicked.connect(self.create_new_note)

        self.sidebar_list_widget.show()
        self.note_title_edit.show()
        self.notes_text_edit.show()
        save_notes_button.show()
        delete_note_button.show()
        new_note_button.show()
        setup_ui_elements(self.main_win)

    def load_notes_from_file(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                self.notes = json.load(file).get("notes", {})
        except FileNotFoundError:
            self.notes = {}
        except json.JSONDecodeError:
            QMessageBox.warning(self.main_win, 'Ошибка', 'The notes file is corrupted. Starting with an empty list.')
            self.notes = {}
        self.load_note_titles()

    def load_note_titles(self):
        self.sidebar_list_widget.clear()
        for note_title in sorted(self.notes.keys()):
            self.sidebar_list_widget.addItem(note_title)

    def on_note_selected(self, item):
        selected_note = item.text()
        self.note_title_edit.setText(selected_note)
        self.notes_text_edit.setText(self.notes[selected_note])

    def save_notes_to_file(self):
        print("Attempting to save the note...")
        title = self.note_title_edit.text().strip()
        content = self.notes_text_edit.toPlainText().strip()

        self.notes[title] = content

        try:
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)
            QMessageBox.information(self.main_win, 'Сохранено', 'Заметка сохранена.')
            self.load_note_titles()
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', f'Произошла ошибка при сохранении заметки: {e}')

    def delete_current_note(self):
        title = self.note_title_edit.text()
        if title in self.notes:
            reply = QMessageBox.question(self.main_win, 'Подтверждение удаления',
                                         f'Вы действительно хотите удалить заметку "{title}"?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                del self.notes[title]
                self.note_title_edit.clear()
                self.notes_text_edit.clear()
                self.load_note_titles()

                try:
                    with open("notes.json", "w", encoding="utf-8") as file:
                        json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)
                    QMessageBox.information(self.main_win, 'Удалено', 'Заметка успешно удалена.')
                except Exception as e:
                    QMessageBox.warning(self.main_win, 'Ошибка', f'Произошла ошибка при сохранении заметки: {e}')
        else:
            QMessageBox.warning(self.main_win, 'Ошибка', 'Выберите заметку для удаления.')

    def create_new_note(self):
        self.note_title_edit.clear()
        self.notes_text_edit.clear()
        self.note_title_edit.setFocus()

    def apply_font_size_style(self, font_size):
        self.notes_text_edit.setStyleSheet(f"font-size: {font_size}px;")

        self.note_title_edit.setStyleSheet(font_size_style)
        self.notes_text_edit.setStyleSheet(font_size_style)
        self.sidebar_list_widget.setStyleSheet("QListView { font-size: " + str(font_size) + "px; }")
