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

def results_list_style():
    return """
     QListWidget {
        border: 2px solid #5d8aa8; 
        border-radius: 10px;
        background-color: #f7f7f7;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        color: #2c3e50; 
        outline: none; 
    }
    QListWidget::item {
        border-radius: 5px;
        padding: 10px;
        margin: 2px;
        background-color: #fdfdfd;
        border-bottom: 1px solid #eaeaea;
    }
    QListWidget::item:alternate {
        background-color: #f6f6f6;
    }
    QListWidget::item:selected {
        background-color: #5d8aa8; 
        color: #ffffff; 
    }
    QListWidget::item:selected:!active {
        background-color: #5d8aa8;
        color: #ffffff;
    }
    QListWidget::item:hover {
        background-color: #ecf0f1; 
        color: #2c3e50; 
    }
    """

def add_tasks_button_style():
    return """
        QPushButton {
            background-color: #84cdfa;
            text-align: left;
            padding-left: 10px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #ADD8E6;
        }
    """

def tasks_button_style():
    return """
        QPushButton {
            text-align: left;
            padding-left: 10px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #ADD8E6;
        }
    """
def subtasks_button_style():
    return """
        QPushButton {
            background-color: #0057fa;  
            text-align: left;
            padding-left: 15px;  
            border-radius: 10px;  
            font-size: 14px;  
            color: white; 
        }
        QPushButton:hover {
            background-color: #0047e5;  
        }
        QPushButton:pressed {
            background-color: #0037d1;  
        }
    """
def day_button_style(active=False):
    if active:
        return """
            QPushButton {
                background-color: #6495ED; 
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
                background-color: #87CEFA; 
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
                border: 2px solid #1E90FF; 
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
        "add_subtask_button_style": """
                QPushButton {
                    background-color: #90EE90;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #32CD32;
                }
            """
    }


def sidebar_list_widget_style():
    return """
        QListWidget {
            background-color: #F2FAFD;
            border: none;
            color: #333;
            font-size: 14px;
        }
        QListWidget::item:selected {
            background-color: #89CFF0;
            color: black;
        }
    """
def notes_button_style():
    return """""
            QPushButton {
                background-color: #6CA6CD;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #5B9BD5;
            }
            QPushButton:hover {
                background-color: #8DBDD8;
            }
        """
def notes_title_edit_style():
    return("""
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #6CA6CD;
            }
        """)
def notes_text_edit_style():
    return ("""
            QTextEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
                color: #555;
            }
            QTextEdit:focus {
                border-color: #6CA6CD;
            }
        """)