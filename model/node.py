#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import time
from lib.query import Query

class NodeModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "node"
        super(NodeModel, self).__init__()

    def get_all_nodes(self):
        return self.select()

    def get_all_nodes_count(self):
        return self.count()

    def get_nodes_by_plane_id(self, plane_id):
        where = "plane_id = %s" % plane_id
        return self.where(where).select()

    def get_node_by_node_slug(self, node_slug):
        where = "slug = '%s'" % node_slug
        return self.where(where).find()

    def get_all_hot_nodes(self):
        where = "topic.reply_count > 0"
        join = "LEFT JOIN topic ON node.id = topic.node_id"
        order = "topic.reply_count DESC"
        group = "node.id"
        return self.where(where).join(join).order(order).group(group).limit(16).select()

    def set_node_topic_count_by_node_slug(self, node_slug, topic_count):
        where = "slug = '%s'" % node_slug
        return self.data({
            "topic_count": topic_count
        }).where(where).save()

