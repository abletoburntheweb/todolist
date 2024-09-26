import json
import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, \
    QMessageBox, QLineEdit, QListWidget, QListWidgetItem, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QDialog, \
    QGroupBox, QSpinBox
from PyQt5.QtCore import Qt, QSize, QDate

from add_daily_task_dialog import AddDailyTaskDialog
from add_weekly_task_dialog import AddWeeklyTaskDialog
from note_page import NotePage
from HowToUse import HelpDialog, RegularTaskDialog, DailyTaskDialog, WeeklyTaskDialog
from text_wrapping import wrap_text
from add_task_dialog import AddTaskDialog
from styles import search_input_style, day_button_style, main_window_style, settings_style, \
    get_task_group_styles, add_tasks_button_style, tasks_button_style, results_list_style, add_daily_tasks_button_style, \
    daily_task_button_style, tag_button_style, add_weekly_tasks_button_style, weekly_tasks_button_style
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
        self.day_mapping = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье"
        }
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

        with open("daily_tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.daily_tasks_data, file, ensure_ascii=False, indent=4)

        with open("weekly_tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.weekly_tasks_data, file, ensure_ascii=False, indent=4)

    def save_daily_tasks_to_file(self):
        with open("daily_tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.daily_tasks_data, file, ensure_ascii=False, indent=4)

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.completed_tasks_count = settings.get("completed_tasks_count", 0)
                self.completed_tasks_history = settings.get("completed_tasks_history", [])
                self.default_task_days = settings.get("default_task_days", 90)
        except (FileNotFoundError, json.JSONDecodeError):
            self.completed_tasks_history = []
            self.completed_tasks_count = 0
            self.default_task_days = 90

    def save_days_setting(self):
        days_value = self.days_input.text()
        if days_value.isdigit():
            self.default_task_days = int(days_value)
            self.save_settings()
            QMessageBox.information(self, "Успешно", "Настройка дней сохранена.")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите корректное числовое значение.")

    def save_settings(self):
        settings = {
            "completed_tasks_count": self.completed_tasks_count,
            "completed_tasks_history": self.completed_tasks_history,
            "default_task_days": self.default_task_days
        }
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def load_daily_tasks(self):
        try:
            with open("daily_tasks.json", "r", encoding="utf-8") as file:
                self.daily_tasks_data = json.load(file)
                for task_name, task in self.daily_tasks_data.items():
                    if isinstance(task, dict):
                        if 'name' not in task:
                            print(f"Задача '{task_name}' без ключа 'name' пропущена.")
                            continue
                        task['type'] = 'daily'
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
                for task_name, task in self.weekly_tasks_data.items():
                    if isinstance(task, dict):
                        task.setdefault('type', 'weekly')
                        task.setdefault('completed_dates', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.weekly_tasks_data = {}

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                self.tasks_data = json.load(file)
                for year, months in self.tasks_data.items():
                    for month, month_data in months.items():
                        for task in month_data["tasks"]:
                            if isinstance(task, dict):
                                task['type'] = 'regular'
        except FileNotFoundError:
            self.tasks_data = {}
        except json.JSONDecodeError:
            QMessageBox.warning(self, 'Ошибка', 'Файл tasks.json поврежден. Начинаем с пустого списка.')
            self.tasks_data = {}

    def style_search_input(self):
        self.search_input.setStyleSheet(search_input_style())

    def apply_main_window_style(self):
        self.setStyleSheet(main_window_style())

    def get_settings_style(self):
        return settings_style()

    def show_completed_tasks_history(self):
        self.load_settings()
        try:
            history_dialog = QDialog(self)
            history_dialog.setWindowTitle("История выполненных задач")
            history_dialog.setFixedSize(700, 600)

            history_layout = QVBoxLayout(history_dialog)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            history_layout.addWidget(scroll_area)

            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            history_list = QListWidget()
            scroll_layout.addWidget(history_list)

            scroll_area.setWidget(scroll_widget)

            tasks_by_date = {}
            for task in self.completed_tasks_history:
                completed_date = task['completed_date']
                if completed_date not in tasks_by_date:
                    tasks_by_date[completed_date] = []

                task_entry = {
                    'name': task['name'],
                    'tag': task.get('tag', 'Без тэга'),
                    'type': task.get('type', 'normal')
                }
                tasks_by_date[completed_date].append(task_entry)

            color_mapping = {
                'normal': '#22a4f5',
                'daily': '#7b61ff',
                'weekly': '#ffa861',
            }

            sorted_dates = sorted(tasks_by_date.keys(), key=lambda x: datetime.datetime.strptime(x, '%d.%m.%Y'),
                                  reverse=True)

            for date in sorted_dates:
                date_item = QListWidgetItem(date)
                date_item.setFlags(date_item.flags() & ~Qt.ItemIsSelectable)
                date_item.setBackground(QColor("#e0e0e0"))
                date_item.setSizeHint(QSize(0, 30))
                date_item.setFont(QFont("Arial", 10, QFont.Bold))
                history_list.addItem(date_item)

                for task in tasks_by_date[date]:
                    task_widget = QWidget()
                    task_layout = QHBoxLayout(task_widget)
                    task_layout.setContentsMargins(10, 5, 10, 5)

                    color_circle = QLabel()
                    color_circle.setFixedSize(20, 20)
                    task_type_color = color_mapping.get(task['type'], '#000')
                    task_tag_color = color_mapping.get(task['tag'], '#000')
                    combined_color = task_tag_color if task['tag'] in color_mapping else task_type_color

                    color_circle.setStyleSheet(f"""
                        QLabel {{
                            background-color: {combined_color};
                            border-radius: 10px;
                        }}
                    """)

                    task_name = QLabel(task['name'])
                    task_name.setStyleSheet("font-size: 16px; color: #333;")

                    task_tag = QLabel(task['tag'])
                    task_tag.setStyleSheet("font-size: 14px; color: #777;")

                    task_layout.addWidget(color_circle)
                    task_layout.addSpacing(10)
                    task_layout.addWidget(task_name)
                    task_layout.addStretch()
                    task_layout.addWidget(task_tag)

                    task_item = QListWidgetItem()
                    task_item.setSizeHint(task_widget.sizeHint())
                    history_list.addItem(task_item)
                    history_list.setItemWidget(task_item, task_widget)

            history_dialog.setLayout(history_layout)
            history_dialog.exec_()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при показе истории выполненных задач: {e}')

    def toggle_task_completed(self, task, button_index, checked):
        task_name = task['name']
        task_date = task.get('date', '')

        print(f"Попытка отметить задачу '{task_name}' как {'выполненную' if checked else 'не выполненную'}.")

        if 'daily' in task and task['daily']:
            if task_name in self.daily_tasks_data:
                if 'completed_dates' not in self.daily_tasks_data[task_name]:
                    self.daily_tasks_data[task_name]['completed_dates'] = []
                if checked:
                    if task_date not in self.daily_tasks_data[task_name]['completed_dates']:
                        self.daily_tasks_data[task_name]['completed_dates'].append(task_date)

                    unique_id = f"{task_name}|{task_date}"
                    if unique_id not in [f"{hist['name']}|{hist['completed_date']}" for hist in
                                         self.completed_tasks_history]:
                        self.completed_tasks_history.append({
                            'name': task_name,
                            'completed_date': task_date,
                            'tag': task.get('tag', 'Без тэга'),
                            'type': 'daily'
                        })
                else:
                    if task_date in self.daily_tasks_data[task_name]['completed_dates']:
                        self.daily_tasks_data[task_name]['completed_dates'].remove(task_date)

                    self.completed_tasks_history = [
                        t for t in self.completed_tasks_history
                        if not (t['name'] == task_name and t['completed_date'] == task_date)
                    ]
                self.save_daily_tasks_to_file()
            else:
                print(f"Задача '{task_name}' не найдена в daily_tasks_data.")
                return

        elif 'weekly' in task and task['weekly']:
            print(f"Проверка задачи '{task_name}' в weekly_tasks_data.")
            if task_name in self.weekly_tasks_data:
                if 'completed_dates' not in self.weekly_tasks_data[task_name]:
                    self.weekly_tasks_data[task_name]['completed_dates'] = []
                if checked:
                    if task_date not in self.weekly_tasks_data[task_name]['completed_dates']:
                        self.weekly_tasks_data[task_name]['completed_dates'].append(task_date)

                    unique_id = f"{task_name}|{task_date}"
                    if unique_id not in [f"{hist['name']}|{hist['completed_date']}" for hist in
                                         self.completed_tasks_history]:
                        self.completed_tasks_history.append({
                            'name': task_name,
                            'completed_date': task_date,
                            'tag': task.get('tag', 'Без тэга'),
                            'type': 'weekly'
                        })
                else:
                    if task_date in self.weekly_tasks_data[task_name]['completed_dates']:
                        self.weekly_tasks_data[task_name]['completed_dates'].remove(task_date)

                    self.completed_tasks_history = [
                        t for t in self.completed_tasks_history
                        if not (t['name'] == task_name and t['completed_date'] == task_date)
                    ]
                self.save_weekly_tasks()
            else:
                print(f"Задача '{task_name}' не найдена в weekly_tasks_data.")
                return
        else:
            task['completed'] = checked
            for year_name, months in self.tasks_data.items():
                for month_name, month_data in months.items():
                    tasks = month_data["tasks"]
                    for t in tasks:
                        if t['name'] == task['name'] and t.get('date') == task['date']:
                            t['completed'] = checked
                            if checked:
                                unique_id = f"{task_name}|{task_date}"
                                if unique_id not in [f"{hist['name']}|{hist['completed_date']}" for hist in
                                                     self.completed_tasks_history]:
                                    self.completed_tasks_history.append({
                                        'name': task_name,
                                        'completed_date': task_date,
                                        'tag': t.get('tag', 'Без тэга'),
                                        'type': 'normal'
                                    })
                            else:
                                self.completed_tasks_history = [
                                    old_task for old_task in self.completed_tasks_history
                                    if not (old_task['name'] == task_name and old_task['completed_date'] == task_date)
                                ]
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
            scroll_area_height = self.height() - scroll_area_y - 120

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
        self.previous_week_button.setCursor(Qt.PointingHandCursor)
        self.previous_week_button.clicked.connect(self.previous_week)
        self.previous_week_button.show()

        self.next_week_button = QPushButton(">", self)
        self.next_week_button.setGeometry(300, 20, 50, 30)
        self.next_week_button.setCursor(Qt.PointingHandCursor)
        self.next_week_button.clicked.connect(self.next_week)
        self.next_week_button.show()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск задачи...")
        self.search_input.setGeometry(20, 60, self.width() - 150, 30)
        self.search_input.setStyleSheet(search_input_style())
        self.search_input.show()

        self.search_button = QPushButton("Поиск", self)
        self.search_button.setGeometry(self.width() - 120, 60, 100, 30)
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.search_button_clicked)
        self.search_button.show()

        self.add_task_button = QPushButton("Добавить задачу", self)
        self.add_task_button.setGeometry(20, 110, 180, 40)
        self.add_task_button.setStyleSheet(add_tasks_button_style())
        self.add_task_button.setCursor(Qt.PointingHandCursor)
        self.add_task_button.clicked.connect(self.add_new_task)
        self.add_task_button.show()

        self.add_daily_task_button = QPushButton("Добавить ежедневную задачу", self)
        self.add_daily_task_button.setGeometry(220, 110, 250, 40)
        self.add_daily_task_button.setStyleSheet(add_daily_tasks_button_style())
        self.add_daily_task_button.setCursor(Qt.PointingHandCursor)
        self.add_daily_task_button.clicked.connect(self.add_new_daily_task)
        self.add_daily_task_button.show()

        self.add_weekly_task_button = QPushButton("Добавить еженедельную задачу", self)
        self.add_weekly_task_button.setGeometry(485, 110, 255, 40)
        self.add_weekly_task_button.setStyleSheet(add_weekly_tasks_button_style())
        self.add_weekly_task_button.setCursor(Qt.PointingHandCursor)
        self.add_weekly_task_button.clicked.connect(self.add_new_weekly_task)
        self.add_weekly_task_button.show()

        self.return_to_current_week_button = QPushButton("Текущая неделя", self)
        self.return_to_current_week_button.setGeometry(1060, 137, 200, 40)
        self.return_to_current_week_button.setCursor(Qt.PointingHandCursor)
        self.return_to_current_week_button.clicked.connect(self.return_to_current_week)
        self.return_to_current_week_button.show()

        self.choose_month_button = QPushButton("Выбрать месяц", self)
        self.choose_month_button.setGeometry(1060, 610, 200, 40)
        self.choose_month_button.setCursor(Qt.PointingHandCursor)
        self.choose_month_button.clicked.connect(self.show_month_selector)
        self.choose_month_button.show()

        self.scroll_area.setWidget(tasks_widget)
        self.scroll_area.show()

        self.update_task_layout()
        setup_ui_elements(self)
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

        styles = self.get_settings_style()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        title_label = QLabel("Настройки")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        usage_group_box = QGroupBox("Как пользоваться")
        usage_layout = QVBoxLayout()
        usage_group_box.setLayout(usage_layout)

        usage_horizontal_layout = QHBoxLayout()
        usage_label = QLabel("В этом разделе вы можете найти справку о том, как пользоваться приложением.")
        usage_label.setStyleSheet(styles["label_style"])
        usage_horizontal_layout.addWidget(usage_label, alignment=Qt.AlignLeft)

        help_button = QPushButton("Справка")
        help_button.setStyleSheet(styles["button_style"])
        help_button.setFixedSize(230, 40)
        help_button.setCursor(Qt.PointingHandCursor)
        help_button.clicked.connect(self.show_help_dialog)
        usage_horizontal_layout.addWidget(help_button, alignment=Qt.AlignRight)

        usage_layout.addLayout(usage_horizontal_layout)
        main_layout.addWidget(usage_group_box)

        task_types_group_box = QGroupBox("Типы задач")
        task_types_layout = QVBoxLayout()
        task_types_group_box.setLayout(task_types_layout)

        task_types_label = QLabel("Дополнительная информация о том, как работают типы задач.")
        task_types_label.setStyleSheet(styles["label_style"])
        task_types_label.setAlignment(Qt.AlignLeft)
        task_types_layout.addWidget(task_types_label, alignment=Qt.AlignLeft)

        task_types_horizontal_layout = QHBoxLayout()

        regular_tasks_button = QPushButton("Задачи")
        regular_tasks_button.setStyleSheet(styles["regular_tasks_button_style_info"])
        regular_tasks_button.setFixedSize(230, 40)
        regular_tasks_button.setCursor(Qt.PointingHandCursor)
        regular_tasks_button.clicked.connect(self.show_regular_task_info)
        task_types_horizontal_layout.addWidget(regular_tasks_button)

        daily_tasks_button = QPushButton("Ежедневные задачи")
        daily_tasks_button.setStyleSheet(styles["daily_tasks_button_style_info"])
        daily_tasks_button.setFixedSize(230, 40)
        daily_tasks_button.setCursor(Qt.PointingHandCursor)
        daily_tasks_button.clicked.connect(self.show_daily_task_info)
        task_types_horizontal_layout.addWidget(daily_tasks_button)

        weekly_tasks_button = QPushButton("Еженедельные задачи")
        weekly_tasks_button.setStyleSheet(styles["weekly_tasks_button_style_info"])
        weekly_tasks_button.setFixedSize(230, 40)
        weekly_tasks_button.setCursor(Qt.PointingHandCursor)
        weekly_tasks_button.clicked.connect(self.show_weekly_task_info)
        task_types_horizontal_layout.addWidget(weekly_tasks_button)

        task_types_layout.addLayout(task_types_horizontal_layout)
        main_layout.addWidget(task_types_group_box)

        days_group_box = QGroupBox("Настройка дней для автоматической задачи")
        days_layout = QVBoxLayout()
        days_group_box.setLayout(days_layout)

        days_label = QLabel("Введите количество дней, на которые будет добавлена задача (по умолчанию 90):")
        days_label.setStyleSheet(styles["label_style"])
        days_layout.addWidget(days_label)

        self.days_spinbox = QSpinBox(self)
        self.days_spinbox.setStyleSheet(styles["spinbox_style"])
        self.days_spinbox.setMinimum(1)
        self.days_spinbox.setMaximum(365)
        self.days_spinbox.setValue(self.default_task_days)
        self.days_spinbox.setFixedWidth(100)
        days_layout.addWidget(self.days_spinbox)

        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet(styles["button_style"])
        save_button.setFixedSize(230, 40)
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.save_days_setting)
        days_layout.addWidget(save_button)

        main_layout.addWidget(days_group_box)

        completed_group_box = QGroupBox("Выполненные задачи")
        completed_layout = QVBoxLayout()
        completed_group_box.setLayout(completed_layout)

        completed_group_box = QGroupBox("Выполненные задачи")
        completed_layout = QVBoxLayout()
        completed_group_box.setLayout(completed_layout)

        self.completed_tasks_label = QLabel(f"Выполнено задач: {self.completed_tasks_count}")
        self.completed_tasks_label.setStyleSheet(styles["completed_tasks_label_style"])
        self.completed_tasks_label.setAlignment(Qt.AlignCenter)
        completed_layout.addWidget(self.completed_tasks_label, alignment=Qt.AlignCenter)

        history_button = QPushButton("История выполненных задач")
        history_button.setStyleSheet(styles["button_style"])
        history_button.setFixedSize(230, 40)
        history_button.setCursor(Qt.PointingHandCursor)
        history_button.clicked.connect(self.show_completed_tasks_history)
        completed_layout.addWidget(history_button, alignment=Qt.AlignCenter)

        reset_button = QPushButton("Сбросить")
        reset_button.setStyleSheet(styles["reset_button_style"])
        reset_button.setFixedSize(230, 40)
        reset_button.setCursor(Qt.PointingHandCursor)
        reset_button.clicked.connect(self.reset_completed_tasks_count)
        completed_layout.addWidget(reset_button, alignment=Qt.AlignCenter)

        completed_layout.addStretch()
        main_layout.addWidget(completed_group_box)

        main_layout.addStretch()

        setup_ui_elements(self)
        print("Настроено окно настроек")

    def show_regular_task_info(self):
        print("Информация о обычных задачах")
        regular_tasks_dialog = RegularTaskDialog(self)
        regular_tasks_dialog.exec_()

    def show_daily_task_info(self):
        print("Информация о ежедневных задачах")
        daily_tasks_dialog = DailyTaskDialog(self)
        daily_tasks_dialog.exec_()

    def show_weekly_task_info(self):
        print("Информация о еженедельных задачах")
        weekly_tasks_dialog = WeeklyTaskDialog(self)
        weekly_tasks_dialog.exec_()

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

    def return_to_current_week(self):
        self.set_current_week()
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
            month_names_ru = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

            for year_name, months in self.tasks_data.items():
                for month_name, month_data in months.items():
                    for task in month_data.get("tasks", []):
                        if search_text in task['name'].lower():
                            date = task.get('date', 'Нет даты')

                            month_index = self.get_month_index(month_name)
                            if month_index is not None:
                                month_name_ru = month_names_ru[month_index]
                                formatted_month_name = month_name_ru
                            else:
                                formatted_month_name = month_name

                            formatted_date = date if date else 'Нет даты'
                            search_results.append(
                                (f"{year_name} - {formatted_month_name}", task['name'], formatted_date))

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

        results_container = QWidget()
        results_list_layout = QVBoxLayout(results_container)

        self.results_list = QListWidget()
        self.results_list.setStyleSheet(results_list_style())

        for year_month, task_name, task_date in search_results:
            item_text = f"{year_month}: {task_name} ({task_date})"
            item = QListWidgetItem(item_text)
            self.results_list.addItem(item)

            item.setData(Qt.UserRole, task_date)

        self.results_list.itemClicked.connect(self.go_to_task_detail)
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

        task_date = item.data(Qt.UserRole)

        self.go_to_week(task_date)

        self.clear_window(keep_main_buttons=True)
        self.handle_button_click(month)

    def show_month_selector(self):
        self.return_to_current_week_button.hide()
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
        self.add_weekly_task_button.hide()

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
                print(f"Неверный формат даты: {date_str}")
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте дд.мм.гггг.')
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

            print(f"Добавлена новая обычная задача: {new_task}")

    def add_new_daily_task(self):
        dialog = AddDailyTaskDialog(self.tags, self)

        if dialog.exec_() == QDialog.Accepted:
            task_name, start_date_str, end_date_str, tag = dialog.get_task_data()

            if not task_name:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
                return

            if len(task_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка',
                                    f"Название задачи должно быть не более {self.MAX_TASK_LENGTH} символов.")
                return

            try:
                start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').date()
                if end_date_str:
                    end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
                else:
                    end_date = None


                if end_date and end_date <= start_date:
                    end_date = start_date + datetime.timedelta(days=90)
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте дд.мм.гггг.')
                return

            new_task = {
                "name": task_name,
                "completed": False,
                "start_date": start_date_str,
                "end_date": end_date.strftime('%d.%m.%Y') if end_date else None,
                "tag": tag,
                "completed_dates": []
            }

            self.daily_tasks_data[task_name] = new_task
            self.save_daily_tasks_to_file()
            self.update_task_layout()
            self.scroll_area.show()

            print(f"Добавлена новая ежедневная задача: {new_task}")

    def add_new_weekly_task(self):
        dialog = AddWeeklyTaskDialog(self.tags, self)

        if dialog.exec_() == QDialog.Accepted:
            task_name, start_date_str, end_date_str, selected_days, tag = dialog.get_task_data()

            if not task_name:
                QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
                return

            if len(task_name) > self.MAX_TASK_LENGTH:
                QMessageBox.warning(self, 'Ошибка',
                                    f"Название задачи должно быть не более {self.MAX_TASK_LENGTH} символов.")
                return

            try:
                start_date = datetime.datetime.strptime(start_date_str, 'dd.MM.yyyy').date()
                if end_date_str:
                    end_date = datetime.datetime.strptime(end_date_str, 'dd.MM.yyyy').date()
                else:
                    end_date = None


                if end_date and end_date <= start_date:
                    end_date = start_date + datetime.timedelta(days=90)
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат даты. Используйте дд.мм.гггг.')
                return

            new_task = {
                "name": task_name,
                "completed": False,
                "start_date": start_date_str,
                "end_date": end_date.strftime('%d.%m.%Y') if end_date else None,
                "days": selected_days,
                "tag": tag,
                "completed_dates": []
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
        weekly_tasks_style = weekly_tasks_button_style()
        tag_style = tag_button_style()

        styles = get_task_group_styles()

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

            if task.get('daily', False):
                btn_style = daily_tasks_style
            elif task.get('weekly', False):
                btn_style = weekly_tasks_style
            else:
                btn_style = tasks_style

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
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.edit_task(t, b_index))

            delete_btn = QPushButton("✖️", self)
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet(styles["delete_button_style"])
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.clicked.connect(lambda _, t=task, b_index=button_index: self.delete_task(t, b_index))

            task_layout.addWidget(btn)
            task_layout.addWidget(checkbox)
            task_layout.addWidget(tag_button)
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
                print(f"Редактируемая задача до изменений: {task}")
                print(f"Новое имя задачи: {new_name}")

                old_name = task['name']
                task['name'] = new_name

                if task.get('daily'):
                    for daily_task in self.daily_tasks_data.values():
                        if daily_task['name'] == old_name:
                            daily_task['name'] = new_name
                            break
                elif task.get('weekly'):
                    for weekly_task in self.weekly_tasks_data.values():
                        if weekly_task['name'] == old_name:
                            weekly_task['name'] = new_name
                            break
                else:
                    for year_name, months in self.tasks_data.items():
                        for month_name, month_data in months.items():
                            for t in month_data["tasks"]:
                                if t['name'] == old_name:
                                    t['name'] = new_name
                                    break

                self.save_tasks_to_file()

                self.update_task_layout()

                print(f"Задача '{old_name}' была успешно изменена на '{new_name}'")

    def delete_task(self, task, button_index):
        try:
            task_name = task['name']

            if task.get('daily'):
                if task_name in self.daily_tasks_data:
                    del self.daily_tasks_data[task_name]
                    print(f"Deleted daily task: {task_name}")
                else:
                    print(f"Daily task '{task_name}' not found in daily_tasks_data.")

            elif task.get('weekly'):
                if task_name in self.weekly_tasks_data:
                    del self.weekly_tasks_data[task_name]
                    print(f"Deleted weekly task: {task_name}")
                else:
                    print(f"Weekly task '{task_name}' not found in weekly_tasks_data.")

            else:
                task_date = task.get('date')
                if task_date:
                    for year_name, months in self.tasks_data.items():
                        for month_name, month_data in months.items():
                            month_data["tasks"] = [
                                t for t in month_data["tasks"] if t['name'] != task_name
                            ]
                            print(f"Deleted regular task: {task_name}")

            self.save_tasks_to_file()

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
        day_of_week_mapping = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }

        tasks_widget = self.scroll_area.widget()
        if tasks_widget is None:
            print("Ошибка: tasks_widget не существует.")
            return

        layout = tasks_widget.layout()
        if layout is None:
            print("Ошибка: layout не существует.")
            return

        self.clear_layout(layout)

        week_tasks = {self.current_week_start + datetime.timedelta(days=i): [] for i in range(7)}

        for task_name, task in self.daily_tasks_data.items():
            if 'name' not in task:
                continue

            completed_dates = task.get('completed_dates', [])
            start_date_str = task.get('start_date')
            end_date_str = task.get('end_date')

            if start_date_str and end_date_str:
                try:
                    start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').date()
                    end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
                    current_date = max(start_date, self.current_week_start)

                    while current_date <= end_date and current_date <= self.current_week_end:
                        daily_task = task.copy()
                        daily_task['date'] = current_date.strftime('%d.%m.%Y')
                        daily_task['daily'] = True
                        daily_task['completed'] = daily_task['date'] in completed_dates
                        week_tasks[current_date].append(daily_task)
                        current_date += datetime.timedelta(days=1)

                except ValueError:
                    print(f"Некорректный формат даты для ежедневной задачи: {start_date_str} или {end_date_str}")

        for task_name, task in self.weekly_tasks_data.items():
            if 'name' not in task:
                print(f"Пропускаем задачу без имени: {task}")
                continue

            if 'start_date' in task and 'end_date' in task and 'days' in task:
                start_date_str = task['start_date']
                end_date_str = task['end_date']
                task_days = task['days']

                try:
                    start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').date()
                    end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
                    current_date = start_date

                    while current_date <= end_date:
                        if self.current_week_start <= current_date <= self.current_week_end:
                            day_name = current_date.strftime('%A')
                            if day_name in task_days or self.day_mapping.get(day_name) in task_days:
                                weekly_task = task.copy()
                                weekly_task['date'] = current_date.strftime('%d.%m.%Y')
                                weekly_task['weekly'] = True
                                week_tasks[current_date].append(weekly_task)
                        current_date += datetime.timedelta(days=1)

                except ValueError:
                    print(f"Некорректный формат даты для задачи '{task_name}': {start_date_str} или {end_date_str}")
        for year_name, months in self.tasks_data.items():
            for month_name, month_data in months.items():
                for task in month_data["tasks"]:
                    if isinstance(task, dict) and 'name' in task:
                        task_date = task.get('date', '')
                        if task_date:
                            try:
                                task_date_obj = datetime.datetime.strptime(task_date, '%d.%m.%Y').date()
                                if self.current_week_start <= task_date_obj <= self.current_week_end:
                                    regular_task = task.copy()
                                    regular_task['regular'] = True
                                    week_tasks[task_date_obj].append(regular_task)
                            except ValueError:
                                print(f"Некорректный формат даты для задачи: {task_date}")
        for i in range(7):
            day_date = self.current_week_start + datetime.timedelta(days=i)
            day_tasks = week_tasks[day_date]
            day_label = QLabel(day_of_week_mapping[i], self)
            layout.addWidget(day_label)

            if day_tasks:
                self.add_tasks_to_layout(layout, day_tasks, None, self.current_button_index)
            else:
                layout.addWidget(QLabel("Нет задач на этот день", self))

        print("Задачи успешно обновлены и отрисованы")


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
