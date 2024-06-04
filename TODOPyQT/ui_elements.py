from PyQt5.QtWidgets import QPushButton, QLabel
def setup_ui_elements(main_window):
    rect_view = QLabel(main_window)
    rect_view.setGeometry(0, 630, 500, 70)
    rect_view.setStyleSheet('background-color: #F2FAFD;')
    rect_view.show()

    # Вычисление позиций для кнопок
    button_width = 50
    button_height = 50
    tabbar_width = 500
    buttons_spacing = (tabbar_width - (3 * button_width)) // 4  # Расстояние между кнопками и краями TabBar

    # Расположение кнопок на равном расстоянии друг от друга
    button1 = QPushButton(main_window)
    button1.setGeometry(buttons_spacing, 640, button_width, button_height)
    button1.setStyleSheet("background-color: #F2FAFD; border-image: url('listcheck.png');")
    button1.clicked.connect(main_window.main_page)

    button2 = QPushButton(main_window)
    button2.setGeometry(buttons_spacing * 2 + button_width, 640, button_width, button_height)
    button2.setStyleSheet("background-color: #F2FAFD; border-image: url('note.png');")
    button2.clicked.connect(main_window.show_note_page)

    button3 = QPushButton(main_window)
    button3.setGeometry(buttons_spacing * 3 + (button_width * 2), 640, button_width, button_height)
    button3.setStyleSheet("background-color: #F2FAFD; border-image: url('settings.png');")
    button3.clicked.connect(main_window.settings_page)

    button1.show()
    button2.show()
    button3.show()