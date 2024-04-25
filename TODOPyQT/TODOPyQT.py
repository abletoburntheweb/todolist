from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QIcon, QPixmap, QDrag
import json

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
            self.important_tasks = tasks_data.get("important_tasks", [])
            self.additional_tasks = tasks_data.get("additional_tasks", [])
            self.tasks_high_priority = tasks_data.get("tasks_high_priority", [])
            self.tasks_low_priority = tasks_data.get("tasks_low_priority", [])

        self.main_screen()

    def save_tasks_to_file(self):
        tasks_data = {
            "important_tasks": self.important_tasks,
            "additional_tasks": self.additional_tasks,
            "tasks_high_priority": self.tasks_high_priority,
            "tasks_low_priority": self.tasks_low_priority
        }
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=4)

    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Important Task', 'Enter task:')
        if ok and text:
            self.tasks_high_priority.append(text)
            self.save_tasks_to_file()
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Additional Task', 'Enter task:')
        if ok and text:
            self.tasks_low_priority.append(text)
            self.save_tasks_to_file()
            self.main_screen()

    def ui_elements(self):
        rect_view = QLabel(self)
        rect_view.setGeometry(0, 630, 500, 70)
        rect_view.setStyleSheet('background-color: #F2FAFD;')
        rect_view.show()

        button1 = QPushButton(self)
        button1.setGeometry(100, 640, 50, 50)
        button1.setStyleSheet("background-color: #F2FAFD; border-image: url('listcheck.png');")
        button1.clicked.connect(self.main_page)

        button2 = QPushButton(self)
        button2.setGeometry(350, 640, 50, 50)
        button2.setStyleSheet("background-color: #F2FAFD; border-image: url('note.png');")
        button2.clicked.connect(self.note_page)

        button3 = QPushButton(self)
        button3.setGeometry(450, 640, 50, 50)
        button3.setStyleSheet("background-color: #F2FAFD; border-image: url('settings.png');")
        button3.clicked.connect(self.settings_page)


        button1.show()
        button2.show()
        button3.show()


    def main_screen(self):
        self.clear_window()
        self.setFixedSize(500, 700)


        self.text1 = QtWidgets.QLabel("HIGH", self)
        self.text1.move(220, 50)
        self.text1.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text1.adjustSize()

        self.add_task_group(self.important_tasks, 100, True)
        self.add_task_group(self.tasks_high_priority, 150, False)

        self.text2 = QtWidgets.QLabel("LOW", self)
        self.text2.move(220, 300)
        self.text2.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text2.adjustSize()

        self.add_task_group(self.additional_tasks, 350, True)
        self.add_task_group(self.tasks_low_priority, 400, False)

        self.text1.show()
        self.text2.show()
        self.ui_elements()


    def main_page(self):
        print("Button 1 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)
        self.main_screen()


    def note_page(self):
        print("Button 2 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        notes_label = QtWidgets.QLabel("Заметки", self)
        notes_label.setGeometry(200, 50, 100, 30)
        notes_label.setStyleSheet("font-size: 20px; color: #000000;")

        notes_text_edit = QtWidgets.QTextEdit(self)
        notes_text_edit.setGeometry(50, 100, 400, 400)
        notes_text_edit.setStyleSheet("font-size: 14px;")

        save_notes_button = QPushButton("Сохранить", self)
        save_notes_button.setGeometry(200, 530, 100, 50)
        save_notes_button.clicked.connect(lambda: self.save_notes(notes_text_edit.toPlainText()))

        notes_label.show()
        notes_text_edit.show()
        save_notes_button.show()
        self.ui_elements()


    def settings_page(self):
        print("Button 3 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        dark_mode_checkbox = QtWidgets.QCheckBox('Dark Mode', self)
        dark_mode_checkbox.setGeometry(200, 50, 100, 30)
        dark_mode_checkbox.setStyleSheet("color: white; font-size: 14px;")

        def toggle_dark_mode(checked):
            if checked:
                self.setStyleSheet("background-color: #1E1E1E; color: white;")
            else:
                self.setStyleSheet("background-color: white; color: black;")

        dark_mode_checkbox.stateChanged.connect(toggle_dark_mode)

        dark_mode_checkbox.show()
        self.ui_elements()

    def add_task_group(self, tasks, y_start, is_important):
        for i, task in enumerate(tasks):
            if task in ["Добавить важных дел", "Добавить дел"]:
                btn = QtWidgets.QPushButton(task, self)
                btn.setGeometry(25, y_start + i * 50, 450, 40)
                checkbox = None
                delete_btn = None
            else:
                btn = QtWidgets.QPushButton(task, self)
                btn.setGeometry(25, y_start + i * 50, 450, 40)

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setGeometry(40, y_start + i * 50 + 10, 30, 30)

                checkbox.setStyleSheet(
                    "QCheckBox::indicator { width: 25px; height: 25px; border-radius: 15px; border: 3px solid #989898;}"
                    "QCheckBox::indicator:checked { background-color: #808080;}"
                    "QCheckBox::indicator:unchecked { background-color: white;}"
                )

                delete_btn = QtWidgets.QPushButton("☓", self)
                delete_btn.setGeometry(430, y_start + i * 50 + 10, 25, 25)
                delete_btn.setStyleSheet("background-color: #FF0000; color: white;")
                delete_btn.clicked.connect(lambda _, t=task: self.delete_task(t, is_important))

            if task in ["Добавить важных дел", "Добавить дел"]:
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: #BBBBBB; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")
                if task == "Добавить важных дел":
                    btn.clicked.connect(self.add_important_task_input)
                elif task == "Добавить дел":
                    btn.clicked.connect(self.add_additional_task_input)
            else:
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: black; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")

            btn.show()
            if checkbox:
                checkbox.show()
            if delete_btn:
                delete_btn.show()



    def delete_task(self, task, is_important):
        try:
            if is_important:
                self.tasks_high_priority.remove(task)
            else:
                self.tasks_low_priority.remove(task)
            self.save_tasks_to_file()

            # Clear the window and then redraw the task groups
            self.clear_window()
            self.main_screen()
        except ValueError as e:
            print(f"Error deleting task: {e}")


    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить важных дел', 'Добавить задачу:')
        if ok and text:
            if len(self.tasks_high_priority) < 3:
                self.tasks_high_priority.append(text)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три задачи!')

            self.save_tasks_to_file()
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить дел', 'Добавить задачу:')
        if ok and text:
            if len(self.tasks_low_priority) < 3:
                self.tasks_low_priority.append(text)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три задачи!')

            self.save_tasks_to_file()
            self.main_screen()

    def clear_window(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.deleteLater()


def run_app():
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run_app()