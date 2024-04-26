import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QInputDialog, QCheckBox, QMessageBox, \
    QTextEdit, QListWidget, QLineEdit, QListWidgetItem
from ui_elements import setup_ui_elements

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)

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
                QMessageBox.information(self, 'Save', 'Note saved.')  # Информационное сообщение о сохранении
            except Exception as e:
                QMessageBox.warning(self, 'Save Failed',
                                    f"An error occurred while saving the note: {str(e)}")  # Сообщение об ошибке
        else:
            QMessageBox.warning(self, 'Warning', 'The note title cannot be empty.')  # Сообщение, если заголовок пустой
    def add_important_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Important Task', 'Enter task:')
        if ok and text:
            self.tasks_high_priority.append(text)
            self.save_tasks_to_file()
            self.main_screen()

    def add_additional_task_input(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Additional Task', 'Enter task:')
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

    def note_page(self, selected_note=None):
        print("Button 2 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        # Sidebar for note titles as a QListWidget
        self.sidebar_list_widget = QListWidget(self)
        self.sidebar_list_widget.setGeometry(10, 10, 150, 650)
        self.sidebar_list_widget.setStyleSheet("background-color: #F2FAFD;")
        self.load_note_titles()

        # LineEdit for the note title
        self.note_title_edit = QLineEdit(self)
        self.note_title_edit.setGeometry(170, 10, 570, 30)
        self.note_title_edit.setPlaceholderText("Название заметки")

        # QTextEdit for the note content
        self.notes_text_edit = QTextEdit(self)
        self.notes_text_edit.setGeometry(170, 50, 570, 610)
        self.notes_text_edit.setPlaceholderText("Напишите что-нибудь...")

        save_notes_button = QPushButton("Сохранить заметку", self)
        save_notes_button.setGeometry(350, 600, 150, 30)
        save_notes_button.clicked.connect(self.save_notes_to_file)

        delete_note_button = QPushButton("Удалить заметку", self)
        delete_note_button.setGeometry(200, 600, 150, 30)
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
        self.note_title_edit.clear()  # Очистить поле заголовка заметки
        self.notes_text_edit.clear()

    def add_new_note_button(self):
        new_note_button = QPushButton("Создать новую заметку", self)
        new_note_button.setGeometry(10, 600, 150, 30)
        new_note_button.clicked.connect(self.create_new_note)
        new_note_button.show()

    def delete_current_note(self):
        title = self.note_title_edit.text()
        if title in self.notes:
            del self.notes[title]
            self.load_note_titles()
            self.create_new_note()  # Clear the note fields
            QMessageBox.information(self, 'Deleted', 'Note deleted successfully.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a note to delete.')
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
            QMessageBox.information(self, 'Сохранено', 'Заметка успешно сохранена.')
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, введите заголовок заметки.')


    def settings_page(self):
        print("Button 3 clicked")
        self.clear_window()
        self.setFixedSize(500, 700)

        dark_mode_checkbox = QtWidgets.QCheckBox('Dark Mode', self)
        dark_mode_checkbox.setGeometry(200, 50, 100, 30)
        dark_mode_checkbox.setStyleSheet("color: white; font-size: 14px;")

        def toggle_dark_mode(checked):
            if checked:
                self.setStyleSheet("background-color: #1E1E1E; color: white;")
            else:
                self.setStyleSheet("background-color: white; color: black;")

        dark_mode_checkbox.stateChanged.connect(toggle_dark_mode)

        dark_mode_checkbox.show()
        setup_ui_elements(self)

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
