#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime


class Task(object):
    def __init__(self):
        self.text = ""
        self.due_date = None
        self.due_date_fuzziness = None
        self.end_date = None
        self.not_before = datetime.now()
        self.expected_duration = None
        self.location = None
        self.weight = None
        self.urgency = None
        self.depends_on = []
        self.sub_tasks = []
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
