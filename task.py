#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime, date, time


class Task(object):
    def __init__(self, text="", due_date=None, due_date_fuzziness=None, weight=None, depends_on=[], sub_tasks=[]):
        self.text = text
        self.due_date = due_date
        self.due_date_fuzziness = due_date_fuzziness
        self.end_date = None
        self.not_before = datetime.now()
        self.expected_duration = None
        self.location = None
        self.weight = weight
        self.urgency = None
        self.depends_on = depends_on
        self.sub_tasks = sub_tasks
        self.repeat = None
        self.finished = False

    def __repr__(self):
        return "<Task: {}>".format(self.text)

    def get_color(self):
        if self.due_date and datetime.now() > self.due_date:
            return 200, 0, 0
        else:
            return 90, 90, 255

    def get_progress(self):
        if len(self.sub_tasks) <= 0:
            return 0.0
        finished_sub_tasks = 0
        for sub_task in self.sub_tasks:
            if sub_task.finished:
                finished_sub_tasks += 1
        return finished_sub_tasks/len(self.sub_tasks)

    def set_due_date(self, new_date):
        if self.due_date:
            self.due_date = datetime.combine(new_date, self.due_date.time())
        else:
            self.due_date = datetime.combine(new_date, time(hour=12, minute=0))

    def set_due_date_time(self, new_time):
        if self.due_date:
            self.due_date = datetime.combine(self.due_date.date(), new_time)
        else:
            self.due_date = datetime.combine(date.today(), new_time)

    def get_due_date_time(self):
        if self.due_date:
            return self.due_date.time
        else:
            return None
