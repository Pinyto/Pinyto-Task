#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from task_list_item import TaskListItem
from task import Task


class TaskList(QWidget):
    task_deleted = pyqtSignal(Task)

    def __init__(self, task_list):
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.tasks = task_list
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)  # This increases the min width
        size_policy.setHorizontalStretch(128)
        self.setSizePolicy(size_policy)
        self.list_layout = QVBoxLayout()
        self.setLayout(self.list_layout)
        self.setAcceptDrops(True)
        self.update()

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
            self.list_layout.addWidget(item, alignment=Qt.AlignTop)
        super().update(*__args)

    def task_del(self, task):
        self.task_deleted.emit(task)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
        qp.setPen(QColor(128, 128, 128))
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRoundedRect(0, 0, w, h, 6, 6)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/pinytoTask'):
            event.accept()

    def dragMoveEvent(self, event):
        y = event.pos().y()
        print(y)
        if event.mimeData().hasFormat('application/pinytoTask'):
            print(event.mimeData().data('application/pinytoTask'))

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        if event.mimeData().hasFormat('application/pinytoTask'):
            pass
        y = event.pos().y()
        print(y)
        event.accept()
