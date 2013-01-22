#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2012 F2E.im
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import time
from lib.query import Query

class CollegeModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "college"
        super(CollegeModel, self).__init__()

    def get_all_colleges(self):
        return self.select()

    def get_all_colleges_count(self):
        return self.count()

    def get_college_by_college_id(self, college_id):
        where = "id = '%s'" % college_id
        return self.where(where).find()

    def get_college_by_college_name(self, college_name):
        where = "name = '%s'" % college_name
        return self.where(where).find()

    def get_all_hot_colleges(self):
        where = "topic.reply_count > 0"
        join = "LEFT JOIN topic ON college.id = topic.college_id"
        order = "topic.reply_count DESC"
        group = "college.id"
        return self.where(where).join(join).order(order).group(group).limit(16).select()

