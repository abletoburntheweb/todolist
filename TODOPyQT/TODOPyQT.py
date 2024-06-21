import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, \
    QMessageBox, QLineEdit, QListWidget, QListWidgetItem, QComboBox, QWidget
from PyQt5.QtCore import Qt
from note_page import NotePage
from HowToUse import HelpDialog
from daily_tasks_page import DailyTasksPage
from long_term_tasks_page import LongTermTasksPage
from text_wrapping import wrap_text
from styles import search_input_style, day_button_style, main_window_style, settings_style, \
    get_task_group_styles, add_tasks_button_style, tasks_button_style, results_list_style
from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setWindowIcon(QIcon('TODO List icon.ico'))
        self.setGeometry(750, 250, 500, 700)
        self._note_page = NotePage(self)
        self.buttons = []
        self.long_term_tasks = []
        self.daily_tasks = []

        self.current_button_index = 1

        self.daily_tasks_page = DailyTasksPage(self)
        self.long_term_tasks_page = LongTermTasksPage(self)

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
    MAX_TASK_LENGTH = 150

    def save_tasks_to_file(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks_data, file, ensure_ascii=False, indent=4)

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.completed_tasks_count = settings.get("completed_tasks_count", 0)
        except Exception as e:
            print(f"Ошибка при загрузке настроек: {e}")
            self.completed_tasks_count = 0

    def save_settings(self):
        settings = {
            "completed_tasks_count": self.completed_tasks_count
        }
        try:
            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Произошла ошибка при сохранении настроек: {e}')

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

    def style_search_input(self):
        self.search_input.setStyleSheet(search_input_style())

    def style_day_buttons(self, active_index=None):
        if active_index is not None:
            active_index = int(active_index)
        for index, btn in enumerate(self.buttons):
            btn.setStyleSheet(day_button_style(active=(index == active_index - 1)))

    def apply_main_window_style(self):
        self.setStyleSheet(main_window_style())

    def get_settings_style(self):
        return settings_style()

    def setup_main_buttons(self):
        button_width = 60
        button_height = 40
        button_spacing = 10

        total_width = (button_width * 7) + (button_spacing * (7 - 1))

        start_x = (self.width() - total_width) // 2  # центрирование кнопки
        start_y = 10

        self.buttons = []
        for i in range(1, 8):
            btn = QPushButton(f"{i}", self)  # Создание кнопки с номером дня
            x_position = start_x + (i - 1) * (button_width + button_spacing)

            btn.setGeometry(x_position, start_y, button_width, button_height)

            # Проверяем, активна ли кнопка, и применяем соответствующий стиль
            if i == self.current_button_index:
                active_style = day_button_style(active=True)
                btn.setStyleSheet(active_style)
            else:
                inactive_style = day_button_style(active=False)
                btn.setStyleSheet(inactive_style)

            btn.clicked.connect(
                lambda checked, index=i: self.handle_button_click(index))
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
        self.save_settings()

    def reset_completed_tasks_count(self):
        self.completed_tasks_count = 0
        self.update_completed_tasks_label()
        self.save_settings()

    def update_completed_tasks_label(self):
        self.completed_tasks_label.setText(f"Выполнено задач: {self.completed_tasks_count}")

    def handle_button_click(self, button_index):
        self.clear_window(keep_main_buttons=True, keep_labels=True)
        self.setFixedSize(500, 700)
        self.current_button_index = button_index

        button_tasks = self.tasks_data.get(str(button_index), {
            "important_tasks": [],
            "additional_tasks": [],
            "tasks_high_priority": [],
            "tasks_low_priority": []
        })

        self.style_day_buttons(active_index=button_index)

        self.text_high = QtWidgets.QLabel("Важные задачи", self)
        self.text_high.setGeometry(20, 100, 460, 40)

        self.text_low = QtWidgets.QLabel("Обычные задачи", self)
        self.text_low.setGeometry(20, 350, 460, 40)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, 340, 30)
        self.style_search_input()
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(370, 60, 100, 30)
        self.search_button.clicked.connect(lambda: self.search_tasks(button_index))
        self.search_button.show()


        self.daily_tasks_button = QPushButton("Ежедневные задачи", self)
        button_width = 180
        button_height = 40
        button_x = self.width() - button_width - 10  # Отступ от правого края
        button_y = self.height() - button_height - 70  # Отступ от нижнего края
        self.daily_tasks_button.setGeometry(button_x, button_y, button_width, button_height)
        self.daily_tasks_button.setStyleSheet(main_window_style())
        self.daily_tasks_button.clicked.connect(self.show_daily_tasks_page)
        self.daily_tasks_button.show()

        self.long_term_tasks_button = QPushButton("Долгосрочные задачи", self)
        button_width = 180
        button_height = 40
        button_x = self.width() - button_width - 195  # Отступ от правого края
        button_y = self.height() - button_height - 70  # Отступ от нижнего края
        self.long_term_tasks_button.setGeometry(button_x, button_y, button_width, button_height)
        self.long_term_tasks_button.setStyleSheet(main_window_style())
        self.long_term_tasks_button.clicked.connect(self.show_long_term_tasks_page)
        self.long_term_tasks_button.show()
        if button_index in range(1, 8):
            self.add_task_group(button_tasks["important_tasks"], 140, True, button_index)
            self.add_task_group(button_tasks["tasks_high_priority"], 190, True, button_index)
            self.add_task_group(button_tasks["additional_tasks"], 390, False, button_index)
            self.add_task_group(button_tasks["tasks_low_priority"], 440, False, button_index)
        else:
            self.main_screen()
        self.text_high.show()
        self.text_low.show()
        setup_ui_elements(self)

    def main_screen(self, button_index='1'):

        self.clear_window(keep_main_buttons=True)
        self.setFixedSize(500, 700)
        self.setup_main_buttons()

        self.apply_main_window_style()

        button_style = main_window_style()

        self.text_high = QtWidgets.QLabel("Важные задачи", self)
        self.text_high.setGeometry(20, 100, 460, 40)

        self.text_low = QtWidgets.QLabel("Обычные задачи", self)
        self.text_low.setGeometry(20, 350, 460, 40)

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
        self.add_task_group(button_tasks["additional_tasks"], 390, False, button_index)
        self.add_task_group(button_tasks["tasks_low_priority"], 440, False, button_index)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, 340, 30)
        self.style_search_input()
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(370, 60, 100, 30)
        self.search_button.clicked.connect(self.search_tasks)
        self.search_button.show()

        self.daily_tasks_button = QPushButton("Ежедневные задачи", self)
        button_width = 180
        button_height = 40
        button_x = self.width() - button_width - 10  # Отступ от правого края
        button_y = self.height() - button_height - 70  # Отступ от нижнего края
        self.daily_tasks_button.setGeometry(button_x, button_y, button_width, button_height)
        self.daily_tasks_button.setStyleSheet(main_window_style())
        self.daily_tasks_button.clicked.connect(self.show_daily_tasks_page)
        self.daily_tasks_button.show()

        self.long_term_tasks_button = QPushButton("Долгосрочные задачи", self)
        button_width = 180
        button_height = 40
        button_x = self.width() - button_width - 195  # Отступ от правого края
        button_y = self.height() - button_height - 70 # Отступ от нижнего края
        self.long_term_tasks_button.setGeometry(button_x, button_y, button_width, button_height)
        self.long_term_tasks_button.setStyleSheet(main_window_style())
        self.long_term_tasks_button.clicked.connect(self.show_long_term_tasks_page)
        self.long_term_tasks_button.show()

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

    def show_daily_tasks_page(self):
        self.clear_window()
        self.daily_tasks_page.setup_ui()
        setup_ui_elements(self)

    def show_long_term_tasks_page(self):
        self.clear_window()
        self.long_term_tasks_page.setup_ui()
        setup_ui_elements(self)

    def settings_page(self):
        self.clear_window()
        self.setFixedSize(500, 700)
        print("Кнопка 3")

        styles = self.get_settings_style()

        usage_label = QLabel("Как пользоваться:", self)
        usage_label.setGeometry(50, 50, 200, 30)
        usage_label.setStyleSheet(styles["label_style"])
        usage_label.show()

        help_button = QPushButton("Справка", self)
        help_button.setGeometry(250, 50, 200, 40)
        help_button.setStyleSheet(styles["button_style"])
        help_button.clicked.connect(self.show_help_dialog)
        help_button.show()

        self.completed_tasks_label = QLabel(f"Выполнено задач: {self.completed_tasks_count}", self)
        self.completed_tasks_label.setGeometry(50, 100, 400, 50)
        self.completed_tasks_label.setStyleSheet(styles["completed_tasks_label_style"])
        self.completed_tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.completed_tasks_label.show()

        reset_button_width = 200
        reset_button_height = 40
        right_margin = 20
        reset_button_x = self.width() - reset_button_width - right_margin
        reset_token_button_y = 160

        reset_button = QPushButton("Сбросить", self)
        reset_button.setGeometry(reset_button_x, reset_token_button_y, reset_button_width, reset_button_height)
        reset_button.setStyleSheet(styles["reset_button_style"])
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
        print("Вызван поиска")
        if button_index is None:
            button_index = self.current_button_index

        if hasattr(self, 'results_list') and self.results_list is not None:
            try:
                self.results_list.deleteLater()
            except RuntimeError:
                pass
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

        if search_results:

            self.clear_window(keep_main_buttons=True)
            self.show_search_results(search_results)
        else:
            QMessageBox.information(self, 'Поиск', 'Задачи с таким названием не найдены.')

    def search_button_clicked(self):
        try:
            self.search_tasks(self.current_button_index)
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при поиске: {e}')

    def show_search_results(self, search_results):
        print("Результаты поиска")
        self.search_button.hide()  # Скрываем кнопку "Поиск"
        self.results_list = QListWidget(self)
        self.results_list.setGeometry(20, 100, 460, 590)
        self.results_list.setStyleSheet(results_list_style())

        for day, category, task_name in search_results:

            for task in self.tasks_data[day][category]:
                if task['name'] == task_name:
                    completed_status = "Выполнено" if task.get('completed', False) else "Не выполнено"
                    priority = "Важная задача" if category in ["important_tasks",
                                                               "tasks_high_priority"] else "Обычная задача"
                    item_text = f"{day}: {task_name} - {priority} - {completed_status}"
                    item = QListWidgetItem(item_text)
                    self.results_list.addItem(item)
                    break
        self.results_list.itemClicked.connect(self.go_to_task_detail)
        self.results_list.show()

    def go_to_task_detail(self, item):
        print("Переход к результатам поиска")
        details = item.text().split(": ")
        day = details[0]
        task_name = details[1]
        # Сохраняем информацию о задаче перед очисткой окна
        self.selected_day = int(day)
        self.selected_task_name = task_name
        self.clear_window(keep_main_buttons=True)
        # Переходим к нужному дню, используя сохранённые значения
        self.handle_button_click(self.selected_day)

    def add_task_group(self, tasks, y_start, is_important, button_index):
        tasks_style = tasks_button_style()
        add_task_style = add_tasks_button_style()
        styles = get_task_group_styles()

        for i, task in enumerate(tasks):
            task_name = task['name']
            btn = QtWidgets.QPushButton(task_name, self)
            btn_width = 300 + 50
            btn.setGeometry(25, y_start + i * 50, btn_width, 40)
            checkbox_x = 330 + 50
            edit_btn_x = 360 + 50
            delete_btn_x = 400 + 50

            btn.setStyleSheet(add_task_style)

            if task_name not in ["Добавить важных дел", "Добавить дел"]:
                btn.clicked.connect(lambda _, name=task_name: self.show_task_full_title(name))
                btn.setEnabled(True)
                btn.setStyleSheet(tasks_style)

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setChecked(task.get('completed', False))
                checkbox.setGeometry(checkbox_x, y_start + i * 50 + 10, 20, 20)
                checkbox.setStyleSheet(styles["checkbox_style"])
                checkbox.toggled.connect(
                    lambda checked, t=task, b_index=button_index: self.toggle_task_completed(t, b_index, checked))
                checkbox.show()

                edit_btn = QtWidgets.QPushButton("✎", self)
                edit_btn.setGeometry(edit_btn_x, y_start + i * 50, 30, 30)
                edit_btn.setStyleSheet(styles["edit_button_style"])
                edit_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.edit_task(t, b_index))
                edit_btn.show()

                delete_btn = QtWidgets.QPushButton("✖", self)
                delete_btn.setGeometry(delete_btn_x, y_start + i * 50, 30, 30)
                delete_btn.setStyleSheet(styles["delete_button_style"])
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
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return

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
        print("Добавляем важную задачу...")
        button_index = int(button_index)
        text, ok = QInputDialog.getText(self, 'Добавить важных дел', 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            if len(self.tasks_data[str(button_index)]["tasks_high_priority"]) < self.MAX_TASKS_COUNT:
                new_task = {"name": text, "completed": False}
                self.tasks_data[str(button_index)]["tasks_high_priority"].append(new_task)
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три важных задачи!')

    def add_additional_task_input(self, button_index):
        print("Добавляем обычную задачу...")
        button_index = int(button_index)
        text, ok = QInputDialog.getText(self, 'Добавить дел', 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            if len(self.tasks_data[str(button_index)]["tasks_low_priority"]) < self.MAX_TASKS_COUNT:
                new_task = {"name": text, "completed": False}
                self.tasks_data[str(button_index)]["tasks_low_priority"].append(new_task)
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три дополнительные задачи!')

    def clear_window(self, keep_main_buttons=False, keep_labels=False):
        widgets_to_keep = [self.search_button] + self.buttons if keep_main_buttons else []
        if keep_labels:
            widgets_to_keep.extend([self.text_high, self.text_low])
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
