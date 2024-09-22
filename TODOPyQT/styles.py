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
               background-color: #54b9f7;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
               background-color: #0b8bdb;
            }
    """


def add_daily_tasks_button_style():
    return """
        QPushButton {
            background-color: #a594ff;  
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #7b61ff; 
        }
    """


def add_weekly_tasks_button_style():
    return """
        QPushButton {
            background-color: #ffa861;  
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #f48647; 
        }
    """


def tasks_button_style():
    return """
            QPushButton {
                background-color: #22a4f5;
                text-align: left;
                padding-left: 10px;
                font-size: 18px;  
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #75c1ff;
            }
            QPushButton:pressed {
                background-color: #2a00fa;
            }
        """


def daily_task_button_style():
    return """
        QPushButton {
                background-color: #7b61ff;
            text-align: left;
            padding-left: 10px;
            font-size: 18px;  
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #a694ff;
        }
        QPushButton:pressed {
            background-color: #2a00fa;
        }
    """

def weekly_tasks_button_style():
    return """
            QPushButton {
                    background-color: #ffa861;
                text-align: left;
                padding-left: 10px;
                font-size: 18px;  
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #f48647;
            }
            QPushButton:pressed {
                background-color: #b35900;
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


def task_name_input_style():
    return """
        QLineEdit {
            border: 2px solid #bdbdbd;
            border-radius: 10px;
            padding: 10px;
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


def date_input_style():
    return """
        QLineEdit {
            border: 2px solid #bdbdbd;
            border-radius: 10px;
            padding: 10px;
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


def tag_selector_style():
    return """
        QComboBox {
            padding: 10px;
            border: 2px solid #bdbdbd;
            border-radius: 10px;
            font-size: 16px;
            color: #212121;
            background-color: #ffffff;
        }
        QComboBox:focus {
            border: 2px solid #42a5f5;
        }
        QComboBox:hover {
            border: 2px solid #64b5f6;
        }
        QComboBox::drop-down {
            border-left: 2px solid #bdbdbd;
        }
        QComboBox::down-arrow {
            image: url(down-arrow.png);  
        }
        QComboBox QAbstractItemView {
            border: 2px solid #42a5f5;
            selection-background-color: #42a5f5;
            selection-color: #ffffff;
        }
    """


def dialog_button_box_style():
    return """
        QPushButton {
            padding: 10px 20px;
            border: 2px solid #bdbdbd;
            border-radius: 10px;
            background-color: #3498db;
            color: white;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1c6ea4;
        }
    """


def tag_button_style():
    return """
        QPushButton {
                background-color: #009e79; 
            color: #ffffff; 
            font-size: 16px;
            border-radius: 15px; 
            padding: 10px 15px; 
            min-width: 60px; 
            min-height: 30px; 
        }
        QPushButton:hover {
            background-color: #128264; 
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
                font-size: 14px;
                color: #2e8b57;
                padding: 5px;
                border: 2px solid #2e8b57;
                border-radius: 8px;
                margin-top: 20px;
                background-color: #d9ecd0;
                text-align: center;
            }
        """,
        "reset_button_style": """
            QPushButton {
                background-color: #FF6347;
                color: white;
                border-radius: 6px;
                padding: 5px;
                font-size: 14px;
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

def calendar_styles():
    return """
        QCalendarWidget QToolButton {
            color: white;
            background-color: #ffa861;
            font-size: 16px;
            border: none;
            margin: 10px;
            padding: 10px;
        }
        QCalendarWidget QToolButton:hover {
            background-color: #f48647;
        }
        QCalendarWidget QToolButton#qt_calendar_prevmonth {
            qproperty-text: "<";
            width: 30px;
        }
        QCalendarWidget QToolButton#qt_calendar_nextmonth {
            qproperty-text: ">";
            width: 30px;
        }
        QCalendarWidget QMenu {
            width: 150px;
            color: white;
            background-color: #ffa861;
        }
        QCalendarWidget QSpinBox {
            width: 100px;
            font-size: 16px;
        }
        QCalendarWidget QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
        }
        QCalendarWidget QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
        }
        QCalendarWidget QSpinBox::up-arrow, QCalendarWidget QSpinBox::down-arrow {
            width: 15px;
            height: 15px;
        }
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #ffa861;
        }
        QCalendarWidget QTableView {
            font-size: 16px;
            color: #333;
        }
        QCalendarWidget QTableView:selected {
            background-color: #ffa861;
            color: white;
        }
        QCalendarWidget QTableView QHeaderView::section {
            background-color: #ffa861;
            color: white;
            font-size: 14px;
        }
    """
def sidebar_list_widget_style():
    return """
        QListWidget {
            background-color: #F2FAFD;
            border: none;
            color: #333;
            font-size: 18px;
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
                font-size: 18px;
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
    return ("""
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
                font-size: 18px;
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
                font-size: 18px;
                color: #555;
            }
            QTextEdit:focus {
                border-color: #6CA6CD;
            }
        """)
