import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, QCheckBox, QMessageBox, \
    QLineEdit, QListWidget, QTextEdit, QListWidgetItem, QComboBox

from ui_elements import setup_ui_elements


class MainWin(QMainWindow):
    def __init__(self):  # Corrected the method name
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)

        self.load_tasks()

        # Set the default background image
        self.current_background_image = "background1.png"
        self.apply_background_image(self.current_background_image)

        # Load settings and apply styles
        self.load_settings()
        self.save_settings()
        self.apply_font_size_style()

        # Finally, set up the main screen UI
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
        title = self.note_title_edit.text()  # Get the title from the QLineEdit
        notes = self.notes_text_edit.toPlainText()  # Get the content from the QTextEdit
        if title:  # Проверяем, что заголовок заметки не пустой
            self.notes[title] = notes  # Обновляем или добавляем заметку в словарь
            try:
                with open("notes.json", "w", encoding="utf-8") as file:
                    json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)  # Сохраняем словарь в файл
                QMessageBox.information(self, 'Success', 'Заметка сохранена')  # Информационное сообщение о сохранении
            except Exception as e:
                QMessageBox.warning(self, 'Save Failed',
                                    f"An error occurred while saving the note: {str(e)}")  # Сообщение об ошибке
        else:
            QMessageBox.warning(self, 'Warning', 'Заголовок не может быть пустым.')  # Сообщение, если заголовок пустой


    def load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.current_font_size = settings.get("font_size", 14)
                self.current_background_image = settings.get("background_image", "background1.png")
                self.apply_font_size_style()
                self.apply_background_image(self.current_background_image)
        except Exception as e:
            # If settings.json does not exist or there is an error, use default settings
            self.current_font_size = 14
            self.current_background_image = "background1.png"
            self.apply_font_size_style()
            self.apply_background_image(self.current_background_image)

    def save_settings(self):
        settings = {
            "font_size": self.current_font_size,
            "background_image": self.current_background_image
        }
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def load_tasks(self):
        # Attempt to load tasks from a file or initialize with empty lists
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                self.important_tasks = tasks_data.get("important_tasks", [])
                self.tasks_high_priority = tasks_data.get("tasks_high_priority", [])
                self.additional_tasks = tasks_data.get("additional_tasks", [])
                self.tasks_low_priority = tasks_data.get("tasks_low_priority", [])
        except FileNotFoundError:
            # If tasks.json does not exist, initialize with default empty lists
            self.important_tasks = []
            self.tasks_high_priority = []
            self.additional_tasks = []
            self.tasks_low_priority = []



    def apply_font_size_from_input(self):
        try:
            font_size_str = self.font_size_input.text()
            font_size = int(font_size_str)
            self.current_font_size = font_size
            self.apply_font_size_style()
            self.save_settings()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid font size.')

    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить важную задачу', 'Введите задачу:')
        if ok and text:
            self.tasks_high_priority.append(text)
            self.save_tasks_to_file()
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Добавить задачу', 'Введите задачу:')
        if ok and text:
            self.tasks_low_priority.append(text)
            self.save_tasks_to_file()
            self.main_screen()

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

    def note_page(self, selected_note=None):
        print("Button 2 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        # Sidebar for note titles as a QListWidget
        self.sidebar_list_widget = QListWidget(self)
        self.sidebar_list_widget.setGeometry(10, 10, 150, 650)
        self.sidebar_list_widget.setStyleSheet("background-color: #F2FAFD;")
        self.load_note_titles()

        # Adjust the geometry for the note title LineEdit
        # Subtracting sidebar width (150) and some margin from the total window width (500)
        self.note_title_edit = QLineEdit(self)
        self.note_title_edit.setGeometry(170, 10, 320, 30)  # Adjusted width to 320
        self.note_title_edit.setPlaceholderText("Название заметки")

        # Adjust the geometry for the note content QTextEdit
        # Subtracting sidebar width (150) and some margin from the total window width (500)
        self.notes_text_edit = QTextEdit(self)
        self.notes_text_edit.setGeometry(170, 50, 320, 610)  # Adjusted width to 320
        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")


        # Apply font size style to the notes text edit
        self.apply_font_size_style()  # Эта строка применяет текущий размер шрифта

        save_notes_button = QPushButton("Сохранить заметку", self)
        save_notes_button.setGeometry(340, 600, 150, 30)
        save_notes_button.clicked.connect(self.save_notes_to_file)

        delete_note_button = QPushButton("Удалить заметку", self)
        delete_note_button.setGeometry(190, 600, 150, 30)
        delete_note_button.clicked.connect(self.delete_current_note)
        delete_note_button.show()

        self.add_new_note_button()

        # Load the selected note content
        if selected_note:
            self.note_title_edit.setText(selected_note)
            self.notes_text_edit.setText(self.notes.get(selected_note, ""))

        self.sidebar_list_widget.show()
        self.note_title_edit.show()
        self.notes_text_edit.show()
        save_notes_button.show()

        setup_ui_elements(self)
    def create_new_note(self):
        self.note_title_edit.clear()  # Clear the note title field
        self.notes_text_edit.clear()  # Clear the note content field
        # Apply the current font size to the new note
        self.apply_font_size_style()

    def add_new_note_button(self):
        new_note_button = QPushButton("Создать новую заметку", self)
        new_note_button.setGeometry(10, 600, 150, 30)
        new_note_button.clicked.connect(self.create_new_note)
        new_note_button.show()

    def delete_current_note(self):
        title = self.note_title_edit.text()
        if title in self.notes:
            reply = QMessageBox.question(self, 'Подтверждение удаления',
                                         'Вы действительно хотите удалить эту заметку?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.notes[title]
                self.load_note_titles()
                self.create_new_note()  # Очистить поля заметки
                try:
                    with open("notes.json", "w", encoding="utf-8") as file:
                        json.dump({"notes": self.notes}, file, ensure_ascii=False, indent=4)
                    QMessageBox.information(self, 'Успех', 'Заметка удалена.')
                except Exception as e:
                    QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при сохранении изменений: {e}')
        else:
            QMessageBox.warning(self, 'Внимание!', 'Заметка не найдена или уже удалена.')
    def load_note_titles(self):
        self.sidebar_list_widget.clear()
        for note in self.notes.keys():
            item = QListWidgetItem(note)
            self.sidebar_list_widget.addItem(item)
        self.sidebar_list_widget.itemClicked.connect(self.on_note_selected)

    def on_note_selected(self, item):
        selected_note = item.text()
        self.note_page(selected_note)

    def save_current_note(self):
        title = self.note_title_edit.text()
        content = self.notes_text_edit.toPlainText()
        if title:
            self.notes[title] = content
            self.save_notes_to_file()
            self.load_note_titles()
            QMessageBox.information(self,'Заметка успешно сохранена.')
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, введите заголовок заметки.')

    def settings_page(self):
        print("Button 3 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        # Create a label for the font size input
        font_size_label = QLabel("Choose font size:", self)
        font_size_label.setGeometry(50, 50, 150, 30)
        font_size_label.show()

        # Create the QLineEdit for font size input
        self.font_size_input = QLineEdit(self)
        self.font_size_input.setGeometry(200, 50, 50, 30)
        self.font_size_input.setText(str(self.current_font_size))  # Set the current font size as the initial text
        self.font_size_input.setMaxLength(2)  # Limit the input to two characters
        self.font_size_input.returnPressed.connect(self.apply_font_size_from_input)

        self.font_size_input.show()
        background_image_label = QLabel("Choose background image:", self)
        background_image_label.setGeometry(50, 150, 200, 30)
        background_image_label.show()

        # Create a dropdown for background image options
        self.background_image_dropdown = QComboBox(self)
        self.background_image_dropdown.setGeometry(250, 150, 200, 30)
        self.background_image_dropdown.addItems(
            ["background1.png", "background2.png", "background3.png", "background4.png", "background5.png"])
        self.background_image_dropdown.currentIndexChanged.connect(self.on_background_image_changed)
        self.background_image_dropdown.show()
        setup_ui_elements(self)

    def on_background_image_changed(self):
        # Get the current selection from the dropdown
        image_file = self.background_image_dropdown.currentText()
        image_path = f"{image_file}"
        self.apply_background_image(image_path)
    def apply_font_size_from_input(self):
        # This method is called when the user presses Enter on the font size input
        try:
            font_size_str = self.font_size_input.text()
            font_size = int(font_size_str)
            self.current_font_size = font_size
            self.apply_font_size_style()  # Update the font size immediately
            self.save_settings()  # Save the new font size to the settings file
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid font size.')

    def apply_font_size_style(self):
        # This method updates the notes text edit with the current font size
        if hasattr(self, 'notes_text_edit'):
            self.notes_text_edit.setStyleSheet(f"font-size: {self.current_font_size}px;")

    def apply_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load background image from {image_path}")
            return
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)


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

            # Clear the window and then redraw the task groups
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

def run_app():
    app = QApplication([])
    window = MainWin()
    window.show()
    app.exec_()

if __name__ == '__main__':
    run_app()