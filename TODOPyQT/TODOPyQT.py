import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, QCheckBox, QMessageBox, \
    QLineEdit, QListWidget, QTextEdit, QListWidgetItem, QComboBox, QWidget
from PyQt5.QtCore import Qt
from note_page import NotePage
from HowToUse import HelpDialog
from text_wrapping import wrap_text
from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)
        self._note_page = NotePage(self)
        self.buttons = []
        self.long_term_tasks = []
        self.daily_tasks = []

        self.current_button_index = 1

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(370, 60, 100, 30)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.search_button.show()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.completed_tasks_count = 0
        self.load_settings()
        self.save_settings()
        self.setup_main_buttons()
        self.load_tasks()



        self.main_screen()

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
            self.important_tasks = tasks_data.get("important_tasks", [])
            self.additional_tasks = tasks_data.get("additional_tasks", [])
            self.tasks_high_priority = tasks_data.get("tasks_high_priority", [])
            self.tasks_low_priority = tasks_data.get("tasks_low_priority", [])

        with open("notes.json", "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            self.notes = notes_data.get("notes", {})

    MAX_TASKS_COUNT = 3
    MAX_TASK_LENGTH = 100

    def load_stylesheet(self):
        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())
    def save_tasks_to_file(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks_data, file, ensure_ascii=False, indent=4)

    def save_notes_to_file(self):
        title = self.note_title_edit.text()
        notes = self.notes_text_edit.toPlainText()
        if title:
            if title in self.notes:
                del self.notes[title]
                try:
                    with open("notes.json", "w", encoding="utf-8") as file:
                        json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)
                    QMessageBox.information(self, 'Сохранено', 'Заметка удалена')
                except Exception as e:
                    QMessageBox.warning(self, 'Сохранение не удалось',
                                        f"Произошла ошибка при сохранении заметки {str(e)}")
            else:
                QMessageBox.warning(self, 'Ошибка', 'Заметка не существует')
            self.clear_note_page()
        else:
            QMessageBox.warning(self, 'Внимание', 'Заголовок не может быть пустым.')

    def clear_note_page(self):
        self.note_title_edit.clear()
        self.notes_text_edit.clear()

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.completed_tasks_count = settings.get("completed_tasks_count", 0)
        except Exception as e:
            self.completed_tasks_count = 0

    def save_settings(self):
        settings = {
            "completed_tasks_count": self.completed_tasks_count
        }
        try:
            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)
        except IOError as e:
            QMessageBox.warning(self, 'Error', f'Произошла ошибка: {e}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Произошла ошибка: {e}')

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                self.tasks_data = json.load(file)
        except FileNotFoundError:
            self.tasks_data = {str(i): {
                "important_tasks": [],
                "additional_tasks": [],
                "tasks_high_priority": [],
                "tasks_low_priority": []
            } for i in range(1, 8)}

    def setup_main_buttons(self):
        button_width = 60
        button_height = 40
        button_spacing = 10

        total_width = (button_width * 7) + (button_spacing * (7 - 1))

        start_x = (self.width() - total_width) // 2  # Вычитание общей ширины из ширины окна и делим на два
        start_y = 10

        self.buttons = []
        for i in range(1, 8):
            btn = QPushButton(f"{i}", self)
            x_position = start_x + (i - 1) * (button_width + button_spacing)
            '''active_button_style = """
                        QPushButton {
                            background-color: #6495ED; /* Темно-синий цвет для активной кнопки */
                            color: white;
                            border-radius: 10px;
                            padding: 5px;
                            font-size: 16px;
                            border: none;
                        }
                    """ '''
            btn.setGeometry(x_position, start_y, button_width, button_height)
            btn.setStyleSheet("""
                   QPushButton {
                       background-color: #87CEFA; /* Светло-синий цвет */
                       border-radius: 10px; /* Скругление углов */
                       padding: 5px;
                       font-size: 16px;
                       border: 2px solid #1E90FF; /* Темно-синяя граница */
                   }
                   QPushButton:hover {
                       background-color: #B0E0E6; /* При наведении */
                   }
                   QPushButton:pressed {
                       background-color: #ADD8E6; /* При нажатии */
                   }
               """)
            btn.clicked.connect(lambda checked, index=i: self.handle_button_click(index))
            btn.show()
            self.buttons.append(btn)

    def toggle_task_completed(self, task, button_index, checked):
        task['completed'] = checked

        if task in self.tasks_data[str(button_index)]["important_tasks"]:
            category = "important_tasks"
        elif task in self.tasks_data[str(button_index)]["tasks_high_priority"]:
            category = "tasks_high_priority"
        elif task in self.tasks_data[str(button_index)]["additional_tasks"]:
            category = "additional_tasks"
        elif task in self.tasks_data[str(button_index)]["tasks_low_priority"]:
            category = "tasks_low_priority"
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось найти задачу в списках.')
            return

        for i, t in enumerate(self.tasks_data[str(button_index)][category]):
            if t['name'] == task['name']:
                self.tasks_data[str(button_index)][category][i]['completed'] = checked
                break
        if checked:
            self.completed_tasks_count += 1
        else:
            if self.completed_tasks_count > 0:
                self.completed_tasks_count -= 1

        self.save_tasks_to_file()

    def reset_completed_tasks_count(self):
        self.completed_tasks_count = 0
        self.update_completed_tasks_label()
        self.save_settings()

    def update_completed_tasks_label(self):
        self.completed_tasks_label.setText(f"Выполнено задач: {self.completed_tasks_count}")

    def handle_button_click(self, button_index):
        self.clear_window(keep_main_buttons=True)
        self.setFixedSize(500, 700)
        self.current_button_index = button_index

        button_tasks = self.tasks_data.get(str(button_index), {
            "important_tasks": [],
            "additional_tasks": [],
            "tasks_high_priority": [],
            "tasks_low_priority": []
        })

        self.setStyleSheet("""
                  
                   QPushButton {
                       font-size: 16px;
                       border-radius: 8px;
                       padding: 6px;
                       background-color: #2196F3; /* Синий цвет кнопок */
                       color: white; /* Белый цвет текста */
                   }
                   QPushButton:hover {
                       background-color: #64B5F6; /* Светло-синий цвет при наведении */
                   }
                   QPushButton:pressed {
                       background-color: #1E88E5; /* Темно-синий цвет при нажатии */
                   }
                   QLabel {
                       font-size: 18px;
                       color: #37474F; /* Цвет текста заголовков */
                   }
               """)
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, 340, 30)
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(370, 60, 100, 30)
        self.search_button.clicked.connect(lambda: self.search_tasks(button_index))  # Передаем индекс в слот
        self.search_button.show()

        self.text_high = QtWidgets.QLabel("Важные задачи", self)
        self.text_high.setGeometry(20, 80, 460, 40)

        self.text_low = QtWidgets.QLabel("Обычные задачи", self)
        self.text_low.setGeometry(20, 340, 460, 40)

        if button_index in range(1, 8):
            self.add_task_group(button_tasks["important_tasks"], 140, True, button_index)
            self.add_task_group(button_tasks["tasks_high_priority"], 190, True, button_index)
            self.add_task_group(button_tasks["additional_tasks"], 420, False, button_index)
            self.add_task_group(button_tasks["tasks_low_priority"], 470, False, button_index)
        else:
            self.main_screen()
        self.text_high.show()
        self.text_low.show()
        setup_ui_elements(self)

    def main_screen(self, button_index='1'):
        self.clear_window(keep_main_buttons=True)
        self.setFixedSize(500, 700)
        self.setup_main_buttons()

        # Стили для главного окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ECEFF1; /* Светло-серый фон всего окна */
            }
            QPushButton {
                font-size: 16px;
                border-radius: 8px;
                padding: 6px;
                background-color: #2196F3; /* Синий цвет кнопок */
                color: white; /* Белый цвет текста */
            }
            QPushButton:hover {
                background-color: #64B5F6; /* Светло-синий цвет при наведении */
            }
            QPushButton:pressed {
                background-color: #1E88E5; /* Темно-синий цвет при нажатии */
            }
            QLabel {
                font-size: 18px;
                color: #37474F; /* Цвет текста заголовков */
            }
        """)

        self.text_high = QtWidgets.QLabel("Важные задачи", self)
        self.text_high.setGeometry(20, 80, 460, 40)

        self.text_low = QtWidgets.QLabel("Обычные задачи", self)
        self.text_low.setGeometry(20, 340, 460, 40)

        # Получение и отображение задач
        button_tasks = self.tasks_data.get(str(button_index), {
            "important_tasks": [],
            "additional_tasks": [],
            "tasks_high_priority": [],
            "tasks_low_priority": []
        })

        # Отображение задач
        self.add_task_group(button_tasks["important_tasks"], 140, True, button_index)
        self.add_task_group(button_tasks["tasks_high_priority"], 190, True, button_index)
        self.add_task_group(button_tasks["additional_tasks"], 420, False, button_index)
        self.add_task_group(button_tasks["tasks_low_priority"], 470, False, button_index)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, 340, 30)
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(370, 60, 100, 30)
        self.search_button.clicked.connect(self.search_tasks)
        self.search_button.show()

        # Показываем созданные элементы
        self.text_high.show()
        self.text_low.show()
        setup_ui_elements(self)

    def main_page(self):
        print("Кнопка 1")
        self.clear_window()
        self.setFixedSize(500, 700)
        self.main_screen()
        setup_ui_elements(self)

    def show_note_page(self, selected_note=None):
        try:
            print("Кнопка 2")
            self.clear_window()
            self._note_page = NotePage(self)
            self._note_page.note_title_edit.setText(selected_note or "")
            self._note_page.notes_text_edit.setText(self.notes.get(selected_note, ""))
            self._note_page.setup_note_page_ui()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при показе страницы заметок: {e}')

    def settings_page(self):
        self.clear_window()
        self.setFixedSize(500, 700)
        print("Кнопка 3")

        label_style = """
               QLabel {
                   font-size: 16px;
                   color: #333;
                   padding: 5px;
               }
           """ """
               QPushButton {
                   background-color: #5CACEE;
                   color: white;
                   border-radius: 6px;
                   padding: 8px;
                   font-size: 14px;
                   border: 1px solid #5CACEE;
                   min-width: 80px;
               }
               QPushButton:hover {
                   background-color: #1E90FF;
               }
               QPushButton:pressed {
                   background-color: #4682B4;
               }
           """
        usage_label = QLabel("Как пользоваться:", self)
        usage_label.setGeometry(50, 50, 200, 30)
        usage_label.setStyleSheet(label_style)
        usage_label.show()

        help_button = QPushButton("Справка", self)
        help_button.setGeometry(250, 50, 200, 40)
        help_button.setStyleSheet("""
                   QPushButton {
                       background-color: #5CACEE;
                       color: white;
                       border-radius: 6px;
                       padding: 5px;  
                       font-size: 14px;  
                       border: 1px solid #5CACEE;
                       min-width: 80px;
                   }
                   QPushButton:hover {
                       background-color: #1E90FF;
                   }
                   QPushButton:pressed {
                       background-color: #4682B4;
                   }
               """)
        help_button.clicked.connect(self.show_help_dialog)
        help_button.show()
        completed_tasks_label_style = """
                    QLabel {
                        font-size: 18px;
                        color: #2e8b57; 
                        padding: 5px;
                        border: 2px solid #2e8b57; 
                        border-radius: 8px; 
                        margin-top: 20px; 
                        background-color: #d9ecd0; 
                    }
                """
        self.completed_tasks_label = QLabel(f"Выполнено задач: {self.completed_tasks_count}", self)
        self.completed_tasks_label.setGeometry(50, 100, 400, 50)
        self.completed_tasks_label.setStyleSheet(completed_tasks_label_style)
        self.completed_tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.completed_tasks_label.show()

        reset_button_width = 200
        reset_button_height = 40
        right_margin = 20

        reset_button_x = self.width() - reset_button_width - right_margin
        reset_button_y = 160

        reset_button = QPushButton("Сбросить", self)
        reset_button.setGeometry(reset_button_x, reset_button_y, reset_button_width, reset_button_height)
        reset_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF6347;
                    color: white;
                    border-radius: 6px;
                    padding: 5px;
                    font-size: 12px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #FF4500;
                }
                QPushButton:pressed {
                    background-color: #CD5C5C;
                }
            """)
        reset_button.clicked.connect(self.reset_completed_tasks_count)
        reset_button.show()

        setup_ui_elements(self)

    def show_help_dialog(self):
        try:
            print("Справка")
            help_dialog = HelpDialog(self)
            help_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'При попытке открыть справку произошла ошибка: {e}')
            print(f'Ошибка: {e}')

    def show_task_full_title(self, task_name):
        wrapped_task_name = wrap_text(task_name, 25)
        QMessageBox.information(self, 'Полное название задачи', wrapped_task_name)

    def search_tasks(self, button_index=None):
        print("Вызван метод search_tasks")
        if button_index is None:
            button_index = self.current_button_index

        if hasattr(self, 'results_list') and self.results_list is not None:
            try:
                self.results_list.clear()
                self.results_list.deleteLater()
            except RuntimeError as e:
                print('')
                self.results_list = None

        search_text = self.search_input.text().lower()
        if len(search_text.strip()) < 3:
            QMessageBox.information(self, 'Поиск', 'Введите минимум 3 символа для поиска.')
            return

        search_results = []
        for day, tasks in self.tasks_data.items():
            for category in ['important_tasks', 'tasks_high_priority', 'additional_tasks', 'tasks_low_priority']:
                for task in tasks[category]:
                    if search_text in task['name'].lower():
                        search_results.append((day, category, task['name']))

        # Очищаем предыдущие результаты поиска
        self.clear_window(keep_main_buttons=True)

        if search_results:
            self.show_search_results(search_results)
        else:
            QMessageBox.information(self, 'Поиск', 'Задачи не найдены.')

    def search_button_clicked(self):
        try:
            self.search_tasks(self.current_button_index)
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при поиске: {e}')

    def show_search_results(self, search_results):
        print("Показываем результаты поиска")
        self.results_list = QListWidget(self)
        self.results_list.setGeometry(20, 100, 460, 590)

        for day, category, task_name in search_results:
            item = QListWidgetItem(f"{day}: {task_name}")
            self.results_list.addItem(item)

        self.results_list.itemClicked.connect(self.go_to_task_detail)

        self.results_list.show()

    def go_to_task_detail(self, item):
        print("Переход к деталям задачи")
        details = item.text().split(": ")
        day = details[0]
        task_name = details[1]

        self.clear_window(keep_main_buttons=True)
        self.handle_button_click(int(day))
    def add_task_group(self, tasks, y_start, is_important, button_index):
        edit_button_style = """
                  QPushButton {
                      background-color: #FFEB3B;
                      border-radius: 15px;
                  }
                  QPushButton:hover {
                      background-color: #FDD835;
                  }
              """

        delete_button_style = """
                  QPushButton {
                      background-color: #F44336;
                      border-radius: 15px;
                  }
                  QPushButton:hover {
                      background-color: #E53935;
                  }
              """

        checkbox_style = """
                  QCheckBox::indicator {
                      width: 20px;
                      height: 20px;
                  }
                  QCheckBox::indicator:checked {
                      background-color: #22a4f5;
                  }
              """

        for i, task in enumerate(tasks):
            task_name = task['name']
            btn = QtWidgets.QPushButton(task_name, self)
            btn.setGeometry(25, y_start + i * 50, 300, 40)

            # Установка стилей для кнопок задачи
            btn.setStyleSheet("""
                            QPushButton {
                                background-color: #84cdfa;
                                text-align: left;
                                padding-left: 10px;
                                border-radius: 15px;
                            }
                            QPushButton:hover {
                                background-color: #ADD8E6;
                            }
                        """)

            # Подключаем функцию show_task_full_title только если это не специальная кнопка
            if task_name not in ["Добавить важных дел", "Добавить дел"]:
                btn.clicked.connect(lambda _, name=task_name: self.show_task_full_title(name))
                btn.setEnabled(True)
                btn.setStyleSheet("""
                            QPushButton {
                                text-align: left;
                                padding-left: 10px;
                                border-radius: 15px;
                            }
                            QPushButton:hover {
                                background-color: #ADD8E6;
                            }
                        """)

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setChecked(task.get('completed', False))
                checkbox.setGeometry(330, y_start + i * 50 + 10, 20, 20)
                checkbox.setStyleSheet(checkbox_style)
                checkbox.toggled.connect(
                    lambda checked, t=task, b_index=button_index: self.toggle_task_completed(t, b_index, checked))
                checkbox.show()

                edit_btn = QtWidgets.QPushButton("✎", self)
                edit_btn.setGeometry(360, y_start + i * 50, 30, 30)
                edit_btn.setStyleSheet(edit_button_style)
                edit_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.edit_task(t, b_index))
                edit_btn.show()

                delete_btn = QtWidgets.QPushButton("✖", self)
                delete_btn.setGeometry(400, y_start + i * 50, 30, 30)
                delete_btn.setStyleSheet(delete_button_style)
                delete_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.delete_task(t, b_index))
                delete_btn.show()
            else:
                btn.setEnabled(True)
                if task_name == "Добавить важных дел":
                    btn.clicked.connect(lambda _, b_index=button_index: self.add_important_task_input(b_index))
                else:
                    btn.clicked.connect(lambda _, b_index=button_index: self.add_additional_task_input(b_index))

            btn.show()

    def edit_task(self, task, button_index):
        new_name, ok = QInputDialog.getText(self, 'Редактировать задачу', 'Введите новое название задачи:',
                                            text=task['name'])
        if ok and new_name:
            if len(new_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 100 символов.')
                return
            # Обновляем название задачи в данных
            task['name'] = new_name
            self.save_tasks_to_file()
            self.handle_button_click(button_index)

    def delete_task(self, task, button_index):
        try:
            category = None
            for cat in ["important_tasks", "tasks_high_priority", "additional_tasks", "tasks_low_priority"]:
                for t in self.tasks_data[str(button_index)][cat]:
                    if t['name'] == task['name']:
                        category = cat
                        break
                if category:
                    break

            if category:
                self.tasks_data[str(button_index)][category] = [
                    t for t in self.tasks_data[str(button_index)][category] if t['name'] != task['name']
                ]
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.warning(self, 'Ошибка', 'Задача не найдена для удаления.')

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при удалении задачи: {e}')

    def add_important_task_input(self, button_index):
        text, ok = QInputDialog.getText(self, 'Добавить важных дел', 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 100 символов.')
                return
            if len(self.tasks_data[str(button_index)]["tasks_high_priority"]) < self.MAX_TASKS_COUNT:
                new_task = {"name": text, "completed": False}
                self.tasks_data[str(button_index)]["tasks_high_priority"].append(new_task)
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три важных задачи!')

    def add_additional_task_input(self, button_index):
        text, ok = QInputDialog.getText(self, 'Добавить дел', 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 100 символов.')
                return
            if len(self.tasks_data[str(button_index)]["tasks_low_priority"]) < self.MAX_TASKS_COUNT:
                new_task = {"name": text, "completed": False}
                self.tasks_data[str(button_index)]["tasks_low_priority"].append(new_task)
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три дополнительные задачи!')

    def clear_window(self, keep_main_buttons=False):
        widgets_to_keep = self.buttons if keep_main_buttons else []
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget not in widgets_to_keep:
                widget.deleteLater()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Q:
            self.clear_window()
            self.main_page()
        elif event.key() == Qt.Key_W:
            self.clear_window()
            NotePage(self)
        elif event.key() == Qt.Key_E:
            self.clear_window()
            self.settings_page()


def run_app():
    try:
        app = QApplication([])
        window = MainWin()
        window.show()
        app.exec_()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    run_app()
