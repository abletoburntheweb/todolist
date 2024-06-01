def search_input_style():
    return """
        QLineEdit {
            border: 2px solid #bdbdbd;
            border-radius: 10px;
            padding: 5px 10px;
            font-size: 16px;
            color: #212121;
        }
        QLineEdit:focus {
            border: 2px solid #42a5f5;
        }
        QLineEdit:hover {
            border: 2px solid #64b5f6;
        }
    """

def day_button_style(active=False):
    if active:
        return """
            QPushButton {
                background-color: #6495ED; /* Dark blue color for the active button */
                color: white;
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #16839C;
            }
            QPushButton:pressed {
                background-color: #ADD8E6;
            }
        """
    else:
        return """
            QPushButton {
                background-color: #87CEFA; /* Light blue color */
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
                border: 2px solid #1E90FF; /* Dark blue border */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
            QPushButton:pressed {
                background-color: #ADD8E6;
            }
        """

def main_window_style():
    return """
        QMainWindow {
            background-color: #ECEFF1;
        }
        QPushButton {
            font-size: 16px;
            border-radius: 8px;
            padding: 6px;
            background-color: #2196F3;
            color: white;
        }
        QPushButton:hover {
            background-color: #64B5F6;
        }
        QPushButton:pressed {
            background-color: #1E88E5;
        }
        QLabel {
            font-size: 18px;
            color: #37474F;
        }
    """

def settings_style():
    return {
        "label_style": """
            QLabel {
                font-size: 16px;
                color: #333;
                padding: 5px;
            }
        """,
        "button_style": """
            QPushButton {
                background-color: #5CACEE;
                color: white;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid #5CACEE;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1E90FF;
            }
            QPushButton:pressed {
                background-color: #4682B4;
            }
        """,
        "completed_tasks_label_style": """
            QLabel {
                font-size: 18px;
                color: #2e8b57;
                padding: 5px;
                border: 2px solid #2e8b57;
                border-radius: 8px;
                margin-top: 20px;
                background-color: #d9ecd0;
            }
        """,
        "reset_button_style": """
            QPushButton {
                background-color: #FF6347;
                color: white;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
            QPushButton:pressed {
                background-color: #CD5C5C;
            }
        """
    }
def get_task_group_styles():
        return {
            "edit_button_style": """
            QPushButton {
                background-color: #FFEB3B;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #FDD835;
            }
        """,
        "delete_button_style": """
            QPushButton {
                background-color: #F44336;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
        """,
        "checkbox_style": """
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #22a4f5;
            }
        """,

    }
