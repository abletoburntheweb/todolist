import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QMessageBox, QCheckBox
from ui_elements import setup_ui_elements
from styles import get_task_group_styles, main_window_style, add_tasks_button_style, tasks_button_style, \
    subtasks_button_style

MAX_TASK_LENGTH = 150
MAX_LONG_TERM_TASKS_COUNT = 2
MAX_SUBTASKS_COUNT = 4


class LongTermTasksPage:
    def __init__(self, main_win):
        self.main_win = main_win
        self.long_term_tasks = []

        self.load_long_term_tasks_from_file()

    def setup_ui(self):
        self.main_win.clear_window(keep_main_buttons=True)
        self.main_win.setFixedSize(500, 700)
        add_task_style = add_tasks_button_style()

        self.long_term_tasks_label = QLabel("Долгосрочные задачи", self.main_win)
        self.long_term_tasks_label.setGeometry(20, 30, 460, 30)
        self.long_term_tasks_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.long_term_tasks_label.show()

        self.add_long_term_task_button = QPushButton("Добавить долгосрочную задачу", self.main_win)
        self.add_long_term_task_button.setGeometry(20, 70, 460, 40)
        self.add_long_term_task_button.setStyleSheet(add_task_style)
        self.add_long_term_task_button.clicked.connect(self.add_long_term_task_input)
        self.add_long_term_task_button.show()

        self.add_task_group()
        setup_ui_elements(self.main_win)

    def load_long_term_tasks_from_file(self):
        try:
            with open('long_term_tasks.json', 'r', encoding='utf-8') as file:
                self.long_term_tasks = json.load(file)

                for task in self.long_term_tasks:
                    task['completed'] = False
        except FileNotFoundError:
            self.long_term_tasks = []
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', f'Не удалось загрузить долгосрочные задачи: {e}')

    def save_long_term_tasks_to_file(self):
        try:
            with open('long_term_tasks.json', 'w', encoding='utf-8') as file:
                json.dump(self.long_term_tasks, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', f'Не удалось сохранить долгосрочные задачи: {e}')

    def add_long_term_task_input(self):
        text, ok = QInputDialog.getText(self.main_win, 'Добавить долгосрочную задачу', 'Введите название задачи:')
        if ok and text:
            if len(text) > MAX_TASK_LENGTH:
                QMessageBox.warning(self.main_win, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            new_task = {"name": text, "completed": False}
            self.long_term_tasks.append(new_task)
            self.save_long_term_tasks_to_file()
            self.setup_ui()

    def add_subtask_input(self, task):
        if 'subtasks' not in task:
            task['subtasks'] = []
        if len(task['subtasks']) >= MAX_SUBTASKS_COUNT:
            QMessageBox.warning(self.main_win, 'Ошибка', 'Вы не можете добавить более 3 подзадач.')
            return

        text, ok = QInputDialog.getText(self.main_win, 'Добавить подзадачу', 'Введите название подзадачи:')
        if ok and text:
            if len(text) > MAX_TASK_LENGTH:
                QMessageBox.warning(self.main_win, 'Ошибка', 'Название подзадачи должно быть не более 150 символов.')
                return
            subtask = {"name": text, "completed": False}
            if 'subtasks' not in task:
                task['subtasks'] = []
            task['subtasks'].append(subtask)
            self.save_long_term_tasks_to_file()
            self.setup_ui()

    def add_task_group(self):
        styles = get_task_group_styles()
        tasks_style = tasks_button_style()
        sub_tasks_style = subtasks_button_style()

        y_start = 120
        task_button_width = 310
        task_button_height = 40
        button_spacing = 5
        checkbox_width = 20
        checkbox_x = 340
        add_subtask_btn_x = checkbox_x + checkbox_width + button_spacing
        edit_btn_x = add_subtask_btn_x + 30 + button_spacing
        delete_btn_x = edit_btn_x + 30 + button_spacing
        subtask_indentation = 25  # Добавляем отступ для подзадач

        for i, task in enumerate(self.long_term_tasks):
            task_name = task['name']
            btn = QPushButton(task_name, self.main_win)
            btn.setGeometry(25, y_start, task_button_width, task_button_height)
            btn.setStyleSheet(tasks_style)
            btn.clicked.connect(lambda _, t=task: self.show_task_full_title(t))
            btn.show()

            checkbox = QCheckBox(self.main_win)
            checkbox.setChecked(task.get('completed', False))
            checkbox.setGeometry(checkbox_x, y_start + 10, 20, 20)
            checkbox.setStyleSheet(styles["checkbox_style"])
            checkbox.stateChanged.connect(
                lambda state, t=task: self.toggle_task_completed(t, state == QtCore.Qt.Checked))
            checkbox.show()

            add_subtask_button = QPushButton("+", self.main_win)
            add_subtask_button.setGeometry(add_subtask_btn_x, y_start, 30, 30)
            add_subtask_button.setStyleSheet(styles["add_subtask_button_style"])
            add_subtask_button.clicked.connect(lambda checked, t=task: self.add_subtask_input(t))
            add_subtask_button.setEnabled(len(task.get('subtasks', [])) < MAX_SUBTASKS_COUNT)
            add_subtask_button.show()

            edit_button = QPushButton("✎", self.main_win)
            edit_button.setGeometry(edit_btn_x, y_start, 30, 30)
            edit_button.setStyleSheet(styles["edit_button_style"])
            edit_button.clicked.connect(lambda _, t=task: self.edit_task(t))
            edit_button.show()

            delete_button = QPushButton("✖", self.main_win)
            delete_button.setGeometry(delete_btn_x, y_start, 30, 30)
            delete_button.setStyleSheet(styles["delete_button_style"])
            delete_button.clicked.connect(lambda _, t=task: self.delete_task(t))
            delete_button.show()

            y_start += task_button_height + button_spacing

            if 'subtasks' in task:
                for j, subtask in enumerate(task['subtasks']):
                    subtask_name = subtask['name']
                    sub_btn = QPushButton(subtask_name, self.main_win)
                    sub_btn.setGeometry(25 + subtask_indentation, y_start, task_button_width - subtask_indentation,
                                        task_button_height)

                    sub_btn.setStyleSheet(sub_tasks_style)

                    sub_btn.clicked.connect(lambda _, t=subtask: self.show_task_full_title(t))
                    sub_btn.show()

                    sub_checkbox = QCheckBox(self.main_win)
                    sub_checkbox.setChecked(subtask.get('completed', False))
                    sub_checkbox.setGeometry(checkbox_x, y_start + 10, checkbox_width, 20)
                    sub_checkbox.setStyleSheet(styles["checkbox_style"])
                    sub_checkbox.stateChanged.connect(
                        lambda state, t=subtask: self.toggle_task_completed(t, state == QtCore.Qt.Checked))
                    sub_checkbox.show()

                    # X координаты кнопок редактирования и удаления подзадачи выровнены с кнопками основной задачи
                    sub_edit_button = QPushButton("✎", self.main_win)
                    sub_edit_button.setGeometry(edit_btn_x, y_start, 30, 30)
                    sub_edit_button.setStyleSheet(styles["edit_button_style"])
                    sub_edit_button.clicked.connect(lambda _, t=subtask: self.edit_task(t))
                    sub_edit_button.show()

                    sub_delete_button = QPushButton("✖", self.main_win)
                    sub_delete_button.setGeometry(delete_btn_x, y_start, 30, 30)
                    sub_delete_button.setStyleSheet(styles["delete_button_style"])
                    sub_delete_button.clicked.connect(lambda _, t=subtask, p=task: self.delete_subtask(p, t))
                    sub_delete_button.show()

                    y_start += task_button_height + button_spacing

    def toggle_task_completed(self, task, completed):
        # Устанавливаем состояние выполнения для основной задачи
        task['completed'] = completed
        # Если основная задача отмечена как выполненная, отмечаем все подзадачи тоже
        if 'subtasks' in task:
            for subtask in task['subtasks']:
                subtask['completed'] = completed
        self.save_long_term_tasks_to_file()
        self.setup_ui()


    def edit_task(self, task):
        new_name, ok = QInputDialog.getText(self.main_win, 'Редактировать задачу', 'Введите новое название задачи:',
                                            text=task['name'])
        if ok and new_name:
            if len(new_name) > MAX_TASK_LENGTH:
                QMessageBox.warning(self.main_win, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            task['name'] = new_name
            self.save_long_term_tasks_to_file()
            self.setup_ui()


    def delete_task(self, task):
        self.long_term_tasks = [t for t in self.long_term_tasks if t['name'] != task['name']]
        self.save_long_term_tasks_to_file()
        self.setup_ui()

    def delete_subtask(self, parent_task, subtask_to_delete):
        parent_task['subtasks'] = [subtask for subtask in parent_task['subtasks'] if subtask != subtask_to_delete]
        self.save_long_term_tasks_to_file()
        self.setup_ui()
    def show_task_full_title(self, task):
        QMessageBox.information(self.main_win, 'Полное название задачи', task['name'])
