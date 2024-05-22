from PyQt5.QtWidgets import QComboBox, QLabel

def weekend_dropdown(parent):
    weekend_label = QLabel("Day of the Week", parent)
    weekend_label.move(50, 25)  # Adjust the position as needed
    weekend_label.show()

    days_of_week_dropdown = QComboBox(parent)
    days_of_week_dropdown.addItem("Monday")
    days_of_week_dropdown.addItem("Tuesday")
    days_of_week_dropdown.addItem("Wednesday")
    days_of_week_dropdown.addItem("Thursday")
    days_of_week_dropdown.addItem("Friday")
    days_of_week_dropdown.addItem("Saturday")
    days_of_week_dropdown.addItem("Sunday")
    days_of_week_dropdown.move(50, 50)
    days_of_week_dropdown.show()

    return weekend_label, weekend_dropdown