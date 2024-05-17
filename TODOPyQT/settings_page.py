import json
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox

def SettingsPage(main_window):
    print("Button 3 clicked")
    main_window.clear_window()
    main_window.setFixedSize(500, 700)

    font_size_label = QLabel("Размер шрифта", main_window)
    font_size_label.setGeometry(50, 50, 150, 30)
    font_size_label.show()

    font_size_input = QLineEdit(main_window)
    font_size_input.setGeometry(200, 50, 50, 30)
    font_size_input.setText(str(main_window.current_font_size))
    font_size_input.setMaxLength(2)
    font_size_input.show()

    save_font_size_button = QPushButton("Сохранить", main_window)
    save_font_size_button.setGeometry(260, 50, 120, 30)
    save_font_size_button.clicked.connect(lambda: apply_font_size_from_input(main_window))
    save_font_size_button.show()

    background_image_label = QLabel("Задний фон", main_window)
    background_image_label.setGeometry(50, 150, 200, 30)
    background_image_label.show()

    background_image_dropdown = QComboBox(main_window)
    background_image_dropdown.setGeometry(250, 150, 200, 30)
    background_image_dropdown.addItems(
        ["background1.png", "background2.png", "background3.png", "background4.png", "background5.png"])
    background_image_dropdown.currentIndexChanged.connect(
        lambda: on_background_image_changed(main_window, background_image_dropdown.currentText()))
    background_image_dropdown.show()

def on_background_image_changed(main_window, image_file):
    image_path = f"{image_file}"
    if main_window.apply_background_image(image_path):
        main_window.current_background_image = image_path
        main_window.save_settings()

def apply_font_size_from_input(main_window):
    font_size_str = main_window.font_size_input.text()

    try:
        font_size = int(font_size_str)
    except ValueError:
        QMessageBox.warning(main_window, 'Ошибка', 'Введите корректный размер шрифта.')
        return

    if 5 <= font_size <= 32:
        main_window.current_font_size = font_size
        main_window.apply_font_size_style()  # Apply font size to all relevant elements
        main_window.save_settings()
    else:
        QMessageBox.warning(main_window, 'Ошибка', 'Размер шрифта должен быть между 5 и 32.')