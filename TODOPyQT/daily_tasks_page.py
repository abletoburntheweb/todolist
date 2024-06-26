import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QMessageBox, QCheckBox, QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox
from ui_elements import setup_ui_elements
from styles import get_task_group_styles, main_window_style, add_tasks_button_style, tasks_button_style

MAX_TASK_LENGTH = 150
MAX_DAILY_TASKS_COUNT = 10


class EditTaskDialog(QDialog):
    def __init__(self, initial_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать задачу")

        layout = QVBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(initial_text)
        layout.addWidget(self.line_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отменить")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_text(self):
        return self.line_edit.text()


class DailyTasksPage:
    def __init__(self, main_win):
        self.main_win = main_win

        self.load_daily_tasks_from_file()

    def setup_ui(self):
        self.main_win.clear_window(keep_main_buttons=True)
        self.main_win.setFixedSize(500, 700)
        add_task_style = add_tasks_button_style()

        self.daily_tasks_label = QLabel("Ежедневные задачи", self.main_win)
        self.daily_tasks_label.setGeometry(20, 30, 460, 30)
        self.daily_tasks_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.daily_tasks_label.show()

        self.add_daily_task_button = QPushButton("Добавить ежедневную задачу", self.main_win)
        self.add_daily_task_button.setGeometry(20, 70, 460, 40)
        self.add_daily_task_button.setStyleSheet(add_task_style)

        self.add_daily_task_button.clicked.connect(self.add_daily_task_input)
        self.add_daily_task_button.show()

        self.add_task_group()
        setup_ui_elements(self.main_win)

    def load_daily_tasks_from_file(self):
        try:
            with open('daily_tasks.json', 'r', encoding='utf-8') as file:
                self.daily_tasks = json.load(file)

                for task in self.daily_tasks:
                    task['completed'] = False
        except FileNotFoundError:
            self.daily_tasks = []
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', f'Не удалось загрузить ежедневные задачи: {e}')

    def save_daily_tasks_to_file(self):
        try:
            with open('daily_tasks.json', 'w', encoding='utf-8') as file:
                json.dump(self.daily_tasks, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', f'Не удалось сохранить ежедневные задачи: {e}')

    def add_daily_task_input(self):
        print("Добавляем ежедневную задачу...")
        if len(self.daily_tasks) >= MAX_DAILY_TASKS_COUNT:
            QMessageBox.warning(self.main_win, 'Ошибка', 'Вы не можете добавить более 10 ежедневных задач.')
            return

        text, ok = QInputDialog.getText(self.main_win, 'Добавить ежедневную задачу', 'Введите название задачи:')
        if ok and text:
            if len(text) > MAX_TASK_LENGTH:
                QMessageBox.warning(self.main_win, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            new_task = {"name": text, "completed": False}
            self.daily_tasks.append(new_task)
            self.save_daily_tasks_to_file()
            self.setup_ui()

    def add_task_group(self):
        y_start = 120
        tasks_style = tasks_button_style()
        styles = get_task_group_styles()

        btn_width = 350
        checkbox_x = 380
        edit_btn_x = 420
        delete_btn_x = 460

        for i, task in enumerate(self.daily_tasks):
            task_name = task['name']
            btn = QPushButton(task_name, self.main_win)
            btn.setGeometry(25, y_start + i * 50, btn_width, 40)
            btn.setStyleSheet(tasks_style)
            btn.clicked.connect(lambda _, t=task: self.show_task_full_title(t))
            btn.show()

            checkbox = QCheckBox(self.main_win)
            checkbox.setChecked(task.get('completed', False))
            checkbox.setGeometry(checkbox_x, y_start + i * 50 + 10, 20, 20)
            checkbox.setStyleSheet(styles["checkbox_style"])
            checkbox.stateChanged.connect(
                lambda state, t=task: self.toggle_task_completed(t, state == QtCore.Qt.Checked))
            checkbox.show()

            edit_button = QPushButton("✎", self.main_win)
            edit_button.setGeometry(edit_btn_x, y_start + i * 50, 30, 30)
            edit_button.setStyleSheet(styles["edit_button_style"])
            edit_button.clicked.connect(lambda _, t=task: self.edit_task(t))
            edit_button.show()

            delete_button = QPushButton("✖", self.main_win)
            delete_button.setGeometry(delete_btn_x, y_start + i * 50, 30, 30)
            delete_button.setStyleSheet(styles["delete_button_style"])
            delete_button.clicked.connect(lambda _, t=task: self.delete_task(t))
            delete_button.show()

    def toggle_task_completed(self, task, completed):
        task['completed'] = completed
        self.save_daily_tasks_to_file()
        self.setup_ui()

    def edit_task(self, task):
        dialog = EditTaskDialog(task['name'], self.main_win)
        if dialog.exec_() == QDialog.Accepted:
            new_name = dialog.get_text()
            if len(new_name) > MAX_TASK_LENGTH:
                QMessageBox.warning(self.main_win, 'Ошибка', 'Название задачи должно быть не более 150 символов.')
                return
            for t in self.daily_tasks:
                if t['name'] == task['name']:
                    t['name'] = new_name
                    break
            self.save_daily_tasks_to_file()
            self.add_task_group()

    def delete_task(self, task):
        try:
            self.daily_tasks = [t for t in self.daily_tasks if t['name'] != task['name']]
            self.save_daily_tasks_to_file()
            self.setup_ui()
        except Exception as e:
            QMessageBox.warning(self.main_win, 'Ошибка', 'Задача не найдена для удаления.')
            print(f'Ошибка', f'Ошибка при удалении задачи: {e}')

    def show_task_full_title(self, task):
        QMessageBox.information(self.main_win, 'Task', task['name'])