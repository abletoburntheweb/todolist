import json
from PyQt5.QtWidgets import QMessageBox


def save_notes_to_file(notes, note_title_edit, notes_text_edit):
    title = note_title_edit.text()
    notes_content = notes_text_edit.toPlainText()
    if title:
        notes[title] = notes_content
        try:
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump({"notes": notes}, file, ensure_ascii=False, indent=4)
            QMessageBox.information(None, 'Save', 'Note saved.')
        except Exception as e:
            QMessageBox.warning(None, 'Save Failed', f"An error occurred while saving the note: {str(e)}")
    else:
        QMessageBox.warning(None, 'Warning', 'The note title cannot be empty.')


def delete_current_note(notes, note_title_edit, sidebar_list_widget):
    title = note_title_edit.text()
    if title in notes:
        del notes[title]
        load_note_titles(notes, sidebar_list_widget)
        note_title_edit.clear()
        QMessageBox.information(None, 'Deleted', 'Note deleted successfully.')
    else:
        QMessageBox.warning(None, 'Warning', 'Please select a note to delete.')


def load_note_titles(notes, sidebar_list_widget):
    sidebar_list_widget.clear()
    for note_title in notes.keys():
        sidebar_list_widget.addItem(note_title)


def create_new_note(note_title_edit, notes_text_edit, sidebar_list_widget):
    note_title_edit.clear()
    notes_text_edit.clear()
    note_title_edit.setFocus()
