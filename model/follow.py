#!/usr/bin/env python
# coding=utf-8
#
## Copyright 2013 3n1b.com

import time
from lib.query import Query

class FollowModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "follow"
        super(FollowModel, self).__init__()

    def add_new_follow(self, follow_info):
        return self.data(follow_info).add()

    def get_follow_info_by_user_id_and_follow_user_id(self, user_id, follow_user_id):
        where = "user_id = %s AND follow_user_id = %s" % (user_id, follow_user_id)
        return self.where(where).find()

    def delete_follow_info_by_user_id_and_follow_user_id(self, user_id, follow_user_id):
        where = "user_id = %s AND follow_user_id = %s" % (user_id, follow_user_id)
        return self.where(where).delete()

    def get_user_follow_count(self, user_id):
        where = "user_id = %s" % user_id
        return self.where(where).count()

    def get_user_all_follow_topics(self, user_id, num = 16, current_page = 1):
        where = "follow.user_id = %s" % user_id
        join = "RIGHT JOIN topic ON follow.follow_user_id = topic.author_id \
                LEFT JOIN user AS author_user ON topic.author_id = author_user.uid \
                LEFT JOIN college ON topic.college_id = college.id \
                LEFT JOIN node ON topic.node_id = node.id \
                LEFT JOIN user AS last_replied_user ON topic.last_replied_by = last_replied_user.uid"
        order = "topic.last_touched DESC, topic.created DESC, topic.last_replied_time DESC, topic.id DESC"
        field = "topic.*, \
                author_user.username as author_username, \
                author_user.nickname as author_nickname, \
                author_user.avatar as author_avatar, \
                author_user.uid as author_uid, \
                author_user.reputation as author_reputation, \
                node.name as node_name, \
                node.slug as node_slug, \
                college.name as college_name, \
                college.id as college_id, \
                last_replied_user.username as last_replied_username, \
                last_replied_user.nickname as last_replied_nickname"
        return self.where(where).order(order).join(join).field(field).pages(current_page = current_page, list_rows = num)

