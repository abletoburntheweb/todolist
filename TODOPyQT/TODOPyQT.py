import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, QCheckBox, QMessageBox, \
    QLineEdit, QListWidget, QTextEdit, QListWidgetItem, QComboBox
from PyQt5.QtCore import Qt
from note_page import NotePage
from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)
        self._note_page = NotePage(self)
        self.load_tasks()

        self.current_background_image = "background1.png"
        self.apply_background_image(self.current_background_image)

        self.current_font_size = 14

        self.apply_font_size_style()

        self.load_settings()
        self.save_settings()

        self.main_screen()

        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
            self.important_tasks = tasks_data.get("important_tasks", [])
            self.additional_tasks = tasks_data.get("additional_tasks", [])
            self.tasks_high_priority = tasks_data.get("tasks_high_priority", [])
            self.tasks_low_priority = tasks_data.get("tasks_low_priority", [])

        with open("notes.json", "r", encoding="utf-8") as file:
            notes_data = json.load(file)
            self.notes = notes_data.get("notes", {})

        self.main_screen()

    def save_tasks_to_file(self):
        tasks_data = {
            "important_tasks": self.important_tasks,
            "additional_tasks": self.additional_tasks,
            "tasks_high_priority": self.tasks_high_priority,
            "tasks_low_priority": self.tasks_low_priority
        }
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks_data, file)

    def save_notes_to_file(self):
        title = self.note_title_edit.text()
        notes = self.notes_text_edit.toPlainText()
        if title:
            if title in self.notes:  # Check if the note exists before deleting it
                del self.notes[title]
                try:
                    with open("notes.json", "w", encoding="utf-8") as file:
                        json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)
                    QMessageBox.information(self, 'Сохранено', 'Заметка удалена')
                except Exception as e:
                    QMessageBox.warning(self, 'Сохранение не удалось',
                                        f"An error occurred while saving the note: {str(e)}")
            else:
                QMessageBox.warning(self, 'Ошибка', 'Заметка не существует')
            self.clear_note_page()  # Clear the note page after deleting the note
        else:
            QMessageBox.warning(self, 'Внимание', 'Заголовок не может быть пустым.')

    def clear_note_page(self):
        self.note_title_edit.clear()
        self.notes_text_edit.clear()

    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.current_font_size = settings.get("font_size", 14)
                self.current_background_image = settings.get("background_image", "background1.png")
                self.apply_font_size_style()
                self.apply_background_image(self.current_background_image)
        except Exception as e:
            self.current_font_size = 14
            self.current_background_image = "background1.png"
            self.apply_font_size_style()
            self.apply_background_image(self.current_background_image)

    def save_settings(self):
        settings = {
            "font_size": self.current_font_size,
            "background_image": self.current_background_image
        }
        try:
            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)
        except IOError as e:
            QMessageBox.warning(self, 'Error', f'Failed to save settings due to an I/O error: {e}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An unexpected error occurred: {e}')

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                self.important_tasks = tasks_data.get("important_tasks", [])
                self.tasks_high_priority = tasks_data.get("tasks_high_priority", [])
                self.additional_tasks = tasks_data.get("additional_tasks", [])
                self.tasks_low_priority = tasks_data.get("tasks_low_priority", [])
        except FileNotFoundError:
            self.important_tasks = []
            self.tasks_high_priority = []
            self.additional_tasks = []
            self.tasks_low_priority = []

    def main_screen(self):
        self.clear_window()
        self.setFixedSize(500, 700)

        self.text1 = QtWidgets.QLabel("HIGH", self)
        self.text1.move(220, 50)
        self.text1.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text1.adjustSize()

        self.add_task_group(self.important_tasks, 100, False)
        self.add_task_group(self.tasks_high_priority, 150, True)

        self.text2 = QtWidgets.QLabel("LOW", self)
        self.text2.move(220, 300)
        self.text2.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text2.adjustSize()

        self.add_task_group(self.additional_tasks, 350, True)
        self.add_task_group(self.tasks_low_priority, 400, False)

        self.text1.show()
        self.text2.show()
        setup_ui_elements(self)

    def main_page(self):
        print("Button 1 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)
        self.main_screen()
        setup_ui_elements(self)

    def show_note_page(self, selected_note=None):
        try:
            self.clear_window()
            self._note_page = NotePage(self)
            self._note_page.note_title_edit.setText(selected_note or "")
            self._note_page.notes_text_edit.setText(self.notes.get(selected_note, ""))
            self._note_page.setup_note_page_ui()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при показе страницы заметок: {e}')

    def settings_page(self):
        print("Button 3 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        font_size_label = QLabel("Размер шрифта", self)
        font_size_label.setGeometry(50, 50, 150, 30)
        font_size_label.show()

        self.font_size_input = QLineEdit(self)
        self.font_size_input.setGeometry(200, 50, 50, 30)
        self.font_size_input.setText(str(self.current_font_size))
        self.font_size_input.setMaxLength(2)
        self.font_size_input.show()

        save_font_size_button = QPushButton("Сохранить", self)
        save_font_size_button.setGeometry(260, 50, 120, 30)
        save_font_size_button.clicked.connect(self.apply_font_size_from_input)
        save_font_size_button.show()

        background_image_label = QLabel("Задний фон", self)
        background_image_label.setGeometry(50, 150, 200, 30)
        background_image_label.show()

        self.background_image_dropdown = QComboBox(self)
        self.background_image_dropdown.setGeometry(250, 150, 200, 30)
        self.background_image_dropdown.addItems(
            ["background1.png", "background2.png", "background3.png", "background4.png", "background5.png"])
        self.background_image_dropdown.currentIndexChanged.connect(self.on_background_image_changed)
        self.background_image_dropdown.show()
        setup_ui_elements(self)

    def on_background_image_changed(self):

        image_file = self.background_image_dropdown.currentText()
        image_path = f"{image_file}"
        if self.apply_background_image(image_path):
            self.current_background_image = image_path
            self.save_settings()

    def apply_font_size_from_input(self):
        font_size_str = self.font_size_input.text()

        try:
            font_size = int(font_size_str)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректный размер шрифта.')
            return

        if 5 <= font_size <= 32:
            self.current_font_size = font_size
            self.apply_font_size_style()  # Apply font size to all relevant elements
            self.save_settings()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Размер шрифта должен быть между 5 и 32.')


    def apply_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.warning(self, 'Error', f"Failed to load background image from {image_path}")
            return False
        else:
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(pixmap))
            self.setPalette(palette)
            return True

    def apply_font_size_style(self):
        font_size_style = f"font-size: {self.current_font_size}px;"

        if hasattr(self, 'notes_text_edit'):
            self.notes_text_edit.setStyleSheet(font_size_style)

    def add_task_group(self, tasks, y_start, is_important):
        for i, task in enumerate(tasks):
            if task in ["Добавить важных дел", "Добавить дел"]:
                btn = QtWidgets.QPushButton(task, self)
                btn.setGeometry(25, y_start + i * 50, 450, 40)
                checkbox = None
                delete_btn = None
            else:
                btn = QtWidgets.QPushButton(task, self)
                btn.setGeometry(25, y_start + i * 50, 450, 40)

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setGeometry(40, y_start + i * 50 + 10, 30, 30)

                checkbox.setStyleSheet(
                    "QCheckBox::indicator { width: 25px; height: 25px; border-radius: 15px; border: 3px solid #989898;}"
                    "QCheckBox::indicator:checked { background-color: #808080;}"
                    "QCheckBox::indicator:unchecked { background-color: white;}"
                )

                delete_btn = QtWidgets.QPushButton("☓", self)
                delete_btn.setGeometry(430, y_start + i * 50 + 10, 25, 25)
                delete_btn.setStyleSheet("background-color: #FF0000; color: white;")
                delete_btn.clicked.connect(lambda _, t=task: self.delete_task(t, is_important))

            if task in ["Добавить важных дел", "Добавить дел"]:
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: #BBBBBB; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")
                if task == "Добавить важных дел":
                    btn.clicked.connect(self.add_important_task_input)
                elif task == "Добавить дел":
                    btn.clicked.connect(self.add_additional_task_input)
            else:
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: black; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")

            btn.show()
            if checkbox:
                checkbox.show()
            if delete_btn:
                delete_btn.show()

    def delete_task(self, task, is_important):
        try:
            if is_important:
                if task in self.important_tasks:
                    self.important_tasks.remove(task)
                elif task in self.tasks_high_priority:
                    self.tasks_high_priority.remove(task)
            else:
                self.tasks_low_priority.remove(task)
            self.save_tasks_to_file()

            self.clear_window()
            self.main_screen()
        except ValueError as e:
            print(f"Error deleting task: {e}")

    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить важных дел', 'Добавить задачу:')
        if ok and text:
            if len(self.tasks_high_priority) < 3:
                self.tasks_high_priority.append(text)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три задачи!')

            self.save_tasks_to_file()
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить дел', 'Добавить задачу:')
        if ok and text:
            if len(self.tasks_low_priority) < 3:
                self.tasks_low_priority.append(text)
            else:
                QMessageBox.information(self, 'Сообщение', 'Вы уже добавили три задачи!')

            self.save_tasks_to_file()
            self.main_screen()

    def clear_window(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.deleteLater()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Q:
            self.clear_window()
            self.main_page()
        elif event.key() == Qt.Key_W:
            self.clear_window()
            NotePage(self)
        elif event.key() == Qt.Key_E:
            self.clear_window()
            self.settings_page()

def run_app():
    try:
        app = QApplication([])
        window = MainWin()
        window.show()
        app.exec_()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    run_app()
