#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime, timedelta
import re


class ParsingInput(QWidget):
    def __init__(self):
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(28, 28)
        self.text = []
        self.parsed_blocks = []
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
        for i, c in enumerate(self.text):
            start_of_parsed_block = False
            end_of_parsed_block = False
            inside_parsed_block = False
            for start, end in self.parsed_blocks:
                if start == i:
                    block_width = 4
                    for char in self.text[start:end]:
                        block_width += font_metrics.width(char["char"])
                    qp.setPen(QColor(0, 0, 0))
                    qp.setBrush(QColor(0, 0, 0))
                    qp.drawRoundedRect(c_start_position+2, 4, block_width, 20, 2, 2)
                    start_of_parsed_block = True
                if end == i:
                    end_of_parsed_block = True
                if start <= i < end:
                    inside_parsed_block = True
            if end_of_parsed_block:
                c_start_position += 4
            if start_of_parsed_block:
                c_start_position += 4
            c_width = font_metrics.width(c["char"])
            if inside_parsed_block:
                qp.setBrush(QColor(0, 0, 0))
                qp.setPen(QColor(255, 255, 255))
            else:
                qp.setPen(QColor(0, 0, 0))
                qp.setBrush(QColor(255, 255, 255))
            qp.drawText(c_start_position, 20, c["char"])
            c_start_position += c_width
            if i == self.cursor_position - 1:
                cursor_pixel_position = c_start_position
        if self.hasFocus() and self.cursor_visible:
            qp.setPen(QColor(0, 0, 0))
            for start, end in self.parsed_blocks:
                if start < self.cursor_position <= end:
                    qp.setPen(QColor(255, 255, 255))
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
                self.parse_text()
                self.set_cursor_visible()
                self.update()
        elif key == 16777223:  # Del
            if self.cursor_position < len(self.text):
                self.text.pop(self.cursor_position)
                self.parse_text()
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
                self.parse_text()
                self.set_cursor_visible()
                self.update()

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update()

    def set_cursor_visible(self):
        self.cursor_visible = True
        self.cursor_timer.stop()
        self.cursor_timer.start(500)

    def get_text_str(self):
        return "".join([c["char"] for c in self.text])

    @staticmethod
    def generate_date(day, hour=None, minute=None):
        fuzziness = timedelta(days=1)
        date = datetime.now()
        if day in ["Morgen", "Tomorrow"]:
            date = datetime.now() + timedelta(days=1)
        try:
            if hour is not None and 0 <= int(hour) <= 24:
                if minute is not None and 0 <= int(minute) < 60:
                    date = datetime(year=date.year, month=date.month, day=date.day, hour=int(hour), minute=int(minute))
                else:
                    date = datetime(year=date.year, month=date.month, day=date.day, hour=int(hour), minute=0)
                fuzziness = 0
        except ValueError:
            print("Unexpected Values for hour ({}) and minute ({}). Ignoring.".format(hour, minute))
        return date, fuzziness

    def parse_text(self):
        regexes = [
            (re.compile(r"(Morgen|Tomorrow) (?:at |um )?(\d\d?):(\d\d?)"), self.generate_date),
            (re.compile(r"(Morgen|Tomorrow)"), self.generate_date)
        ]
        text = self.get_text_str()
        self.parsed_blocks = []
        for regex, generator in regexes:
            matches = regex.finditer(text)
            for match in matches:
                if match.end() > 0 and self.text[match.end()-1]["parse"]:
                    print(match.groups())
                    print(generator(*match.groups()))
                    text = text[:match.start()] + " "*(match.end()-match.start()) + text[match.end():]
                    self.parsed_blocks.append((match.start(), match.end()))

