from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Справка')
        self.setFixedSize(500, 700)
        layout = QVBoxLayout(self)

        try:
            help_image = QPixmap("How To Use2.png")
            if help_image.isNull():
                raise IOError("Не удалось загрузить изображение.")
            image_label = QLabel()
            image_label.setPixmap(help_image.scaled(480, 680, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            error_label = QLabel(f"Произошла ошибка: {e}")
            layout.addWidget(error_label)

        self.setLayout(layout)