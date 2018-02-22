#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QStyle, QCommonStyle
from PyQt5.QtGui import QPainter, QColor
from task import Task


class TaskListItem(QWidget):
    deleted = pyqtSignal(Task)

    def __init__(self, task):
        self.task = task
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(255)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(120, 36)
        self.setCursor(Qt.OpenHandCursor)
        task_layout = QHBoxLayout()
        task_layout.setContentsMargins(25, 6, 6, 6)
        name_widget = QLabel()
        name_widget.setText(self.task.text)
        task_layout.addWidget(name_widget, alignment=Qt.AlignLeading)
        task_layout.addStretch(255)
        del_button = QPushButton()
        del_button.setFlat(True)
        del_button.setIcon(QCommonStyle().standardIcon(QStyle.SP_TrashIcon))
        del_button.clicked.connect(self.delete_task)
        task_layout.addWidget(del_button, alignment=Qt.AlignRight)
        self.setLayout(task_layout)

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
        qp.setPen(QColor(64, 64, 64))
        qp.setBrush(QColor(*self.task.get_color()))
        qp.drawRoundedRect(0, 0, w, h, 6, 6)
        progress = self.task.get_progress()
        if progress > 0:
            qp.setBrush(QColor(0, 200, 0))
            qp.drawRoundedRect(0, 0, int(round(w*progress)), h, 6, 6)

    def delete_task(self):
        self.deleted.emit(self.task)
