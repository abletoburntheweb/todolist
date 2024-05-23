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
        self.buttons = []

        self.setup_main_buttons()
        self.load_tasks()

        self.current_background_image = "background1.png"
        self.apply_background_image(self.current_background_image)

        self.current_font_size = 14

        self.apply_font_size_style()
        self.completed_tasks_count = 0
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


    def save_tasks_to_file(self):
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(self.tasks_data, file, ensure_ascii=False, indent=4)

    def save_notes_to_file(self):
        title = self.note_title_edit.text()
        notes = self.notes_text_edit.toPlainText()
        if title:
            if title in self.notes:
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
            self.clear_note_page()
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
                self.completed_tasks_count = settings.get("completed_tasks_count", 0)
        except Exception as e:
            self.current_font_size = 14
            self.current_background_image = "background1.png"
            self.apply_font_size_style()
            self.apply_background_image(self.current_background_image)
            self.completed_tasks_count = 0

    def save_settings(self):
        settings = {
            "font_size": self.current_font_size,
            "background_image": self.current_background_image,
            "completed_tasks_count": self.completed_tasks_count
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
                self.tasks_data = json.load(file)
        except FileNotFoundError:
            self.tasks_data = {str(i): {
                "important_tasks": [],
                "additional_tasks": [],
                "tasks_high_priority": [],
                "tasks_low_priority": []
            } for i in range(1, 8)}

    def setup_main_buttons(self):
        button_width = 60
        button_height = 40
        button_spacing = 10
        start_x = 25
        start_y = 10

        self.buttons = []
        for i in range(1, 8):
            btn = QPushButton(f"{i}", self)

            btn.setGeometry(start_x + (i - 1) * (button_width + button_spacing), start_y, button_width, button_height)
            btn.clicked.connect(lambda checked, index=i: self.handle_button_click(index))
            btn.show()
            self.buttons.append(btn)

    def toggle_task_completed(self, task, button_index, checked):
        task['completed'] = checked

        if task in self.tasks_data[str(button_index)]["important_tasks"]:
            category = "important_tasks"
        elif task in self.tasks_data[str(button_index)]["tasks_high_priority"]:
            category = "tasks_high_priority"
        elif task in self.tasks_data[str(button_index)]["additional_tasks"]:
            category = "additional_tasks"
        elif task in self.tasks_data[str(button_index)]["tasks_low_priority"]:
            category = "tasks_low_priority"
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось найти задачу в списках.')
            return

        for i, t in enumerate(self.tasks_data[str(button_index)][category]):
            if t['name'] == task['name']:
                self.tasks_data[str(button_index)][category][i]['completed'] = checked
                break
        if checked:
            self.completed_tasks_count += 1
        else:
            self.completed_tasks_count -= 1
        self.save_settings()

        self.save_tasks_to_file()
    def handle_button_click(self, button_index):
        self.clear_window(keep_main_buttons=True)
        self.setFixedSize(500, 700)


        button_tasks = self.tasks_data.get(str(button_index), {
            "important_tasks": [],
            "additional_tasks": [],
            "tasks_high_priority": [],
            "tasks_low_priority": []
        })


        self.text_high = QtWidgets.QLabel("HIGH", self)
        self.text_high.move(220, 50)
        self.text_high.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text_high.show()

        self.text_low = QtWidgets.QLabel("LOW", self)
        self.text_low.move(220, 300)
        self.text_low.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text_low.show()

        if button_index in range(1, 8):
            self.add_task_group(button_tasks["important_tasks"], 100, True, button_index)
            self.add_task_group(button_tasks["tasks_high_priority"], 150, True, button_index)
            self.add_task_group(button_tasks["additional_tasks"], 350, False, button_index)
            self.add_task_group(button_tasks["tasks_low_priority"], 400, False, button_index)
        else:
            self.main_screen()

        setup_ui_elements(self)

    def main_screen(self, button_index='1'):
        self.clear_window(keep_main_buttons=True)
        self.setFixedSize(500, 700)
        self.setup_main_buttons()

        button_tasks = self.tasks_data.get(button_index, {
            "important_tasks": [],
            "additional_tasks": [],
            "tasks_high_priority": [],
            "tasks_low_priority": []
        })

        self.text1 = QtWidgets.QLabel("HIGH", self)
        self.text1.move(220, 50)
        self.text1.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text1.adjustSize()

        self.add_task_group(button_tasks["important_tasks"], 100, True, button_index)
        self.add_task_group(button_tasks["tasks_high_priority"], 150, True, button_index)

        self.text2 = QtWidgets.QLabel("LOW", self)
        self.text2.move(220, 300)
        self.text2.setStyleSheet("font-size: 15pt; color: #000000;")
        self.text2.adjustSize()

        self.add_task_group(button_tasks["additional_tasks"], 350, False, button_index)
        self.add_task_group(button_tasks["tasks_low_priority"], 400, False, button_index)

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

        completed_tasks_label = QLabel(f"Выполнено задач: {self.completed_tasks_count}", self)
        completed_tasks_label.setGeometry(50, 200, 300, 30)
        completed_tasks_label.show()

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
            self.apply_font_size_style()
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

    def add_task_group(self, tasks, y_start, is_important, button_index):
        for i, task in enumerate(tasks):
            task_name = task['name']
            btn = QtWidgets.QPushButton(task_name, self)
            btn.setGeometry(25, y_start + i * 50, 450, 40)

            if task_name in ["Добавить важных дел", "Добавить дел"]:
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: #BBBBBB; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")
                if task_name == "Добавить важных дел":
                    btn.clicked.connect(lambda _, b_index=button_index: self.add_important_task_input(b_index))
                else:
                    btn.clicked.connect(lambda _, b_index=button_index: self.add_additional_task_input(b_index))
            else:
                task_completed = task.get('completed', False)
                btn.setStyleSheet(
                    "QPushButton { border-radius: 15px; background-color: white; color: black; border: 1px solid; "
                    "border-color: #989898; font-size: 20px}")

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setChecked(task_completed)
                checkbox.setGeometry(40, y_start + i * 50 + 10, 30, 30)
                checkbox.setStyleSheet(
                    "QCheckBox::indicator { width: 25px; height: 25px; border-radius: 15px; border: 3px solid #989898;}"
                    "QCheckBox::indicator:checked { background-color: #808080;}"
                    "QCheckBox::indicator:unchecked { background-color: white;}"
                )
                checkbox.toggled.connect(
                    lambda checked, t=task, b_index=button_index: self.toggle_task_completed(t, b_index, checked))
                checkbox.show()

                delete_btn = QtWidgets.QPushButton("☓", self)
                delete_btn.setGeometry(430, y_start + i * 50 + 10, 25, 25)
                delete_btn.setStyleSheet("background-color: #FF0000; color: white;")
                delete_btn.clicked.connect(
                    lambda _, t=task, b_index=button_index: self.delete_task(t, b_index))
                delete_btn.show()

            btn.show()

    def delete_task(self, task, button_index):
        try:
            category = None
            for cat in ["important_tasks", "tasks_high_priority", "additional_tasks", "tasks_low_priority"]:
                for t in self.tasks_data[str(button_index)][cat]:
                    if t['name'] == task['name']:
                        category = cat
                        break
                if category:
                    break

            if category:
                self.tasks_data[str(button_index)][category] = [
                    t for t in self.tasks_data[str(button_index)][category] if t['name'] != task['name']
                ]
                self.save_tasks_to_file()
                self.handle_button_click(button_index)
            else:
                QMessageBox.warning(self, 'Ошибка', 'Задача не найдена для удаления.')

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка при удалении задачи: {e}')

    def add_important_task_input(self, button_index):
        text, ok = QInputDialog.getText(self, 'Добавить важных дел', 'Введите название задачи:')
        if ok and text:
            new_task = {"name": text, "completed": False}
            self.tasks_data[str(button_index)]["tasks_high_priority"].append(new_task)
            self.save_tasks_to_file()
            self.handle_button_click(button_index)

    def add_additional_task_input(self, button_index):
        text, ok = QInputDialog.getText(self, 'Добавить дел', 'Введите название задачи:')
        if ok and text:
            new_task = {"name": text, "completed": False}
            self.tasks_data[str(button_index)]["additional_tasks"].append(new_task)
            self.save_tasks_to_file()
            self.handle_button_click(button_index)

    def clear_window(self, keep_main_buttons=False):
        widgets_to_keep = self.buttons if keep_main_buttons else []
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget not in widgets_to_keep:
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
