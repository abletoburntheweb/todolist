from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Справка')
        self.setFixedSize(1280, 720)
        layout = QVBoxLayout(self)

        try:
            help_image = QPixmap("How To Use4.png")
            if help_image.isNull():
                raise IOError("Не удалось загрузить изображение.")
            image_label = QLabel()
            image_label.setPixmap(help_image.scaled(1220, 720, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            error_label = QLabel(f"Произошла ошибка: {e}")
            layout.addWidget(error_label)

        self.setLayout(layout)


class RegularTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Обычные задачи')
        self.setFixedSize(1280, 720)
        layout = QVBoxLayout(self)

        try:
            regular_task_image = QPixmap("regular_tasks_info.png")
            if regular_task_image.isNull():
                raise IOError("Не удалось загрузить изображение.")
            image_label = QLabel()
            image_label.setPixmap(regular_task_image.scaled(1280, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)

            info_label = QLabel("Информация о том, как работают обычные задачи")
            info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label)

        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            error_label = QLabel(f"Произошла ошибка: {e}")
            layout.addWidget(error_label)

        self.setLayout(layout)


class DailyTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ежедневные задачи')
        self.setFixedSize(1280, 720)
        layout = QVBoxLayout(self)

        try:
            daily_task_image = QPixmap("daily_tasks_info.png")
            if daily_task_image.isNull():
                raise IOError("Не удалось загрузить изображение.")
            image_label = QLabel()
            image_label.setPixmap(daily_task_image.scaled(1280, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)

            info_label = QLabel("Информация о том, как работают ежедневные задачи")
            info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label)

        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            error_label = QLabel(f"Произошла ошибка: {e}")
            layout.addWidget(error_label)

        self.setLayout(layout)


class WeeklyTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Еженедельные задачи')
        self.setFixedSize(1280, 720)
        layout = QVBoxLayout(self)

        try:
            weekly_task_image = QPixmap("weekly_tasks_info.png")
            if weekly_task_image.isNull():
                raise IOError("Не удалось загрузить изображение.")
            image_label = QLabel()
            image_label.setPixmap(weekly_task_image.scaled(1280, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)

            info_label = QLabel("Информация о том, как работают еженедельные задачи")
            info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(info_label)

        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            error_label = QLabel(f"Произошла ошибка: {e}")
            layout.addWidget(error_label)

        self.setLayout(layout)