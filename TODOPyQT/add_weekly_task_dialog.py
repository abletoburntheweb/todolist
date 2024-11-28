from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QDialogButtonBox, QDateEdit, QComboBox, \
    QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from styles import task_name_input_style, date_input_style, tag_selector_style, dialog_button_box_style, calendar_styles


class AddWeeklyTaskDialog(QDialog):
    def __init__(self, tags, parent=None, task_name='', task_tags=''):
        super().__init__(parent)
        self.setWindowTitle("Добавить еженедельную задачу")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Введите название задачи")
        self.task_name_input.setStyleSheet(task_name_input_style())
        self.task_name_input.setFont(QFont('Arial', 12))
        self.task_name_input.setText(task_name)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("dd.MM.yyyy")
        self.start_date_input.setStyleSheet(date_input_style())
        self.start_date_input.setFont(QFont('Arial', 12))
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.calendarWidget().setStyleSheet(calendar_styles())

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("dd.MM.yyyy")
        self.end_date_input.setStyleSheet(date_input_style())
        self.end_date_input.setFont(QFont('Arial', 12))
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.calendarWidget().setStyleSheet(calendar_styles())

        self.tag_selector = QComboBox(self)
        self.tag_selector.setEditable(True)
        self.tag_selector.addItem('')
        self.tag_selector.addItems(tags)
        self.tag_selector.setStyleSheet(tag_selector_style())
        self.tag_selector.setFont(QFont('Arial', 12))
        index = self.tag_selector.findText(task_tags)
        if index != -1:
            self.tag_selector.setCurrentIndex(index)
        else:
            self.tag_selector.setEditText(task_tags)

        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        days_layout = QGridLayout()
        self.days_checkboxes = []
        row, col = 0, 0
        for i, day in enumerate(days):
            checkbox = QCheckBox(day)
            checkbox.setFont(QFont('Arial', 12))
            self.days_checkboxes.append(checkbox)
            days_layout.addWidget(checkbox, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.button_box.button(QDialogButtonBox.Ok).setText('ОК')
        self.button_box.button(QDialogButtonBox.Cancel).setText('Отменить')

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(dialog_button_box_style())
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(dialog_button_box_style())

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название задачи:", self))
        layout.addWidget(self.task_name_input)
        layout.addWidget(QLabel("Дата начала:", self))
        layout.addWidget(self.start_date_input)
        layout.addWidget(QLabel("Дата окончания:", self))
        layout.addWidget(self.end_date_input)
        layout.addWidget(QLabel("Тег:", self))
        layout.addWidget(self.tag_selector)

        layout.addWidget(QLabel("Дни недели:", self))
        layout.addLayout(days_layout)

        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_task_data(self):
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]
        task_name = self.task_name_input.text().strip()
        task_start_date = self.start_date_input.date().toString('dd.MM.yyyy')

        task_end_date = self.end_date_input.date().toString('dd.MM.yyyy') if self.end_date_input.date().isValid() else ""

        task_tags = self.tag_selector.currentText().strip()

        if not task_name:
            QMessageBox.warning(self, 'Ошибка', 'Название задачи не может быть пустым.')
            return None

        if not selected_days:
            QMessageBox.warning(self, 'Ошибка', 'Выберите хотя бы один день для еженедельной задачи.')
            return None

        return task_name, task_start_date, task_end_date, selected_days, task_tags

