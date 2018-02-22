#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from parsing_input import ParsingInput
from tast_list_widget import TaskList
from task import Task


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 150, 800, 600)
        self.setWindowTitle('Pinyto Task')
        self.setWindowIcon(QIcon('Icon/Icon.png'))

        example_task_1 = Task(text="Spülmaschine ausräumen", weight=1.0)
        example_task_2 = Task(text="Steuererklärung", weight=2.0)
        self.task_list = [example_task_1, example_task_2]

        self.new_task_input = ParsingInput()
        self.new_task_input.edit_complete.connect(self.add_task)
        hbox = QHBoxLayout()
        hbox.addWidget(self.new_task_input)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.task_list_widget = TaskList(self.task_list)
        self.task_list_widget.task_deleted.connect(self.del_task)
        vbox.addWidget(self.task_list_widget, alignment=Qt.AlignTop)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.new_task_input.focusWidget()
        self.show()

    def add_task(self, task):
        self.task_list.append(task)
        self.task_list_widget.update()

    def del_task(self, task):
        for i, t in enumerate(self.task_list):
            if t == task:
                self.task_list.pop(i)
                self.task_list_widget.update()
                break
