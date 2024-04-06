from random import randint
from PyQt5 import QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QCheckBox, QLabel, \
    QLineEdit
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


# class Rect(QGraphicsView):
#     def __init__(self):
#         super().__init__()
#
#         self.scene = QGraphicsScene()
#         self.setScene(self.scene)
#         self.rect = self.scene.addRect(0, 600, 500, 50)
#         self.rect.setBrush(QColor("#F2FAFD"))
#
#         self.setFixedSize(500, 50)
#
#         self.setHorizontalScrollBarPolicy(1)  # Горизонтальный скроллбар
#         self.setVerticalScrollBarPolicy(1)  # Вертикальный скроллбар


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TODO List')
        self.setGeometry(750, 250, 500, 700)

        self.main_screen()

    def main_screen(self):
        self.clear_window()
        self.setFixedSize(500, 700)

        rect_view = QLabel(self)
        rect_view.setGeometry(0, 630, 500, 70)
        rect_view.setStyleSheet('background-color: #F2FAFD;')
        rect_view.show()

        # self.btnTs4 = QtWidgets.QPushButton('⚙', self)
        # self.btnTs4.setGeometry(470, 10, 20, 21)
        # self.btnTs4.show()

        self.text1 = QtWidgets.QLabel("HIGH", self)
        self.text1.move(220, 25)
        self.text1.setStyleSheet("font-size: 15pt; color: f7dfea;")
        self.text1.adjustSize()

        self.btnTs1 = QtWidgets.QPushButton('Добавить важных дел', self)
        self.btnTs1.setGeometry(25, 100, 450, 40)
        self.btnTs1.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #BBBBBB;border :1px solid; "
            "border-color: #989898; font-size: 20px}")
        self.btnTs1.show()

        checkbox1 = QCheckBox(self)
        checkbox1.setGeometry(5, 105, 20, 20)

        delete_btn1 = QPushButton('❌', self)
        delete_btn1.setGeometry(470, 105, 20, 20)

        self.btnTs1 = QtWidgets.QPushButton('Помыть посуду', self)
        self.btnTs1.setGeometry(25, 150, 450, 40)
        self.btnTs1.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #202020;border :1px solid; "
            "border-color: #989898; font-size: 20px}")
        self.btnTs1.show()

        checkbox2 = QCheckBox(self)
        checkbox2.setGeometry(5, 155, 20, 20)

        delete_btn2 = QPushButton('❌', self)
        delete_btn2.setGeometry(470, 155, 20, 20)

        self.btnTs2 = QtWidgets.QPushButton('Сверстать этот TODO list', self)
        self.btnTs2.setGeometry(25, 200, 450, 40)
        self.btnTs2.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #202020;border :1px solid; "
            "border-color: #989898; font-size: 20px}")
        self.btnTs2.show()

        checkbox3 = QCheckBox(self)
        checkbox3.setGeometry(5, 205, 20, 20)

        delete_btn3 = QPushButton('❌', self)
        delete_btn3.setGeometry(470, 205, 20, 20)

        self.btnTs3 = QtWidgets.QPushButton('Начать делать задачу', self)
        self.btnTs3.setGeometry(25, 250, 450, 40)
        self.btnTs3.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #202020; border :1px solid; "
            "border-color: #989898; font-size: 20px}")

        self.text1 = QtWidgets.QLabel("LOW", self)
        self.text1.move(220, 350)
        self.text1.setStyleSheet("font-size: 15pt; color: f7dfea;")
        self.text1.adjustSize()
        self.text1.show()

        self.btnTs4 = QtWidgets.QPushButton('Добавить дел', self)
        self.btnTs4.setGeometry(25, 400, 450, 40)
        self.btnTs4.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #BBBBBB; border :1px solid; "
            "border-color: #989898; font-size: 20px}")

        self.btnTs5 = QtWidgets.QPushButton('Записаться к стоматологу', self)
        self.btnTs5.setGeometry(25, 450, 450, 40)
        self.btnTs5.setStyleSheet(
            "QPushButton { border-radius: 15px; background-color: white; color: #202020; border :1px solid; "
            "border-color: #989898; font-size: 20px}")

    def second_screen(self):
        print('Settings menu opened')
        self.clear_window()

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
