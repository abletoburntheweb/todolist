import json
import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, \
    QMessageBox, QLineEdit, QListWidget, QListWidgetItem, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt
from note_page import NotePage
from HowToUse import HelpDialog
from text_wrapping import wrap_text
from styles import search_input_style, day_button_style, main_window_style, settings_style, \
    get_task_group_styles, add_tasks_button_style, tasks_button_style, results_list_style, add_daily_tasks_button_style, \
    daily_task_button_style
from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setWindowIcon(QIcon('TODO List icon.ico'))
        self.setGeometry(100, 100, 1280, 720)

        self.current_button_index = 1

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.completed_tasks_count = 0
        self.load_settings()
        self.save_settings()

        self.load_tasks()
        self.scroll_area = None

        self.main_screen()

        with open("notes.json", "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            self.notes = notes_data.get("notes", {})

    MAX_TASKS_COUNT = 90
    MAX_TASK_LENGTH = 450

    def save_tasks_to_file(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks_data, file, ensure_ascii=False, indent=4)

    def load_settings(self):
        with open("settings.json", "r", encoding="utf-8") as file:
            settings = json.load(file)
            self.completed_tasks_count = settings.get("completed_tasks_count", 0)

    def save_settings(self):
        settings = {
            "completed_tasks_count": self.completed_tasks_count
        }
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                self.tasks_data = json.load(file)
        except FileNotFoundError:
            self.tasks_data = {str(i): {"tasks": []} for i in range(1, 8)}
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Файл поврежден. Начинаем с пустого списка.')
            self.tasks_data = {str(i): {"tasks": []} for i in range(1, 8)}

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

    def toggle_task_completed(self, task, button_index, checked):
        task['completed'] = checked
        for day, tasks_info in self.tasks_data.items():
            if day == str(button_index):
                tasks = tasks_info["tasks"]
                for t in tasks:
                    if t['name'] == task['name']:
                        t['completed'] = checked
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
        self.main_screen(button_index)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def recreate_task_scroll_area(self):
        if self.scroll_area is not None:
            self.scroll_area.deleteLater()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(20, 140, self.width() - 40, 500)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        tasks_widget = QWidget()
        tasks_layout = QVBoxLayout(tasks_widget)
        tasks_widget.setLayout(tasks_layout)

        self.scroll_area.setWidget(tasks_widget)

        return tasks_layout

    def main_screen(self):
        print("Основной экран")

        if hasattr(self, 'scroll_area') and self.scroll_area is not None:
            try:
                print("Скрываем область с задачами")
                self.scroll_area.hide()
            except RuntimeError:
                self.scroll_area = None
                print("Область с задачами была удалена")

        self.setFixedSize(1280, 720)
        self.apply_main_window_style()

        if not hasattr(self, 'scroll_area') or self.scroll_area is None:
            self.scroll_area = QScrollArea(self)
            scroll_area_x = 20
            scroll_area_y = 180
            scroll_area_width = self.width() - 40
            scroll_area_height = self.height() - scroll_area_y - 100

            self.scroll_area.setGeometry(scroll_area_x, scroll_area_y, scroll_area_width, scroll_area_height)
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            print("Область с задачами уже существует")

        tasks_widget = QWidget()
        layout = QVBoxLayout(tasks_widget)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 20, self.width() - 150, 30)
        self.style_search_input()
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(self.width() - 120, 20, 100, 30)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.search_button.show()

        self.add_task_button = QPushButton("Добавить задачу", self)
        self.add_task_button.setGeometry(20, 70, 180, 40)
        self.add_task_button.setStyleSheet(add_tasks_button_style())
        self.add_task_button.clicked.connect(self.add_new_task)
        self.add_task_button.show()

        self.add_daily_task_button = QPushButton("Добавить ежедневную задачу", self)
        self.add_daily_task_button.setGeometry(220, 70, 250, 40)
        self.add_daily_task_button.setStyleSheet(add_daily_tasks_button_style())
        self.add_daily_task_button.clicked.connect(self.add_new_daily_task)
        self.add_daily_task_button.show()

        self.choose_month_button = QPushButton("Выбрать месяц", self)
        self.choose_month_button.setGeometry(self.width() - 220, self.height() - 110, 200, 40)
        self.choose_month_button.clicked.connect(self.show_month_selector)
        self.choose_month_button.show()

        button_tasks = self.tasks_data.get(str(self.current_button_index), {"tasks": []})
        self.add_tasks_to_layout(layout, button_tasks["tasks"], None, self.current_button_index)

        self.scroll_area.setWidget(tasks_widget)
        self.scroll_area.move((self.width() - self.scroll_area.width()) // 2, 160)

        print("Показываем область с задачами")
        self.scroll_area.show()

        setup_ui_elements(self)
        print("Настройка UI завершена")

    def main_page(self):
        print("Кнопка 1")
        self.clear_window()
        self.setFixedSize(1280, 720)
        self.main_screen()
        setup_ui_elements(self)

    def show_note_page(self, selected_note=None):
        try:
            print("Кнопка 2: Переход на страницу заметок")
            print("Очищаем окно")
            self.clear_window()

            print("Создаем страницу заметок")
            self._note_page = NotePage(self)

            if selected_note:
                print(f"Устанавливаем заголовок заметки: {selected_note}")
                self._note_page.note_title_edit.setText(selected_note)
                note_text = self.notes.get(selected_note, "")
                print(f"Устанавливаем текст заметки: {note_text}")
                self._note_page.notes_text_edit.setText(note_text)
            else:
                print("Нет выбранной заметки, оставляем заголовок и текст пустыми")
                self._note_page.note_title_edit.setText("")
                self._note_page.notes_text_edit.setText("")

            print("Настраиваем UI страницы заметок")
            self._note_page.setup_note_page_ui()
            print("Страница заметок успешно показана")
        except Exception as e:
            error_message = f"Произошла ошибка при показе страницы заметок: {e}"
            print(error_message)
            QMessageBox.warning(self, 'Ошибка', error_message)

    def settings_page(self):
        self.clear_window()
        self.setFixedSize(1280, 720)
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
        print("Справка")
        help_dialog = HelpDialog(self)
        help_dialog.exec_()

    def show_task_full_title(self, task_name):
        wrapped_task_name = wrap_text(task_name, 100)
        QMessageBox.information(self, 'Полное название задачи', wrapped_task_name)

    def search_tasks(self, button_index=None):
        try:
            print("Вызван поиск")

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
            for day, tasks_info in self.tasks_data.items():
                tasks = tasks_info.get("tasks", [])
                for task in tasks:
                    if search_text in task['name'].lower():
                        search_results.append((day, task['name']))

            if search_results:
                self.clear_window(keep_main_buttons=True)
                self.show_search_results(search_results)
            else:
                QMessageBox.information(self, 'Поиск', 'Задачи с таким названием не найдены.')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при поиске: {e}')

    def search_button_clicked(self):
        try:
            self.search_tasks(self.current_button_index)
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при поиске: {e}')

    def show_search_results(self, search_results):
        print("Результаты поиска")
        self.search_button.hide()
        self.results_list = QListWidget(self)
        self.results_list.setGeometry(20, 100, 460, 590)
        self.results_list.setStyleSheet(results_list_style())

        for day, task_name in search_results:
            tasks = self.tasks_data[day]["tasks"]
            for task in tasks:
                if task['name'] == task_name:
                    completed_status = "Выполнено" if task.get('completed', False) else "Не выполнено"
                    priority = "Важная задача" if task.get('priority', False) else "Обычная задача"
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

        self.selected_day = int(day)
        self.selected_task_name = task_name
        self.clear_window(keep_main_buttons=True)

        self.handle_button_click(self.selected_day)

    def show_month_selector(self):
        month_counts = self.calculate_task_counts_per_month()

        self.month_dialog = QDialog(self)
        self.month_dialog.setWindowTitle("Выбрать месяц")
        layout = QVBoxLayout(self.month_dialog)

        month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                       'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        for i, count in enumerate(month_counts, start=1):
            month_button = QPushButton(f"{month_names[i - 1]}: {count} задач")
            month_button.clicked.connect(lambda checked, month=i: self.show_tasks_by_month(month))
            layout.addWidget(month_button)

        self.month_dialog.setLayout(layout)
        self.month_dialog.exec_()

    def calculate_task_counts_per_month(self):
        month_counts = [0] * 12

        for tasks_info in self.tasks_data.values():
            for task in tasks_info["tasks"]:
                task_date = task.get('date')
                if task_date:
                    month = datetime.datetime.fromisoformat(task_date).month
                    month_counts[month - 1] += 1

        return month_counts

    def show_tasks_by_month(self, month):
        self.month_dialog.accept()
        tasks_layout = self.recreate_task_scroll_area()

        tasks_for_month = []
        for day, day_tasks in self.tasks_data.items():
            for task in day_tasks["tasks"]:
                task_date = task.get('date')
                if task_date and datetime.datetime.strptime(task_date, '%Y-%m-%d').month == month:
                    tasks_for_month.append(task)
        if tasks_for_month:
            self.add_tasks_to_layout(tasks_layout, tasks_for_month, None, self.current_button_index)

            self.choose_month_button.hide()
        else:

            QMessageBox.information(self, 'Задачи', 'На этот месяц задач нет.')

        self.scroll_area.show()

    def add_new_task(self):
        text, ok = QInputDialog.getText(self, 'Добавить задачу', 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 450 символов.')
                return

            date, ok = QInputDialog.getText(self, 'Добавить дату', 'Введите дату в формате ДД.ММ.ГГ:')
            if not ok or not date:
                return

            try:

                task_date = datetime.datetime.strptime(date, '%d.%m.%y').date()
                iso_date = task_date.isoformat()
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте ДД.ММ.ГГ.')
                return

            new_task = {"name": text, "completed": False, "date": iso_date}
            self.tasks_data[str(self.current_button_index)]["tasks"].append(new_task)
            self.save_tasks_to_file()
            self.update_task_layout()
            self.scroll_area.show()

    def handle_button_click(self, button_index=None):
        self.main_screen()

    def add_tasks_to_layout(self, layout, tasks, is_important, button_index):
        tasks_style = tasks_button_style()
        daily_tasks_style = daily_task_button_style()
        styles = get_task_group_styles()

        for task in tasks:
            task_name = task['name']
            task_date = task.get('date', '')


            if task_date:
                try:
                    formatted_date = datetime.datetime.strptime(task_date, '%Y-%m-%d').strftime('%d.%m.%y')
                except ValueError:
                    formatted_date = 'Неверный формат даты'
            else:
                formatted_date = 'Нет даты'

            task_widget = QWidget(self)
            task_layout = QHBoxLayout(task_widget)

            btn_style = daily_tasks_style if task.get('daily', False) else tasks_style

            btn = QtWidgets.QPushButton(f"{task_name} ({formatted_date})", self)
            btn.setStyleSheet(btn_style)
            btn.setFixedSize(800, 50)
            btn.clicked.connect(lambda _, name=task_name: self.show_task_full_title(name))

            checkbox = QtWidgets.QCheckBox(self)
            checkbox.setChecked(task.get('completed', False))
            checkbox.setStyleSheet(styles["checkbox_style"])
            checkbox.toggled.connect(
                lambda checked, t=task, b_index=button_index: self.toggle_task_completed(t, b_index, checked))

            edit_btn = QtWidgets.QPushButton("✎", self)
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet(styles["edit_button_style"])
            edit_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.edit_task(t, b_index))

            delete_btn = QtWidgets.QPushButton("✖", self)
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet(styles["delete_button_style"])
            delete_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.delete_task(t, b_index))

            task_layout.addWidget(btn)
            task_layout.addWidget(checkbox)
            task_layout.addWidget(edit_btn)
            task_layout.addWidget(delete_btn)

            layout.addWidget(task_widget)

    def edit_task(self, task, button_index):
        dialog = QInputDialog(self)
        dialog.setWindowTitle('Редактировать задачу')
        dialog.setLabelText('Введите новое название задачи:')
        dialog.setTextValue(task['name'])
        dialog.setOkButtonText('OK')
        dialog.setCancelButtonText('Отменить')

        if dialog.exec_() == QInputDialog.Accepted:
            new_name = dialog.textValue()
            if new_name:
                if len(new_name) > self.MAX_TASK_LENGTH:
                    QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 450 символов.')
                    return

                date, ok = QInputDialog.getText(self, 'Изменить дату', 'Введите новую дату (ДД.ММ.ГГ):',
                                                text=task.get('date', ''))
                if not ok:
                    return

                if date:
                    try:
                        task_date = datetime.datetime.strptime(date, '%d.%m.%y').date()
                    except ValueError:
                        QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте ДД.ММ.ГГ.')
                        return
                else:
                    task_date = ''

                for t in self.tasks_data[str(button_index)]["tasks"]:
                    if t['name'] == task['name']:
                        t['name'] = new_name
                        t['date'] = task_date.isoformat() if task_date else ''   
                        break

                self.save_tasks_to_file()
                self.update_task_layout()

    def delete_task(self, task, button_index):
        try:
            self.tasks_data[str(button_index)]["tasks"] = [
                t for t in self.tasks_data[str(button_index)]["tasks"] if t['name'] != task['name']
            ]
            self.save_tasks_to_file()
            self.update_task_layout()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при удалении задачи: {e}')

    def add_task_input(self, button_index, task_type):
        print(f"Добавляем задачу ({task_type})...")
        button_index = int(button_index)
        task_type_map = {
            "important": "Важных дел",
            "additional": "Дополнительных дел"
        }
        dialog_title = f'Добавить {task_type_map.get(task_type, "Задачу")}'
        text, ok = QInputDialog.getText(self, dialog_title, 'Введите название задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            if len(self.tasks_data[str(button_index)]["tasks"]) < self.MAX_TASKS_COUNT:
                new_task = {"name": text, "completed": False}
                self.tasks_data[str(button_index)]["tasks"].append(new_task)
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.information(self, 'Сообщение',
                                        f'Вы уже добавили максимальное количество задач ({self.MAX_TASKS_COUNT})!')

    def add_new_daily_task(self):
        text, ok = QInputDialog.getText(self, 'Добавить ежедневную задачу', 'Введите название ежедневной задачи:')
        if ok and text:
            if len(text) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 450 символов.')
                return
            new_task = {"name": text, "completed": False, "daily": True}

            daily_task_index = 0
            tasks = self.tasks_data[str(self.current_button_index)]["tasks"]
            for index, task in enumerate(tasks):
                if task.get('daily', False):
                    daily_task_index = index + 1

            self.tasks_data[str(self.current_button_index)]["tasks"].insert(daily_task_index, new_task)
            self.save_tasks_to_file()
            self.update_task_layout()
            self.scroll_area.show()

    def update_task_layout(self):
        layout = self.scroll_area.widget().layout()
        self.clear_layout(layout)

        button_tasks = self.tasks_data.get(str(self.current_button_index), {"tasks": []})
        self.add_tasks_to_layout(layout, button_tasks["tasks"], None, self.current_button_index)

    def clear_window(self, keep_main_buttons=False, keep_labels=False):
        widgets_to_keep = [self.search_button] + self.buttons if keep_main_buttons else []
        if keep_labels:
            widgets_to_keep.extend([self.text_high, self.text_low])
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget not in widgets_to_keep:
                widget.deleteLater()

        if hasattr(self, 'scroll_area') and self.scroll_area is not None:
            try:
                self.scroll_area.hide()
            except RuntimeError:
                pass

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
