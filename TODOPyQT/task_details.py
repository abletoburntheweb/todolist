from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class TaskDetailsDialog(QDialog):
    def __init__(self, task_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Подробности задачи')
        self.setFixedSize(300, 100)
        layout = QVBoxLayout()

        self.task_label = QLabel(task_name, self)
        self.task_label.setWordWrap(True)
        layout.addWidget(self.task_label)

        self.setLayout(layout)