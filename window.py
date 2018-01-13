#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from parsing_input import ParsingInput


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 150, 800, 600)
        self.setWindowTitle('Pinyto Task')
        self.setWindowIcon(QIcon('Icon/Icon.png'))

        self.new_task_input = ParsingInput()
        hbox = QHBoxLayout()
        hbox.addWidget(self.new_task_input)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.new_task_input.focusWidget()
        self.show()
