#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime, date, time
import json


class Task(object):
    def __init__(self, text="", due_date=None, due_date_fuzziness=None, weight=None, depends_on=[], sub_tasks=[]):
        self.text = text
        self.due_date = due_date
        self.due_date_fuzziness = due_date_fuzziness
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

    def to_json(self):
        return json.dumps({
            'text': self.text,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'due_date_fuzziness': self.due_date_fuzziness,
            'not_before': self.not_before.isoformat() if self.due_date else None,
            'expected_duration': self.expected_duration,
            'location': self.location,
            'weight': self.weight,
            'urgency': self.urgency,
            'depends_on': self.depends_on,
            'sub_tasks': self.sub_tasks,
            'repeat': self.repeat,
            'finished': self.finished
        })


class TaskFactory(object):
    @staticmethod
    def from_json(task_json):
        t = Task(text=task_json['text'],
                 due_date=datetime.strptime(task_json['due_date'], "YYYY-MM-DDTHH:MM:SS"),
                 due_date_fuzziness=task_json['due_date_fuzziness'],
                 weight=task_json['weight'])
        if task_json['not_before']:
            t.not_before = datetime.strptime(task_json['not_before'], "YYYY-MM-DDTHH:MM:SS")
        for task_id in task_json['depends_on']:
            t.depends_on.append(TaskFactory.find_task(task_id))
        for task_id in task_json['sub_tasks']:
            t.sub_tasks.append(TaskFactory.find_task(task_id))
        return t

    @staticmethod
    def find_task(task_id):
        pass
