#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QLineEdit
from PyQt5.QtWidgets import QCalendarWidget, QGroupBox
#from PyQt5.QtWidgets import QStyle, QCommonStyle
from PyQt5.QtGui import QPainter, QColor, QIcon, QDrag, QPixmap
from time_selector_widget import TimeSelector
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
        task_layout = QVBoxLayout()
        task_layout.setContentsMargins(25, 6, 6, 6)
        first_line = QHBoxLayout()
        self.name_widget = QLabel()
        self.name_widget.setText(self.task.text)
        first_line.addWidget(self.name_widget, stretch=255, alignment=Qt.AlignLeading)
        self.edit_name = QLineEdit()
        self.edit_name.setText(self.task.text)
        self.edit_name.textChanged.connect(self.setTaskText)
        self.edit_name.returnPressed.connect(self.leaveEditMode)
        first_line.addWidget(self.edit_name)
        self.edit_button = QPushButton()
        self.edit_button.setFlat(True)
        self.edit_button.setIcon(QIcon("Icon/Edit.png"))
        self.edit_button.clicked.connect(self.enterEditMode)
        first_line.addWidget(self.edit_button, alignment=Qt.AlignRight)
        self.leave_edit_mode_button = QPushButton()
        self.leave_edit_mode_button.setFlat(True)
        self.leave_edit_mode_button.setIcon(QIcon("Icon/Collapse.png"))
        self.leave_edit_mode_button.clicked.connect(self.leaveEditMode)
        first_line.addWidget(self.leave_edit_mode_button, alignment=Qt.AlignRight)
        del_button = QPushButton()
        del_button.setFlat(True)
        #del_button.setIcon(QCommonStyle().standardIcon(QStyle.SP_TrashIcon))
        del_button.setIcon(QIcon("Icon/Trash.png"))
        del_button.clicked.connect(self.delete_task)
        first_line.addWidget(del_button, alignment=Qt.AlignRight)
        task_layout.addLayout(first_line)
        second_line = QHBoxLayout()
        self.due_date_box = QGroupBox("Due Date")
        due_date_box_layout = QVBoxLayout()
        self.due_date_calendar = QCalendarWidget()
        if self.task.due_date:
            self.due_date_calendar.setSelectedDate(self.task.due_date)
        self.due_date_calendar.selectionChanged.connect(self.setDueDate)
        due_date_box_layout.addWidget(self.due_date_calendar)
        self.due_date_time = TimeSelector(self.task.get_due_date_time())
        self.due_date_time.time_changed.connect(self.setDueDateTime)
        due_date_box_layout.addWidget(self.due_date_time)
        self.due_date_box.setLayout(due_date_box_layout)
        second_line.addWidget(self.due_date_box, alignment=Qt.AlignLeft)
        task_layout.addLayout(second_line)
        self.setLayout(task_layout)
        self.setEditMode(False)

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

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        mime_data = QMimeData()
        mime_data.setData('application/pinytoTask', self.task.to_json().encode('utf-8'))
        mime_data.setText(self.task.text)
        drag_object = QDrag(self)
        drag_object.setMimeData(mime_data)
        drag_object.setHotSpot(event.pos() - self.rect().topLeft())
        drag_object.setPixmap(self.grab())
        dropAction = drag_object.exec_(Qt.MoveAction)

    def delete_task(self):
        self.deleted.emit(self.task)

    def enterEditMode(self):
        self.setEditMode(True)

    def leaveEditMode(self):
        self.setEditMode(False)

    def setEditMode(self, edit=False):
        self.name_widget.setVisible(not edit)
        self.edit_name.setVisible(edit)
        self.edit_button.setVisible(not edit)
        self.leave_edit_mode_button.setVisible(edit)
        self.due_date_box.setVisible(edit)
        if edit:
            self.edit_name.setFocus()

    def setTaskText(self, new_text):
        self.task.text = new_text
        self.name_widget.setText(new_text)

    def setDueDate(self):
        self.task.set_due_date(self.due_date_calendar.selectedDate().toPyDate())
        self.update()

    def setDueDateTime(self, new_time):
        self.task.set_due_date_time(new_time)
        self.update()
