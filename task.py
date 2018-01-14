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
        self.weight = None
        self.urgency = None
        self.depends_on = []
        self.sub_tasks = []
        self.repeat = None
