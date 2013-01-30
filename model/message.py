#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import time
from lib.query import Query

class MessageModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "message"
        super(MessageModel, self).__init__()

    def add_new_message(self, message_info):
        return self.data(message_info).add()

    def get_user_unread_message_count(self, uid):
        where = "status = 0 AND to_user_id = %s" % uid
        return self.where(where).count()

    def get_user_all_messages(self, uid, num = 16, current_page = 1):
        where = "from_user_id = %s OR to_user_id = %s" % (uid, uid)
        join = "LEFT JOIN user AS from_user ON message.from_user_id = from_user.uid \
                LEFT JOIN user AS to_user ON message.to_user_id = to_user.uid "
        order = "id DESC"
        field = "message.*, \
                from_user.username as from_user_username, \
                from_user.nickname as from_user_nickname, \
                from_user.avatar as from_user_avatar, \
                from_user.uid as from_user_uid, \
                to_user.username as to_user_username, \
                to_user.nickname as to_user_nickname, \
                to_user.avatar as to_user_avatar, \
                to_user.uid as to_user_uid"
        return self.where(where).join(join).field(field).order(order).pages(current_page = current_page, list_rows = num)

    def get_messages(self, from_uid, to_uid, num = 16, current_page = 1):
        where = "(from_user_id = %s AND to_user_id = %s) OR (from_user_id = %s AND to_user_id = %s)" % (from_uid, to_uid, to_uid, from_uid)
        join = "LEFT JOIN user AS from_user ON message.from_user_id = from_user.uid \
                LEFT JOIN user AS to_user ON message.to_user_id = to_user.uid "
        order = "id DESC"
        field = "message.*, \
                from_user.username as from_user_username, \
                from_user.nickname as from_user_nickname, \
                from_user.avatar as from_user_avatar, \
                from_user.uid as from_user_uid, \
                to_user.username as to_user_username, \
                to_user.nickname as to_user_nickname, \
                to_user.avatar as to_user_avatar, \
                to_user.uid as to_user_uid"
        return self.where(where).join(join).field(field).order(order).pages(current_page = current_page, list_rows = num)

    def mark_user_unread_message_as_read(self, uid):
        where = "status = 0 AND to_user_id = %s" % (uid)
        return self.where(where).data({"status": 1}).save()

