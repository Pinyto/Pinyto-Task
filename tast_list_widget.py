#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from task_list_item import TaskListItem
from task import Task


class TaskList(QWidget):
    task_deleted = pyqtSignal(Task)

    def __init__(self, task_list):
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.tasks = task_list
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(128)
        self.setSizePolicy(size_policy)
        self.list_layout = QVBoxLayout()
        self.setLayout(self.list_layout)

    def update(self, *__args):
        while self.list_layout.count() > 0:
            item = self.list_layout.takeAt(self.list_layout.count()-1)
            if type(item) == QWidgetItem:
                item.widget().deleteLater()
            else:
                item.deleteLater()
        print(self.tasks)
        for task in self.tasks:
            item = TaskListItem(task)
            item.deleted.connect(self.task_del)
            self.list_layout.addWidget(item, alignment=Qt.AlignCenter)
        super().update(*__args)

    def task_del(self, task):
        self.task_deleted.emit(task)
