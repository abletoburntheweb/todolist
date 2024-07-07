from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, QDateEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from styles import task_name_input_style, date_input_style, tag_selector_style, dialog_button_box_style, calendar_styles

class AddTaskDialog(QDialog):
    def __init__(self, tags, parent=None, task_name='', task_date='', task_tag=''):
        super().__init__(parent)
        self.setWindowTitle("Добавить задачу" if not task_name else "Редактировать задачу")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Введите название задачи")
        self.task_name_input.setStyleSheet(task_name_input_style())
        self.task_name_input.setFont(QFont('Arial', 12))
        self.task_name_input.setText(task_name)

        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd.MM.yyyy")
        self.date_input.setStyleSheet(date_input_style())
        self.date_input.setFont(QFont('Arial', 12))
        self.date_input.setDate(QDate.currentDate())
        self.date_input.calendarWidget().setStyleSheet(calendar_styles())

        self.tag_selector = QComboBox(self)
        self.tag_selector.setEditable(True)
        self.tag_selector.addItem('')
        self.tag_selector.addItems(tags)
        self.tag_selector.setStyleSheet(tag_selector_style())
        self.tag_selector.setFont(QFont('Arial', 12))
        index = self.tag_selector.findText(task_tag)
        if index != -1:
            self.tag_selector.setCurrentIndex(index)
        else:
            self.tag_selector.setEditText(task_tag)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(dialog_button_box_style())
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(dialog_button_box_style())

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название задачи:", self))
        layout.addWidget(self.task_name_input)
        layout.addWidget(QLabel("Дата (dd.MM.yyyy):", self))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Тег:", self))
        layout.addWidget(self.tag_selector)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_task_data(self):
        task_name = self.task_name_input.text()
        task_date = self.date_input.date().toString('dd.MM.yyyy')
        task_tag = self.tag_selector.currentText()
        return task_name, task_date, task_tag