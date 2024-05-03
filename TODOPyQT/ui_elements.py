from PyQt5.QtWidgets import QPushButton, QLabel

def setup_ui_elements(main_window):
    rect_view = QLabel(main_window)
    rect_view.setGeometry(0, 630, 500, 70)
    rect_view.setStyleSheet('background-color: #F2FAFD;')
    rect_view.show()

    button1 = QPushButton(main_window)
    button1.setGeometry(100, 640, 50, 50)
    button1.setStyleSheet("background-color: #F2FAFD; border-image: url('listcheck.png');")
    button1.clicked.connect(main_window.main_page)

    button2 = QPushButton(main_window)
    button2.setGeometry(350, 640, 50, 50)
    button2.setStyleSheet("background-color: #F2FAFD; border-image: url('note.png');")
    button2.clicked.connect(main_window.show_note_page)

    button3 = QPushButton(main_window)
    button3.setGeometry(450, 640, 50, 50)
    button3.setStyleSheet("background-color: #F2FAFD; border-image: url('settings.png');")
    button3.clicked.connect(main_window.settings_page)

    button1.show()
    button2.show()
    button3.show()