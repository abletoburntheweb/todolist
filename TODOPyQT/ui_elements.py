from PyQt5.QtWidgets import QPushButton, QLabel

def setup_ui_elements(main_window):
    bottom_panel_height = 70
    bottom_panel_y_position = main_window.height() - bottom_panel_height

    rect_view = QLabel(main_window)
    rect_view.setGeometry(0, bottom_panel_y_position, main_window.width(), bottom_panel_height)
    rect_view.setStyleSheet('background-color: #F2FAFD;')
    rect_view.show()

    button_width = 50
    button_height = 50
    buttons_spacing = (main_window.width() - (3 * button_width)) // 4

    button1 = QPushButton(main_window)
    button1.setGeometry(buttons_spacing, bottom_panel_y_position + 10, button_width, button_height)
    button1.setStyleSheet("background-color: #F2FAFD; border-image: url('listcheck.png');")
    button1.clicked.connect(main_window.main_page)

    button2 = QPushButton(main_window)
    button2.setGeometry(buttons_spacing * 2 + button_width, bottom_panel_y_position + 10, button_width, button_height)
    button2.setStyleSheet("background-color: #F2FAFD; border-image: url('note.png');")
    button2.clicked.connect(main_window.show_note_page)

    button3 = QPushButton(main_window)
    button3.setGeometry(buttons_spacing * 3 + (button_width * 2), bottom_panel_y_position + 10, button_width, button_height)
    button3.setStyleSheet("background-color: #F2FAFD; border-image: url('settings.png');")
    button3.clicked.connect(main_window.settings_page)

    button1.show()
    button2.show()
    button3.show()