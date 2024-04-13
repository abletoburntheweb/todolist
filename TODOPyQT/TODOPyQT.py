from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)

        self.important_tasks = ["Добавить важных дел"]
        self.additional_tasks = ["Добавить дел"]

        self.tasks_high_priority = [
            "Помыть посуду",
            "Сверстать этот TODO list",
            "Начать делать задачу"
        ]

        self.tasks_low_priority = [
            "Записаться к стоматологу"
        ]

        self.main_screen()

    def main_screen(self):
        self.clear_tasks()
        self.setFixedSize(500, 700)

        rect_view = QLabel(self)
        rect_view.setGeometry(0, 630, 500, 70)
        rect_view.setStyleSheet('background-color: #F2FAFD;')
        rect_view.show()

        self.text1 = QtWidgets.QLabel("HIGH", self)
        self.text1.move(220, 50)
        self.text1.setStyleSheet("font-size: 15pt; color: f7dfea;")
        self.text1.adjustSize()

        self.add_task_group(self.important_tasks, 100, True)
        self.add_task_group(self.tasks_high_priority, 150, False)

        self.text2 = QtWidgets.QLabel("LOW", self)
        self.text2.move(220, 300)
        self.text2.setStyleSheet("font-size: 15pt; color: f7dfea;")
        self.text2.adjustSize()

        self.add_task_group(self.additional_tasks, 350, True)
        self.add_task_group(self.tasks_low_priority, 400, False)

    def add_task_group(self, tasks, y_start, is_important):
        for i, task in enumerate(tasks):
            btn = QtWidgets.QPushButton(task, self)
            btn.setGeometry(25, y_start + i * 50, 450, 40)
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

    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Important Task', 'Enter your important task:')
        if ok and text:
            self.important_tasks.append(text)
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Additional Task', 'Enter your additional task:')
        if ok and text:
            self.additional_tasks.append(text)
            self.main_screen()

    def clear_tasks(self):
        for widget in self.findChildren(QtWidgets.QPushButton):
            widget.deleteLater()


def run_app():
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run_app()
