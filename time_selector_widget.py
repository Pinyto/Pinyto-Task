#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont
from datetime import time
from math import sin, cos, pi


class TimeSelector(QWidget):
    time_changed = pyqtSignal(time)

    def __init__(self, initial_time=None):
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setMinimumSize(270, 270)
        self.time = initial_time
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        self.hour_edit = QSpinBox()
        self.hour_edit.setMaximum(23)
        self.hour_edit.setMinimum(0)
        self.hour_edit.valueChanged.connect(self.hour_changed)
        h_layout.addWidget(self.hour_edit, alignment=Qt.AlignCenter)
        self.minute_edit = QSpinBox()
        self.minute_edit.setMaximum(59)
        self.minute_edit.setMinimum(0)
        self.minute_edit.valueChanged.connect(self.minute_changed)
        h_layout.addWidget(self.minute_edit, alignment=Qt.AlignCenter)
        h_layout.addStretch(1)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(1)
        self.setLayout(v_layout)

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
        font = QFont('Sans-Serif', 12, QFont.Normal)
        qp.setFont(font)
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 255, 255))
        qp.drawEllipse(int(round(w / 2 - min(w, h) / 2)), int(round(h / 2 - min(w, h) / 2)), min(w, h), min(w, h))
        font_metrics = qp.fontMetrics()
        for i in range(12):
            label_width = font_metrics.width(str(i))
            label_height = font_metrics.height()
            r = min(w, h) / 2 - 0.6 * label_height
            alpha = i * pi / 6
            if self.time and self.time.hour == i:
                qp.setPen(QColor(0, 0, 0))
                qp.setBrush(QColor(0, 0, 0))
                qp.drawEllipse(int(round(w / 2 + r * sin(alpha) - 0.8 * label_height + 0.4)),
                               int(round(h / 2 - r * cos(alpha) - 0.8 * label_height + 0.8)),
                               int(round(1.6*label_height)), int(round(1.6*label_height)))
                qp.setPen(QColor(255, 255, 255))
            else:
                qp.setPen(QColor(0, 0, 0))
            qp.drawText(int(round(w / 2 + r * sin(alpha) - label_width / 2)),
                        int(round(h / 2 - r * cos(alpha) + label_height / 2 - 3)),
                        str(i))
        qp.setPen(QColor(128, 128, 128))
        qp.setBrush(QColor(128, 128, 128))
        qp.drawEllipse(int(round(w / 2 - (min(w, h) - 2.38 * font_metrics.height()) / 2)),
                       int(round(h / 2 - (min(w, h) - 2.38 * font_metrics.height()) / 2)),
                       min(w, h) - 2.38 * font_metrics.height(),
                       min(w, h) - 2.38 * font_metrics.height())
        qp.setPen(QColor(0, 0, 0))
        for i in range(12, 24):
            label_width = font_metrics.width(str(i))
            label_height = font_metrics.height()
            r = min(w, h) / 2 - 1.8 * label_height
            alpha = i * pi / 6
            if self.time and self.time.hour == i:
                qp.setPen(QColor(0, 0, 0))
                qp.setBrush(QColor(0, 0, 0))
                qp.drawEllipse(int(round(w / 2 + r * sin(alpha) - 0.8 * label_height + 0.4)),
                               int(round(h / 2 - r * cos(alpha) - 0.8 * label_height + 0.8)),
                               int(round(1.6*label_height)), int(round(1.6*label_height)))
                qp.setPen(QColor(255, 255, 255))
            else:
                qp.setPen(QColor(0, 0, 0))
            qp.drawText(int(round(w / 2 + r * sin(alpha) - label_width / 2)),
                        int(round(h / 2 - r * cos(alpha) + label_height / 2 - 3)),
                        str(i))
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawEllipse(int(round(w / 2 - (min(w, h) - 4.9 * font_metrics.height()) / 2)),
                       int(round(h / 2 - (min(w, h) - 4.9 * font_metrics.height()) / 2)),
                       min(w, h) - 4.9 * font_metrics.height(),
                       min(w, h) - 4.9 * font_metrics.height())
        r = min(w, h) / 2 - 3.3 * font_metrics.height()
        if self.time:
            qp.setPen(QColor(128, 128, 128))
            qp.setBrush(QColor(128, 128, 128))
            alpha = self.time.minute * pi / 30
            qp.drawEllipse(int(round(w / 2 + r * sin(alpha) - 0.8 * font_metrics.height() + 0.4)),
                           int(round(h / 2 - r * cos(alpha) - 0.8 * font_metrics.height() + 0.8)),
                           int(round(1.6 * font_metrics.height())),
                           int(round(1.6 * font_metrics.height())))
        qp.setPen(QColor(255, 255, 255))
        for i in range(0, 60, 5):
            label_width = font_metrics.width(str(i))
            label_height = font_metrics.height()
            alpha = i * pi / 30
            qp.drawText(int(round(w / 2 + r * sin(alpha) - label_width / 2)),
                        int(round(h / 2 - r * cos(alpha) + label_height / 2 - 3)),
                        str(i))
        qp.setPen(QColor(255, 255, 255))
        qp.drawText(int(round(w/2-3)), int(round(h/2+4)), ":")

    def hour_changed(self, new_value):
        self.time = time(hour=new_value, minute=self.time.minute if type(self.time) == time else 0)
        self.update()
        self.time_changed.emit(self.time)

    def minute_changed(self, new_value):
        self.time = time(hour=self.time.hour if type(self.time) == time else 0, minute=new_value)
        self.update()
        self.time_changed.emit(self.time)
