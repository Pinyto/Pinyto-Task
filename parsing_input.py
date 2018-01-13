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
        self.text = []
        self.cursor_position = 0
        self.cursor_visible = True
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.set_cursor_visible()

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
            c_width = font_metrics.width(c["char"])
            qp.drawText(c_start_position, 20, c["char"])
            c_start_position += c_width
            if i == self.cursor_position - 1:
                cursor_pixel_position = c_start_position
        if self.hasFocus() and self.cursor_visible:
            qp.drawLine(cursor_pixel_position, 4, cursor_pixel_position, 28 - 4)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777234:  # left arrow
            self.cursor_position = max(0, self.cursor_position - 1)
            self.set_cursor_visible()
            self.update()
        elif key == 16777236:  # right arrow
            self.cursor_position = min(len(self.text), self.cursor_position + 1)
            self.set_cursor_visible()
            self.update()
        elif key == 16777219:  # Backspace
            if self.cursor_position > 0:
                self.text.pop(self.cursor_position - 1)
                self.cursor_position -= 1
                self.set_cursor_visible()
                self.update()
        elif key == 16777223:  # Del
            if self.cursor_position < len(self.text):
                self.text.pop(self.cursor_position)
                self.set_cursor_visible()
                self.update()
        else:
            mod = int(event.modifiers())
            print(
                "Key 0x{:d}/{}/ {} {} {}".format(
                    key,
                    event.text(),
                    "  [+shift]" if event.modifiers() & Qt.SHIFT else "",
                    "  [+ctrl]" if event.modifiers() & Qt.CTRL else "",
                    "  [+alt]" if event.modifiers() & Qt.ALT else ""
                )
            )
            if len(event.text()) > 0:
                self.text.insert(self.cursor_position, {"char": event.text()[0], "parse": True})
                self.cursor_position += 1
                self.set_cursor_visible()
                self.update()

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()

    def set_cursor_visible(self):
        self.cursor_visible = True
        self.cursor_timer.stop()
        self.cursor_timer.start(500)
