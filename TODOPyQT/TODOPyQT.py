import json
import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, \
    QMessageBox, QLineEdit, QListWidget, QListWidgetItem, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt

from add_weekly_task_dialog import AddWeeklyTaskDialog
from note_page import NotePage
from HowToUse import HelpDialog
from text_wrapping import wrap_text
from add_task_dialog import AddTaskDialog
from styles import search_input_style, day_button_style, main_window_style, settings_style, \
    get_task_group_styles, add_tasks_button_style, tasks_button_style, results_list_style, add_daily_tasks_button_style, \
    daily_task_button_style, tag_button_style, add_weekly_tasks_button_style
from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setWindowIcon(QIcon('TODO List icon.ico'))
        self.setGeometry(100, 100, 1280, 720)

        self.current_button_index = 1
        self.set_current_week()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.completed_tasks_count = 0
        self.load_settings()
        self.save_settings()

        self.load_tasks()
        self.load_daily_tasks()

        self.weekly_tasks_data = {}
        self.load_weekly_tasks()

        self.scroll_area = None
        self.buttons = []

        self.main_screen()

        with open("notes.json", "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            self.notes = notes_data.get("notes", {})

        self.update_task_layout()

        self.tags = ["Работа📄", "Дом🏚", "Личное🎸", "Учёба✍️"]

    MAX_TASKS_COUNT = 90
    MAX_TASK_LENGTH = 450

    def save_tasks_to_file(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks_data, file, ensure_ascii=False, indent=4)

    def save_daily_tasks_to_file(self):
        with open("daily_tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.daily_tasks_data, file, ensure_ascii=False, indent=4)

    def save_weekly_tasks(self):
        with open("weekly_tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.weekly_tasks_data, file, ensure_ascii=False, indent=4)

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.completed_tasks_count = settings.get("completed_tasks_count", 0)
                self.completed_tasks_history = settings.get("completed_tasks_history", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.completed_tasks_history = []
            self.completed_tasks_count = 0

    def save_settings(self):
        settings = {
            "completed_tasks_count": self.completed_tasks_count,
            "completed_tasks_history": self.completed_tasks_history
        }
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def load_daily_tasks(self):
        try:
            with open("daily_tasks.json", "r", encoding="utf-8") as file:
                self.daily_tasks_data = json.load(file)
            print(f"Загруженные ежедневные задачи: {self.daily_tasks_data}")
        except FileNotFoundError:
            self.daily_tasks_data = {}
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Файл daily_tasks.json поврежден. Начинаем с пустого списка.')
            self.daily_tasks_data = {}

    def load_weekly_tasks(self):
        try:
            with open("weekly_tasks.json", "r", encoding="utf-8") as file:
                self.weekly_tasks_data = json.load(file)
            print(f"Загруженные еженедельные задачи: {self.weekly_tasks_data}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.weekly_tasks_data = {}

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                self.tasks_data = json.load(file)
            print(f"Загруженные задачи: {self.tasks_data}")
        except FileNotFoundError:
            self.tasks_data = {}
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Файл поврежден. Начинаем с пустого списка.')
            self.tasks_data = {}

    def style_search_input(self):
        self.search_input.setStyleSheet(search_input_style())

    def apply_main_window_style(self):
        self.setStyleSheet(main_window_style())

    def get_settings_style(self):
        return settings_style()

    def show_completed_tasks_history(self):
        try:
            history_dialog = QDialog(self)
            history_dialog.setWindowTitle("История выполненных задач")
            history_layout = QVBoxLayout(history_dialog)

            history_list = QListWidget()
            history_layout.addWidget(history_list)

            for task in self.completed_tasks_history:
                task_str = f"{task['name']} - {task['completed_date']}"
                history_list.addItem(task_str)

            history_dialog.setLayout(history_layout)
            history_dialog.exec_()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при показе истории выполненных задач: {e}')

    def toggle_task_completed(self, task, button_index, checked):
        task_name = task['name']
        task_date = task.get('date')
        task['daily'] = task.get('daily', False)

        if task['daily']:
            if checked:
                if 'completed_dates' not in self.daily_tasks_data[task_name]:
                    self.daily_tasks_data[task_name]['completed_dates'] = []
                self.daily_tasks_data[task_name]['completed_dates'].append(task_date)
                self.completed_tasks_history.append({'name': task_name, 'completed_date': task_date})
            else:
                if 'completed_dates' in self.daily_tasks_data[task_name]:
                    self.daily_tasks_data[task_name]['completed_dates'] = [
                        date for date in self.daily_tasks_data[task_name]['completed_dates'] if date != task_date]

            self.save_daily_tasks_to_file()
        else:
            task['completed'] = checked
            for year, months in self.tasks_data.items():
                for month, month_data in months.items():
                    tasks = month_data["tasks"]
                    for t in tasks:
                        if t['name'] == task['name']:
                            t['completed'] = checked
                            if checked:
                                self.completed_tasks_history.append({'name': task_name, 'completed_date': task_date})
                            else:
                                self.completed_tasks_history = [task for task in self.completed_tasks_history if
                                                                task['name'] != task_name and task[
                                                                    'completed_date'] != task_date]
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

        tasks_widget = QWidget()
        layout = QVBoxLayout(tasks_widget)

        self.scroll_area.setWidget(tasks_widget)

        self.week_label = QLabel(self)
        self.week_label.setGeometry(20, 20, 200, 30)
        self.update_week_label()
        self.week_label.show()

        self.previous_week_button = QPushButton("<", self)
        self.previous_week_button.setGeometry(240, 20, 50, 30)
        self.previous_week_button.clicked.connect(self.previous_week)
        self.previous_week_button.show()

        self.next_week_button = QPushButton(">", self)
        self.next_week_button.setGeometry(300, 20, 50, 30)
        self.next_week_button.clicked.connect(self.next_week)
        self.next_week_button.show()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, self.width() - 150, 30)
        self.search_input.setStyleSheet(search_input_style())
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(self.width() - 120, 60, 100, 30)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.search_button.show()

        self.add_task_button = QPushButton("Добавить задачу", self)
        self.add_task_button.setGeometry(20, 110, 180, 40)
        self.add_task_button.setStyleSheet(add_tasks_button_style())
        self.add_task_button.clicked.connect(self.add_new_task)
        self.add_task_button.show()

        self.add_daily_task_button = QPushButton("Добавить ежедневную задачу", self)
        self.add_daily_task_button.setGeometry(220, 110, 250, 40)
        self.add_daily_task_button.setStyleSheet(add_daily_tasks_button_style())
        self.add_daily_task_button.clicked.connect(self.add_new_daily_task)
        self.add_daily_task_button.show()

        self.add_weekly_task_button = QPushButton("Добавить еженедельную задачу", self)
        self.add_weekly_task_button.setGeometry(480, 110, 250, 40)
        self.add_weekly_task_button.setStyleSheet(add_weekly_tasks_button_style())
        self.add_weekly_task_button.clicked.connect(self.add_new_weekly_task)
        self.add_weekly_task_button.show()

        self.choose_month_button = QPushButton("Выбрать месяц", self)
        self.choose_month_button.setGeometry(self.width() - 220, self.height() - 110, 200, 40)
        self.choose_month_button.clicked.connect(self.show_month_selector)
        self.choose_month_button.show()

        self.scroll_area.setWidget(tasks_widget)
        self.scroll_area.show()

        self.update_task_layout()
        print("Показываем область с задачами")

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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        usage_layout = QHBoxLayout()
        usage_label = QLabel("Как пользоваться:")
        usage_label.setStyleSheet(styles["label_style"])
        usage_layout.addWidget(usage_label)

        help_button = QPushButton("Справка")
        help_button.setStyleSheet(styles["button_style"])
        help_button.clicked.connect(self.show_help_dialog)
        usage_layout.addWidget(help_button)
        usage_layout.addStretch()
        main_layout.addLayout(usage_layout)

        completed_layout = QVBoxLayout()
        self.completed_tasks_label = QLabel(f"Выполнено задач: {self.completed_tasks_count}")
        self.completed_tasks_label.setStyleSheet(styles["completed_tasks_label_style"])
        self.completed_tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        completed_layout.addWidget(self.completed_tasks_label)

        reset_button = QPushButton("Сбросить")
        reset_button.setStyleSheet(styles["reset_button_style"])
        reset_button.clicked.connect(self.reset_completed_tasks_count)
        reset_button.setFixedWidth(200)
        reset_button.setFixedHeight(30)
        completed_layout.addWidget(reset_button)
        completed_layout.setAlignment(reset_button, QtCore.Qt.AlignHCenter)
        main_layout.addLayout(completed_layout)

        history_layout = QVBoxLayout()
        history_button = QPushButton("История выполненных задач")
        history_button.setStyleSheet(styles["button_style"])
        history_button.clicked.connect(self.show_completed_tasks_history)
        history_button.setFixedWidth(250)
        history_button.setFixedHeight(30)
        history_layout.addWidget(history_button)
        history_layout.setAlignment(history_button, QtCore.Qt.AlignHCenter)
        history_layout.addStretch()
        main_layout.addLayout(history_layout)

        main_layout.addStretch()
        setup_ui_elements(self)

    def show_help_dialog(self):
        print("Справка")
        help_dialog = HelpDialog(self)
        help_dialog.exec_()

    def show_task_full_title(self, task_name):
        wrapped_task_name = wrap_text(task_name, 100)
        QMessageBox.information(self, 'Полное название задачи', wrapped_task_name)

    def set_current_week(self):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        self.current_week_start = start_of_week
        self.current_week_end = end_of_week

    def update_week_label(self):
        week_str = f"{self.current_week_start.strftime('%d.%m')} - {self.current_week_end.strftime('%d.%m')}"
        self.week_label.setText(f"Неделя: {week_str}")

    def previous_week(self):
        self.current_week_start -= datetime.timedelta(days=7)
        self.current_week_end -= datetime.timedelta(days=7)
        self.update_week_label()
        self.update_task_layout()

    def next_week(self):
        self.current_week_start += datetime.timedelta(days=7)
        self.current_week_end += datetime.timedelta(days=7)
        self.update_week_label()
        self.update_task_layout()

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
            for year_name, months in self.tasks_data.items():
                for month_name, month_data in months.items():
                    for task in month_data.get("tasks", []):
                        if search_text in task['name'].lower():
                            date = task.get('date', 'Нет даты')
                            formatted_date = date if date else 'Нет даты'
                            search_results.append((f"{year_name} - {month_name}", task['name'], formatted_date))

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

        if hasattr(self, 'results_widget') and self.results_widget is not None:
            self.results_widget.deleteLater()
            self.results_widget = None

        if hasattr(self, 'scroll_area') and self.scroll_area is not None:
            self.scroll_area.deleteLater()
            self.scroll_area = None

        self.search_button.hide()

        results_widget = QWidget()
        self.results_widget = results_widget
        results_layout = QVBoxLayout(results_widget)

        title_label = QLabel("Результаты поиска", self)
        title_label.setStyleSheet("font-size: 18px; margin: 10px;")
        results_layout.addWidget(title_label)

        scroll_area = QScrollArea(results_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area = scroll_area

        results_container = QWidget()
        results_list_layout = QVBoxLayout(results_container)

        self.results_list = QListWidget()
        self.results_list.setStyleSheet(results_list_style())

        for year_month, task_name, task_date in search_results:
            item_text = f"{year_month}: {task_name} ({task_date})"
            item = QListWidgetItem(item_text)
            self.results_list.addItem(item)

        self.results_list.itemClicked.connect(lambda item: self.go_to_task_detail(item))
        results_list_layout.addWidget(self.results_list)
        results_container.setLayout(results_list_layout)
        scroll_area.setWidget(results_container)

        results_layout.addWidget(scroll_area)
        results_widget.setLayout(results_layout)
        self.setCentralWidget(results_widget)
        results_widget.show()
        setup_ui_elements(self)

    def go_to_task_detail(self, item):
        print("Переход к результатам поиска")
        details = item.text().split(": ")
        month = details[0]
        task_name = details[1]

        self.selected_month = month
        self.selected_task_name = task_name
        self.clear_window(keep_main_buttons=True)

        self.handle_button_click(self.selected_month)

    def show_month_selector(self):
        month_counts = self.calculate_task_counts_per_month()

        self.month_dialog = QDialog(self)
        self.month_dialog.setWindowTitle("Выбрать месяц")
        layout = QVBoxLayout(self.month_dialog)

        month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                       'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        for i, count in enumerate(month_counts):
            month_button = QPushButton(f"{month_names[i]}: {count} задач")
            month_button.clicked.connect(lambda checked, month=i + 1: self.show_tasks_by_month(month))
            layout.addWidget(month_button)

        self.month_dialog.setLayout(layout)
        self.month_dialog.exec_()

    def calculate_task_counts_per_month(self):
        month_counts = [0] * 12

        for year_name, months in self.tasks_data.items():
            for month_name, month_data in months.items():
                tasks = month_data.get("tasks", [])
                month_index = self.get_month_index(month_name)
                if month_index is not None:
                    month_counts[month_index] += len(tasks)

        return month_counts

    def show_tasks_by_month(self, month):
        self.month_dialog.accept()

        self.previous_week_button.hide()
        self.next_week_button.hide()
        self.choose_month_button.hide()
        self.add_task_button.hide()
        self.add_daily_task_button.hide()

        month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                       'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        selected_month_name = month_names[month - 1]
        self.week_label.setText(f"Месяц: {selected_month_name}")
        self.week_label.show()

        tasks_layout = self.recreate_task_scroll_area()

        tasks_for_month = []
        for year_name, months in self.tasks_data.items():
            for month_name, month_data in months.items():
                month_index = self.get_month_index(month_name)
                if month_index is not None and month_index == month - 1:
                    tasks_for_month.extend(month_data.get("tasks", []))

        if tasks_for_month:
            self.add_tasks_to_layout(tasks_layout, tasks_for_month, None, self.current_button_index)
        else:
            QMessageBox.information(self, 'Задачи', 'На этот месяц задач нет.')

        self.scroll_area.show()

    def get_month_index(self, month_name):
        month_names_en = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
        month_names_ru = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        if month_name in month_names_en:
            return month_names_en.index(month_name)
        elif month_name in month_names_ru:
            return month_names_ru.index(month_name)
        return None

    def add_new_task(self):
        dialog = AddTaskDialog(self.tags, self)

        if dialog.exec_() == QDialog.Accepted:
            task_name, date_str, tag = dialog.get_task_data()

            if not task_name:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
                return

            if len(task_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка',
                                    f"Название задачи должно быть не более {self.MAX_TASK_LENGTH} символов.")
                return

            try:
                task_date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
                formatted_date = task_date.strftime('%d.%m.%Y')
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте dd.mm.yyyy.')
                return

            year_name = str(task_date.year)
            month_name = task_date.strftime('%B')

            if year_name not in self.tasks_data:
                self.tasks_data[year_name] = {}

            if month_name not in self.tasks_data[year_name]:
                self.tasks_data[year_name][month_name] = {"tasks": []}

            new_task = {"name": task_name, "completed": False, "date": formatted_date, "tag": tag}
            self.tasks_data[year_name][month_name]["tasks"].append(new_task)
            self.save_tasks_to_file()
            self.update_task_layout()
            self.scroll_area.show()

            print(f"Добавлена новая задача: {new_task} в год: {year_name}, месяц: {month_name}")

    def add_new_daily_task(self):
        text, ok = QInputDialog.getText(self, 'Добавить ежедневную задачу', 'Введите название ежедневной задачи:')
        if not ok or not text:
            return

        if len(text) > self.MAX_TASK_LENGTH:
            QMessageBox.warning(self, 'Ошибка', 'Название задачи должно быть не более 450 символов.')
            return

        date_str, ok = QInputDialog.getText(self, 'Добавить дату', 'Введите дату начала в формате dd.mm.yyyy:')
        if not ok or not date_str:
            return

        try:
            start_date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте dd.mm.yyyy.')
            return

        new_task = {
            "name": text,
            "completed": False,
            "start_date": start_date.strftime('%d.%m.%Y')
        }

        self.daily_tasks_data[text] = new_task
        self.save_daily_tasks_to_file()
        self.update_task_layout()
        self.scroll_area.show()

        print(f"Добавлена новая ежедневная задача: {new_task}")

    def add_new_weekly_task(self):
        dialog = AddWeeklyTaskDialog(self.tags, self)

        if dialog.exec_() == QDialog.Accepted:
            task_name, start_date, days, tags = dialog.get_task_data()

            if not task_name:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
                return

            if len(task_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка',
                                    f"Название задачи должно быть не более {self.MAX_TASK_LENGTH} символов.")
                return

            try:
                task_date = datetime.datetime.strptime(start_date, '%d.%m.%Y').date()
                formatted_date = task_date.strftime('%d.%m.%Y')
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте dd.mm.yyyy.')
                return

            new_task = {
                "name": task_name,
                "completed": False,
                "start_date": formatted_date,
                "days": days,
                "tag": tags
            }

            self.weekly_tasks_data[task_name] = new_task
            self.save_weekly_tasks()
            self.update_task_layout()
            self.scroll_area.show()

            print(f"Добавлена новая еженедельная задача: {new_task}")

    def handle_button_click(self, button_index=None):
        self.current_button_index = button_index
        self.main_screen()

    def add_tasks_to_layout(self, layout, tasks, is_important, button_index):
        tasks_style = tasks_button_style()
        daily_tasks_style = daily_task_button_style()
        styles = get_task_group_styles()
        tag_style = tag_button_style()

        print(f"Добавляем задачи в компоновку: {tasks}")

        for task in tasks:
            task_name = task['name']
            task_date = task.get('date', '')
            task_tag = task.get('tag', '')

            if task_date:
                try:
                    formatted_date = datetime.datetime.strptime(task_date, '%d.%m.%Y').strftime('%d.%m.%Y')
                except ValueError:
                    formatted_date = 'Неверный формат даты'
            else:
                formatted_date = 'Нет даты'

            task_widget = QWidget(self)
            task_layout = QHBoxLayout(task_widget)

            btn_style = daily_tasks_style if task.get('daily', False) else tasks_style

            btn = QPushButton(f"{task_name} ({formatted_date})", self)
            btn.setStyleSheet(btn_style)
            btn.setFixedSize(670, 50)
            btn.clicked.connect(lambda _, name=task_name: self.show_task_full_title(name))

            checkbox = QtWidgets.QCheckBox(self)
            checkbox.setChecked(task.get('completed', False))
            checkbox.setStyleSheet(styles["checkbox_style"])
            checkbox.toggled.connect(
                lambda checked, t=task, b_index=button_index: self.toggle_task_completed(t, b_index, checked))

            tag_button = QPushButton(task_tag, self)
            tag_button.setStyleSheet(tag_style)
            tag_button.setFixedSize(130, 50)
            if not task_tag:
                tag_button.hide()

            edit_btn = QPushButton("✎", self)
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet(styles["edit_button_style"])
            edit_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.edit_task(t, b_index))

            delete_btn = QPushButton("✖️", self)
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet(styles["delete_button_style"])
            delete_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.delete_task(t, b_index))

            task_layout.addWidget(btn)
            task_layout.addWidget(checkbox)
            task_layout.addWidget(tag_button)
            task_layout.addWidget(edit_btn)
            task_layout.addWidget(delete_btn)

            layout.addWidget(task_widget)
            print(f"Задача '{task_name}' добавлена в компоновку")

    def edit_task(self, task, button_index):
        dialog = AddTaskDialog(self.tags, self, task_name=task['name'], task_date=task.get('date', ''),
                               task_tag=task.get('tag', ''))

        if dialog.exec_() == QDialog.Accepted:
            new_name, new_date, new_tag = dialog.get_task_data()

            if not new_name:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
                return

            if len(new_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка',
                                    f"Название задачи должно быть не более {self.MAX_TASK_LENGTH} символов.")
                return

            if new_date:
                try:
                    task_date = datetime.datetime.strptime(new_date, '%d.%m.%Y').date()
                    formatted_date = task_date.strftime('%d.%m.%Y')
                except ValueError:
                    QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте dd.mm.yyyy.')
                    return
            else:
                formatted_date = ''

            task_to_edit = None
            for year_name, months in self.tasks_data.items():
                for month_name, month_data in months.items():
                    for t in month_data["tasks"]:
                        if t == task:
                            task_to_edit = t
                            break
                    if task_to_edit:
                        break
                if task_to_edit:
                    break

            if task_to_edit:
                task_to_edit['name'] = new_name
                task_to_edit['date'] = formatted_date
                task_to_edit['tag'] = new_tag if new_tag else ''
                self.save_tasks_to_file()
                self.update_task_layout()
                print(f"Задача обновлена: {task_to_edit}")

            elif task.get('daily', False):
                daily_task = self.daily_tasks_data.get(task['name'])
                if daily_task:
                    daily_task['name'] = new_name
                    daily_task['start_date'] = formatted_date
                    daily_task['tag'] = new_tag if new_tag else ''
                    self.save_daily_tasks_to_file()
                    self.update_task_layout()
                    print(f"Ежедневная задача обновлена: {daily_task}")

    def delete_task(self, task, button_index):
        try:
            task_date_str = task.get('date', '')
            if task_date_str:
                task_date = datetime.datetime.strptime(task_date_str, '%d.%m.%Y').date()
                year_name = str(task_date.year)
                month_name = task_date.strftime('%B')

                if year_name in self.tasks_data and month_name in self.tasks_data[year_name]:
                    self.tasks_data[year_name][month_name]["tasks"] = [
                        t for t in self.tasks_data[year_name][month_name]["tasks"] if t['name'] != task['name']
                    ]

            if task.get('daily', False):
                del self.daily_tasks_data[task['name']]

            self.save_tasks_to_file()
            self.save_daily_tasks_to_file()
            self.update_task_layout()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при удалении задачи: {e}')

    def clear_window(self, keep_main_buttons=False, keep_labels=False):
        widgets_to_keep = [self.search_button] + self.buttons if keep_main_buttons else []
        if keep_labels:
            widgets_to_keep.extend([self.text_high, self.text_low])

        for widget in self.findChildren(QtWidgets.QWidget):
            if widget not in widgets_to_keep:
                widget.hide()
                widget.deleteLater()

        if hasattr(self, 'scroll_area') and self.scroll_area is not None:
            self.scroll_area.hide()
            self.scroll_area.deleteLater()
            self.scroll_area = None

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

    def update_task_layout(self):
        tasks_widget = self.scroll_area.widget()
        if tasks_widget is None:
            print("Ошибка: tasks_widget не существует.")
            return

        layout = tasks_widget.layout()

        if layout is None:
            print("Ошибка: layout не существует.")
            return

        self.clear_layout(layout)

        print(f"Текущая неделя: начало {self.current_week_start}, конец {self.current_week_end}")
        print(f"Текущий индекс кнопки: {self.current_button_index}")

        week_tasks = {self.current_week_start + datetime.timedelta(days=i): [] for i in range(7)}

        for task_name, task in self.daily_tasks_data.items():
            start_date_str = task.get('start_date')
            completed_dates = task.get('completed_dates', [])
            task_days = task.get('days', [])

            if start_date_str:
                try:
                    start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').date()
                    current_date = max(start_date, self.current_week_start)
                    while current_date <= self.current_week_end:
                        daily_task = task.copy()
                        daily_task['date'] = current_date.strftime('%d.%m.%Y')
                        daily_task['daily'] = True
                        daily_task['completed'] = daily_task['date'] in completed_dates
                        weekday = current_date.strftime('%A')
                        if not task_days or weekday in task_days:
                            week_tasks[current_date].append(daily_task)
                            print(f"Ежедневная задача добавлена: {daily_task}")
                        current_date += datetime.timedelta(days=1)
                except ValueError:
                    print(f"Некорректный формат даты для ежедневной задачи: {start_date_str}")

        for task_name, task in self.weekly_tasks_data.items():
            start_date_str = task.get('start_date')
            completed_dates = task.get('completed_dates', [])
            task_days = task.get('days', [])

            if start_date_str:
                try:
                    start_date = datetime.datetime.strptime(start_date_str, '%d.%м.%Y').date()
                    current_date = max(start_date, self.current_week_start)
                    while current_date <= self.current_week_end:
                        weekly_task = task.copy()
                        weekly_task['date'] = current_date.strftime('%d.%m.%Y')
                        weekly_task['weekly'] = True
                        weekly_task['completed'] = weekly_task['date'] in completed_dates
                        weekday = current_date.strftime('%A')
                        if not task_days or weekday in task_days:
                            week_tasks[current_date].append(weekly_task)
                            print(f"Еженедельная задача добавлена: {weekly_task}")
                        current_date += datetime.timedelta(days=1)
                except ValueError:
                    print(f"Некорректный формат даты для еженедельной задачи: {start_date_str}")

        for year_name, months in self.tasks_data.items():
            for month_name, month_data in months.items():
                for task in month_data.get("tasks", []):
                    task_date = task.get('date')
                    if task_date:
                        try:
                            task_date_obj = datetime.datetime.strptime(task_date, '%d.%m.%Y').date()
                            if self.current_week_start <= task_date_obj <= self.current_week_end:
                                week_tasks[task_date_obj].append(task)
                                print(f"Задача добавлена: {task}")
                        except ValueError:
                            print(f"Некорректный формат даты для задачи: {task_date}")

        tasks_in_current_week = []
        for day, tasks in week_tasks.items():
            tasks_in_current_week.extend(tasks)

        print(f"Задачи для текущей недели: {tasks_in_current_week}")

        self.add_tasks_to_layout(layout, tasks_in_current_week, None, self.current_button_index)
        self.scroll_area.show()


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
