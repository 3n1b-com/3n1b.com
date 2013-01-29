#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import time
from lib.query import Query

class ProvinceModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "province"
        super(ProvinceModel, self).__init__()

    def get_all_provinces(self):
        return self.select()

    def get_all_provinces_with_colleges(self):
        provinces = self.get_all_provinces()

        for province in provinces:
            where = "pid = %s" % province["id"]
            province["colleges"] = self.table("college").where(where).select()

        return provinces