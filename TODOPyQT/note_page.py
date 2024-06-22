import json
from PyQt5.QtWidgets import QListWidget, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
from styles import sidebar_list_widget_style, notes_button_style, notes_title_edit_style, notes_text_edit_style
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
        self.note_title_edit.setPlaceholderText("Название заметки")
        self.note_title_edit.setGeometry(170, 10, 320, 30)

        self.sidebar_list_widget.setStyleSheet(sidebar_list_widget_style())
        self.sidebar_list_widget.setGeometry(10, 10, 150, 550)
        self.sidebar_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sidebar_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")
        self.notes_text_edit.setGeometry(170, 50, 320, 510)

        self.note_title_edit.setStyleSheet(notes_title_edit_style())
        self.note_title_edit.setGeometry(170, 10, 320, 30)

        self.notes_text_edit.setStyleSheet(notes_text_edit_style())
        self.notes_text_edit.setGeometry(170, 50, 320, 510)

        save_notes_button = QPushButton("Сохранить заметку", self.main_win)
        save_notes_button.setStyleSheet(notes_button_style())
        save_notes_button.setGeometry(340, 600, 150, 30)
        save_notes_button.clicked.connect(self.save_notes_to_file)

        delete_note_button = QPushButton("Удалить заметку", self.main_win)
        delete_note_button.setStyleSheet(notes_button_style())
        delete_note_button.setGeometry(190, 600, 150, 30)
        delete_note_button.clicked.connect(self.delete_current_note)

        new_note_button = QPushButton("Создать заметку", self.main_win)
        new_note_button.setStyleSheet(notes_button_style())
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
            QMessageBox.warning(self.main_win, 'Ошибка', 'Файл поврежден. Начинаем с пустого списка.')
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
        print("Сохранение заметки...")
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
        print("Удаление заметки...")
        title = self.note_title_edit.text()
        if title in self.notes:
            msg_box = QMessageBox(self.main_win)
            msg_box.setWindowTitle('Подтверждение удаления')
            msg_box.setText(f'Вы действительно хотите удалить заметку "{title}"?')
            yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
            no_button = msg_box.addButton("Нет", QMessageBox.NoRole)

            msg_box.exec_()

            if msg_box.clickedButton() == yes_button:
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