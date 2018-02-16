#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QTextCursor, QTextDocument
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from datetime import datetime, timedelta
from task import Task
import re
ALL_CHARACTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÜÖÄẞ ßüöäabcdefghijklmnopqrstuvwxyz0987654321" +
                      "^°§ℓ»«$€„“”—`-,–.•´~$|~`+%\"';\\/{}*?()-:@…_[]^!<>=&ſ/¹²³›‹¢¥‚‘’°")


class ParsingInput(QWidget):
    edit_complete = pyqtSignal(Task)

    def __init__(self):
        super().__init__(flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint |
                         Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(28, 28)
        self.text = []
        self.character_offsets = [5]
        self.parsed_blocks = []
        self.qt_text = QTextDocument("")
        self.cursor = QTextCursor(self.qt_text)
        self.cursor.setPosition(0)
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
            if self.cursor.hasSelection() and self.cursor.selectionStart() <= i < self.cursor.selectionEnd():
                if start_of_parsed_block or end_of_parsed_block:
                    sel_rect_start = c_start_position - 2
                    sel_rect_width = font_metrics.width(c["char"]) + 4
                else:
                    sel_rect_start = c_start_position
                    sel_rect_width = font_metrics.width(c["char"])
                if i != self.cursor.selectionStart():
                    sel_rect_start += 2
                if i + 1 != self.cursor.selectionEnd():
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
            if i == self.cursor.position() - 1:
                cursor_pixel_position = c_start_position
            self.character_offsets.append(c_start_position)
        if self.hasFocus() and self.cursor_visible:
            qp.setPen(QColor(0, 0, 0))
            for start, end in self.parsed_blocks:
                if start < self.cursor.position() <= end:
                    qp.setPen(QColor(255, 255, 255))
            qp.drawLine(cursor_pixel_position, 4, cursor_pixel_position, 28 - 4)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if event.modifiers() & Qt.CTRL:
                new_pos = max(0, self.get_text_str().rfind(" ", 0, max(0, self.cursor.position() - 1)))
            else:
                new_pos = self.cursor.position() - 1
            if event.modifiers() & Qt.SHIFT:
                if self.cursor.hasSelection():
                    self.cursor.setPosition(max(0, new_pos), mode=QTextCursor.KeepAnchor)
                else:
                    self.cursor.setPosition(self.cursor.position(), mode=QTextCursor.MoveAnchor)
                    self.cursor.setPosition(max(0, new_pos), mode=QTextCursor.KeepAnchor)
            else:
                self.cursor.setPosition(max(0, new_pos))
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_Right:
            if event.modifiers() & Qt.CTRL:
                next_space = self.get_text_str().find(" ", self.cursor.position() + 1, len(self.text))
                if next_space < 0:
                    new_pos = len(self.text)
                else:
                    new_pos = next_space
            else:
                new_pos = self.cursor.position() + 1
            if event.modifiers() & Qt.SHIFT:
                if self.cursor.hasSelection():
                    self.cursor.setPosition(max(0, new_pos), mode=QTextCursor.KeepAnchor)
                else:
                    self.cursor.setPosition(self.cursor.position(), mode=QTextCursor.MoveAnchor)
                    self.cursor.setPosition(max(0, new_pos), mode=QTextCursor.KeepAnchor)
            else:
                self.cursor.setPosition(min(len(self.text), new_pos))
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_Home:
            if event.modifiers() & Qt.SHIFT:
                if self.cursor.hasSelection():
                    self.cursor.setPosition(0, mode=QTextCursor.KeepAnchor)
                else:
                    self.cursor.setPosition(self.cursor.position(), mode=QTextCursor.MoveAnchor)
                    self.cursor.setPosition(0, mode=QTextCursor.KeepAnchor)
            else:
                self.cursor.setPosition(0)
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_End:
            if event.modifiers() & Qt.SHIFT:
                if self.cursor.hasSelection():
                    self.cursor.setPosition(len(self.text), mode=QTextCursor.KeepAnchor)
                else:
                    self.cursor.setPosition(self.cursor.position(), mode=QTextCursor.MoveAnchor)
                    self.cursor.setPosition(len(self.text), mode=QTextCursor.KeepAnchor)
            else:
                self.cursor.setPosition(len(self.text))
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_Escape:
            self.cursor.clearSelection()
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_Backspace:
            something_changed = False
            if self.cursor.hasSelection():
                self.delete_selected_text()
                something_changed = True
            else:
                if self.cursor.position() > 0:
                    self.text.pop(self.cursor.position() - 1)
                    self.cursor.setPosition(self.cursor.position() - 1)
                    something_changed = True
            if something_changed:
                self.parse_text()
                self.set_cursor_visible()
                self.update()
        elif key == Qt.Key_Delete:
            something_changed = False
            if self.cursor.hasSelection():
                self.delete_selected_text()
                something_changed = True
            else:
                if self.cursor.position() < len(self.text):
                    self.text.pop(self.cursor.position())
                    something_changed = True
            if something_changed:
                self.parse_text()
                self.set_cursor_visible()
                self.update()
        elif key == Qt.Key_C and event.modifiers() & Qt.CTRL:
            selected_text = self.get_selected_text()
            print("Selected Text: {}".format(selected_text))
            if len(selected_text) > 0:
                QApplication.clipboard().setText(selected_text)
        elif key == Qt.Key_V and event.modifiers() & Qt.CTRL:
            self.delete_selected_text()
            clipboard_text = QApplication.clipboard().text()
            self.text = self.text[:self.cursor.position()] + \
                [{"char": c, "parse": True} for c in clipboard_text] + \
                self.text[self.cursor.position():]
            self.parse_text()
            self.cursor.setPosition(self.cursor.position() + len(clipboard_text))
            self.set_cursor_visible()
            self.update()
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.edit_complete.emit(self.get_task())
        else:
            if len(event.text()) > 0:
                typed_text = ""
                for c in event.text():
                    if c in ALL_CHARACTERS:
                        typed_text += c
                if len(typed_text):
                    self.delete_selected_text()
                    self.text = self.text[:self.cursor.position()] + \
                        [{"char": c, "parse": True} for c in typed_text] + \
                        self.text[self.cursor.position():]
                    self.parse_text()
                    self.cursor.setPosition(self.cursor.position() + len(typed_text))
                    self.set_cursor_visible()
                    self.update()

    def get_selected_text(self):
        if self.cursor.hasSelection():
            return "".join([c["char"] for c in self.text[self.cursor.selectionStart():self.cursor.selectionEnd()]])
        else:
            return ""

    def delete_selected_text(self):
        if self.cursor.hasSelection():
            start_pos = self.cursor.selectionStart()
            self.text = self.text[:start_pos] + self.text[self.cursor.selectionEnd():]
            self.cursor.clearSelection()
            self.cursor.setPosition(start_pos)

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
        self.cursor.select(QTextCursor.BlockUnderCursor)
        self.cursor.setPosition(self.get_min_dist_pos(event.pos().x()), mode=QTextCursor.MoveAnchor)
        self.update()

    def mouseMoveEvent(self, event):
        self.cursor.setPosition(self.get_min_dist_pos(event.pos().x()), mode=QTextCursor.KeepAnchor)
        self.update()

    def mouseReleaseEvent(self, event):
        self.cursor.setPosition(self.get_min_dist_pos(event.pos().x()), mode=QTextCursor.KeepAnchor)
        if self.cursor.selectionStart() == self.cursor.selectionEnd():
            self.cursor.clearSelection()
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
        saved_cursor_pos = self.cursor.position()
        self.qt_text.setPlainText(text)
        self.cursor.setPosition(saved_cursor_pos)
        self.parsed_blocks = []
        for regex, generator in regexes:
            matches = regex.finditer(text)
            for match in matches:
                if match.end() > 0 and self.text[match.end()-1]["parse"]:
                    print(match.groups())
                    print(generator(*match.groups()))
                    text = text[:match.start()] + " "*(match.end()-match.start()) + text[match.end():]
                    self.parsed_blocks.append((match.start(), match.end()))

    def get_task(self):
        new_task = Task()
        new_task.text = self.get_text_str()
        return new_task
