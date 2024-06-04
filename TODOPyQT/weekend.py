from PyQt5.QtWidgets import QComboBox, QLabel

def weekend_dropdown(parent):
    weekend_label = QLabel("Дни недели", parent)
    weekend_label.move(50, 25)
    weekend_label.show()

    days_of_week_dropdown = QComboBox(parent)
    days_of_week_dropdown.addItem("Понедельник")
    days_of_week_dropdown.addItem("Вторник")
    days_of_week_dropdown.addItem("Среда")
    days_of_week_dropdown.addItem("Четверг")
    days_of_week_dropdown.addItem("Пятница")
    days_of_week_dropdown.addItem("Суббота")
    days_of_week_dropdown.addItem("Воскресенье")
    days_of_week_dropdown.move(50, 50)
    days_of_week_dropdown.show()

    return weekend_label, weekend_dropdown