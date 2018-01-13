#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 150, 800, 600)
        self.setWindowTitle('Pinyto Task')
        self.setWindowIcon(QIcon('Icon/Icon.png'))
        self.show()
