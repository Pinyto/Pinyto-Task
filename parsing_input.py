#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer


class ParsingInput(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(28, 28)
        self.text = ""
        self.cursor_position = 0
        self.cursor_visible = True
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)

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
        qp.setPen(QColor(128, 128, 128))
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRoundedRect(0, 0, w, h, 5, 5)
        qp.setPen(QColor(0, 0, 0))
        font_metrics = qp.fontMetrics()
        c_start_position = 5
        cursor_pixel_position = c_start_position
        print("cursor position: {}".format(self.cursor_position))
        for i, c in enumerate(self.text):
            c_width = font_metrics.width(c)
            qp.drawText(c_start_position, 20, c)
            c_start_position += c_width
            if i == self.cursor_position - 1:
                cursor_pixel_position = c_start_position
        if self.hasFocus() and self.cursor_visible:
            qp.drawLine(cursor_pixel_position, 4, cursor_pixel_position, 28 - 4)

    def keyPressEvent(self, event):
        key = event.key()
        mod = int(event.modifiers())
        print(
            "Key 0x{:x}/{}/ {} {} {}".format(
                key,
                event.text(),
                "  [+shift]" if event.modifiers() & Qt.SHIFT else "",
                "  [+ctrl]" if event.modifiers() & Qt.CTRL else "",
                "  [+alt]" if event.modifiers() & Qt.ALT else ""
            )
        )
        if len(event.text()) > 0:
            self.text += event.text()[0]
            self.cursor_position += 1
        self.update()

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()
