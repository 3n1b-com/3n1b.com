#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import time
from lib.query import Query

class PlaneModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "plane"
        super(PlaneModel, self).__init__()

    def get_all_planes(self):
        return self.select()

    def get_all_planes_with_nodes(self):
        planes = self.get_all_planes()

        for plane in planes:
            where = "plane_id = %s" % plane["id"]
            order = "node.topic_count DESC"
            plane["nodes"] = self.table("node").where(where).order(order).select()

        return planes

    def get_plane_by_plane_id(self):
        where = ""
        planes = self.get_all_planes()

        for plane in planes:
            where = "plane_id = %s" % plane["id"]
            plane["nodes"] = self.table("node").where(where).select()

        return planes

