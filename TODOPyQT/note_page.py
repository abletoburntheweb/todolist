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
        # Определение стиля для кнопок
        button_style = """
            QPushButton {
                background-color: #6CA6CD;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #5B9BD5;
            }
            QPushButton:hover {
                background-color: #8DBDD8;
            }
        """
        self.note_title_edit.setPlaceholderText("Название заметки")
        self.note_title_edit.setGeometry(170, 10, 320, 30)
        # Стиль для боковой панели со списком заметок
        self.sidebar_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #F2FAFD;
                border: none;
                color: #333;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #89CFF0;
                color: black;
            }
        """)
        self.sidebar_list_widget.setGeometry(10, 10, 150, 650)
        # ... [остальные настройки виджета]
        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")
        self.notes_text_edit.setGeometry(170, 50, 320, 610)
        # Стиль для поля ввода названия заметки
        self.note_title_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #6CA6CD;
            }
        """)
        self.note_title_edit.setGeometry(170, 10, 320, 30)

        # Стиль для окна текста заметки
        self.notes_text_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
                color: #555;
            }
            QTextEdit:focus {
                border-color: #6CA6CD;
            }
        """)

        self.notes_text_edit.setGeometry(170, 50, 320, 610)
        # ... [остальные настройки QTextEdit]

        # Создание и стилизация кнопок с использованием определенного выше стиля
        save_notes_button = QPushButton("Сохранить заметку", self.main_win)
        save_notes_button.setStyleSheet(button_style)
        save_notes_button.setGeometry(340, 600, 150, 30)
        save_notes_button.clicked.connect(self.save_notes_to_file)

        delete_note_button = QPushButton("Удалить заметку", self.main_win)
        delete_note_button.setStyleSheet(button_style)
        delete_note_button.setGeometry(190, 600, 150, 30)
        delete_note_button.clicked.connect(self.delete_current_note)

        new_note_button = QPushButton("Создать заметку", self.main_win)
        new_note_button.setStyleSheet(button_style)
        new_note_button.setGeometry(10, 600, 150, 30)
        new_note_button.clicked.connect(self.create_new_note)

        # Отображаем виджеты
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
