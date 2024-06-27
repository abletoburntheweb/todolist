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
        self.load_notes_from_file()
        self.setup_note_page_ui()

    def setup_note_page_ui(self):
        sidebar_width = 200
        sidebar_height = self.main_win.height() - 130
        note_edit_width = self.main_win.width() - sidebar_width - 40
        note_edit_height = self.main_win.height() - 170
        button_width = 180
        right_padding = 5
        button_height = 40
        button_spacing = 5

        self.sidebar_list_widget.setGeometry(10, 10, sidebar_width, sidebar_height)
        self.sidebar_list_widget.setStyleSheet(sidebar_list_widget_style())

        self.note_title_edit.setGeometry(sidebar_width + 20, 10, note_edit_width, 30)
        self.note_title_edit.setStyleSheet(notes_title_edit_style())

        self.notes_text_edit.setGeometry(sidebar_width + 20, 50, note_edit_width, note_edit_height)
        self.notes_text_edit.setStyleSheet(notes_text_edit_style())

        buttons_y_position = self.main_win.height() - button_height - 70

        new_note_button = QPushButton("Создать заметку", self.main_win)
        new_note_button.setGeometry(10, buttons_y_position, button_width, button_height)
        new_note_button.setStyleSheet(notes_button_style())
        new_note_button.clicked.connect(self.create_new_note)

        delete_note_button = QPushButton("Удалить заметку", self.main_win)

        delete_note_button.setGeometry(self.main_win.width() - button_width * 2 - button_spacing - right_padding,
                                       buttons_y_position, button_width, button_height)
        delete_note_button.setStyleSheet(notes_button_style())
        delete_note_button.clicked.connect(self.delete_current_note)

        save_notes_button = QPushButton("Сохранить заметку", self.main_win)
        save_notes_button.setGeometry(self.main_win.width() - button_width - right_padding,
                                      buttons_y_position, button_width, button_height)
        save_notes_button.setStyleSheet(notes_button_style())
        save_notes_button.clicked.connect(self.save_notes_to_file)

        self.sidebar_list_widget.show()
        self.note_title_edit.show()
        self.notes_text_edit.show()
        new_note_button.show()
        delete_note_button.show()
        save_notes_button.show()
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