#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import uuid
import hashlib
import Image
import StringIO
import time
import json
import re
import urllib2
import tornado.web
import lib.jsonp
import pprint
import math
import datetime

from base import *
from lib.variables import *
from form.topic import *
from lib.variables import gen_random
from lib.xss import XssCleaner
from lib.utils import find_mentions

class CreateMessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, username = None, template_variables = {}):
        user_info = self.current_user
        to_user = self.user_model.get_user_by_username(username)
        if (user_info["uid"] == to_user["uid"]):
            self.redirect("/")
        template_variables["user_info"] = user_info
        template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
        }       
        template_variables["to_user"] = to_user
        template_variables["gen_random"] = gen_random
        page = int(self.get_argument("p", "1"))
        template_variables["messages"] = self.message_model.get_messages(user_info["uid"], to_user["uid"], current_page = page)
        self.message_model.mark_user_unread_message_as_read(user_info["uid"])
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("message/create_message.html", **template_variables)

    @tornado.web.authenticated
    def post(self, username = None, template_variables = {}):
        user_info = self.current_user
        to_user = self.user_model.get_user_by_username(username)

        template_variables = {}

        # validate the fields

        form = CreateMessageForm(self)

        if not form.validate():
            self.get(username, {"errors": form.errors})
            return

        # continue while validate succeed
        
        message_info = {
            "content": form.content.data,
            "status": 0,
            "from_user_id": user_info["uid"],
            "to_user_id": to_user["uid"],
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        self.message_model.add_new_message(message_info)

        self.redirect("/m/"+username)

class MessagesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, username = None, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
        }
        template_variables["gen_random"] = gen_random
        page = int(self.get_argument("p", "1"))
        template_variables["messages"] = self.message_model.get_user_all_messages(user_info["uid"], current_page = page)
        self.message_model.mark_user_unread_message_as_read(user_info["uid"])
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("message/messages.html", **template_variables)