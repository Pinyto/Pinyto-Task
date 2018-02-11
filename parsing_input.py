#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication
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
        self.character_offsets = [5]
        self.parsed_blocks = []
        self.selection = None
        self.selection_start = None
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
        self.character_offsets = [cursor_pixel_position]
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
            if self.selection and self.selection[0] <= i < self.selection[1]:
                if start_of_parsed_block or end_of_parsed_block:
                    sel_rect_start = c_start_position - 2
                    sel_rect_width = font_metrics.width(c["char"]) + 4
                else:
                    sel_rect_start = c_start_position
                    sel_rect_width = font_metrics.width(c["char"])
                if i != self.selection[0]:
                    sel_rect_start += 2
                if i + 1 != self.selection[1]:
                    sel_rect_width += 2
                else:
                    sel_rect_width -= 2
                if not inside_parsed_block:
                    selection_color = QColor(100, 100, 255)
                else:
                    selection_color = QColor(60, 60, 168)
                qp.setBrush(selection_color)
                qp.setPen(selection_color)
                qp.drawRect(sel_rect_start, 6, sel_rect_width, 16)
            qp.setPen(QColor(inside_parsed_block*255,
                             inside_parsed_block*255,
                             inside_parsed_block*255))
            qp.setBrush(QColor(255-inside_parsed_block*255,
                               255-inside_parsed_block*255,
                               255-inside_parsed_block*255))
            qp.drawText(c_start_position, 20, c["char"])
            c_start_position += c_width
            if i == self.cursor_position - 1:
                cursor_pixel_position = c_start_position
            self.character_offsets.append(c_start_position)
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
            something_changed = False
            if self.selection:
                self.delete_selected_text()
                something_changed = True
            else:
                if self.cursor_position > 0:
                    self.text.pop(self.cursor_position - 1)
                    self.cursor_position -= 1
                    something_changed = True
            if something_changed:
                self.parse_text()
                self.set_cursor_visible()
                self.update()
        elif key == 16777223:  # Del
            something_changed = False
            if self.selection:
                self.delete_selected_text()
                something_changed = True
            else:
                if self.cursor_position < len(self.text):
                    self.text.pop(self.cursor_position)
                    something_changed = True
            if something_changed:
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
                self.delete_selected_text()
                self.cursor_position += 1
                self.parse_text()
                self.set_cursor_visible()
                self.update()

    def delete_selected_text(self):
        if self.selection:
            print(self.selection)
            self.cursor_position = self.selection[0]
            self.text = self.text[:self.selection[0]] + self.text[self.selection[1]:]
            self.selection = None
            self.selection_start = None

    def get_min_dist_pos(self, click_x):
        min_dist_pos = 0
        min_dist = abs(self.character_offsets[0] - click_x)
        for i, offset in enumerate(self.character_offsets[1:]):
            d = abs(offset - click_x)
            if d < min_dist:
                min_dist = d
                min_dist_pos = i + 1
        return min_dist_pos

    def mousePressEvent(self, event):
        self.cursor_position = self.get_min_dist_pos(event.pos().x())
        self.selection = (self.cursor_position, self.cursor_position)
        self.selection_start = self.cursor_position

    def mouseMoveEvent(self, event):
        self.cursor_position = self.get_min_dist_pos(event.pos().x())
        if self.selection_start < self.cursor_position:
            self.selection = (self.selection_start, self.cursor_position)
        else:
            self.selection = (self.cursor_position, self.selection_start)

    def mouseReleaseEvent(self, event):
        self.cursor_position = self.get_min_dist_pos(event.pos().x())
        if self.selection_start < self.cursor_position:
            self.selection = (self.selection_start, self.cursor_position)
        else:
            self.selection = (self.cursor_position, self.selection_start)
        if self.selection[0] == self.selection[1]:
            self.selection = None
        self.selection_start = None

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

