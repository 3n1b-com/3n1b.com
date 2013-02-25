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

class IndexHandler(BaseHandler):
    def get(self, template_variables = {}):
        tab = self.get_argument('tab', "index")
        user_info = self.current_user
        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        user_college = self.college_model.get_college_by_college_id(1001)
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            }
            user_college = self.college_model.get_college_by_college_name(user_info["collegename"])
            if(tab=="index"):
                template_variables["topics"] = self.topic_model.get_all_topics(current_page = page)           
            if(tab=="college"):
                template_variables["topics"] = self.topic_model.get_all_topics_by_college_id(current_page = page, college_id = user_college.id)
            if(tab=="interest"):
                template_variables["topics"] = self.interest_model.get_user_all_interest_topics(user_id = user_info["uid"], current_page = page)
            if(tab=="follows"):
                template_variables["topics"] = self.follow_model.get_user_all_follow_topics(user_id = user_info["uid"], current_page = page)
        else:
            if(tab=="college"):
                self.redirect("/login?next=/?tab=college")
            if(tab=="interest"):
                self.redirect("/login?next=/?tab=interest")
            if(tab=="follows"):
                self.redirect("/login?next=/?tab=follows")
            template_variables["topics"] = self.topic_model.get_all_topics(current_page = page);
        template_variables["college"] = user_college
        template_variables["status_counter"] = {
            "users": self.user_model.get_all_users_count(),
            "nodes": self.node_model.get_all_nodes_count(),
            "topics": self.topic_model.get_all_topics_count(),
            "replies": self.reply_model.get_all_replies_count(),
        }
        template_variables["node"] = self.node_model.get_node_by_node_slug("qna")
        if(tab=="index"):
            template_variables["active_page"] = "topic"           
        else:
            template_variables["active_page"] = tab      
        template_variables["planes"] = self.plane_model.get_all_planes_with_nodes()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()        
        template_variables["gen_random"] = gen_random    
        notice_text = "暂时还没有话题，发出您的讨论吧。"
        if (tab == "college"):
            notice_text = "你学校下暂时还没有话题，发出您的讨论吧。"
        if (tab == "interest"):
            notice_text = "这里列出了您所关注小组下的最新话题，暂时还没有话题，发出您的讨论吧。"
        if (tab == "follows"):
            notice_text = "这里列出了您所关注同学的最新话题，暂时还没有话题，发出你的讨论吧。"
        template_variables["notice_text"] = notice_text
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("topic/topics.html", **template_variables)

class NodeTopicsHandler(BaseHandler):
    def get(self, node_slug, template_variables = {}):
        user_info = self.current_user
        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        user_college = self.college_model.get_college_by_college_id(1001)
        current_node = self.node_model.get_node_by_node_slug(node_slug);
        follow_text = "+关注"
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
            user_college = self.college_model.get_college_by_college_name(user_info["collegename"])
            interest = self.interest_model.get_interest_info_by_user_id_and_node_id(user_info["uid"], current_node.id)
            if(interest):
                follow_text = "取消关注"
        template_variables["follow_text"] = follow_text
        template_variables["college"] = user_college
        template_variables["topics"] = self.topic_model.get_all_topics_by_node_slug(current_page = page, node_slug = node_slug)
        template_variables["node"] = current_node;
        template_variables["active_page"] = "topic"
        template_variables["gen_random"] = gen_random
        wallpaper = current_node["custom_style"]
        if (wallpaper == ""):
            wallpaper = self.get_wallpaper()
        template_variables["wallpaper"] = wallpaper
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/node_topics.html", **template_variables)

class CollegeTopicsHandler(BaseHandler):
    def get(self, college_id, template_variables = {}):
        user_info = self.current_user
        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
        template_variables["topics"] = self.topic_model.get_all_topics_by_college_id(current_page = page, college_id = college_id)
        template_variables["college"] = self.college_model.get_college_by_college_id(college_id)
        template_variables["node"] = self.node_model.get_node_by_node_slug("qna")
        template_variables["active_page"] = "topic"
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/college_topics.html", **template_variables)

class ViewHandler(BaseHandler):
    def get(self, topic_id, template_variables = {}):
        user_info = self.current_user
        page = int(self.get_argument("p", "1"))
        user_info = self.get_current_user()
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
        template_variables["gen_random"] = gen_random
        template_variables["topic"] = self.topic_model.get_topic_by_topic_id(topic_id)

        # check reply count and cal current_page if `p` not given
        reply_num = 16
        reply_count = template_variables["topic"]["reply_count"]
        reply_last_page = (reply_count / reply_num + (reply_count % reply_num and 1)) or 1
        page = int(self.get_argument("p", reply_last_page))
        template_variables["reply_num"] = reply_num
        template_variables["current_page"] = page

        template_variables["replies"] = self.reply_model.get_all_replies_by_topic_id(topic_id, current_page = page)
        template_variables["active_page"] = "topic"
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()  

        # update topic reply_count and hits

        self.topic_model.update_topic_by_topic_id(topic_id, {
            "reply_count": template_variables["replies"]["page"]["total"],
            "hits": (template_variables["topic"]["hits"] or 0) + 1,
        })

        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("topic/view.html", **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = ReplyForm(self)

        if not form.validate():
            self.get(form.tid.data, {"errors": form.errors})
            return

        # continue while validate succeed

        topic_info = self.topic_model.get_topic_by_topic_id(form.tid.data)
        replied_info = self.reply_model.get_user_reply_by_topic_id(self.current_user["uid"], form.tid.data)

        if(not topic_info):
            template_variables["errors"] = {}
            template_variables["errors"]["invalid_topic_info"] = [u"要回复的帖子不存在"]
            self.get(template_variables)
            return
        
        reply_info = {
            "author_id": self.current_user["uid"],
            "topic_id": form.tid.data,
            # "content": XssCleaner().strip(form.content.data),
            "content": form.content.data,
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        reply_id = self.reply_model.add_new_reply(reply_info)

        # update topic last_replied_by and last_replied_time

        self.topic_model.update_topic_by_topic_id(form.tid.data, {
            "last_replied_by": self.current_user["uid"],
            "last_replied_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "last_touched": time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        # create reply notification

        if not self.current_user["uid"] == topic_info["author_id"]:
            self.notification_model.add_new_notification({
                "trigger_user_id": self.current_user["uid"],
                "involved_type": 1, # 0: mention, 1: reply
                "involved_user_id": topic_info["author_id"],
                "involved_topic_id": form.tid.data,
                "content": form.content.data,
                "status": 0,
                "occurrence_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # create @username notification

        for username in set(find_mentions(form.content.data)):
            print username
            mentioned_user = self.user_model.get_user_by_username(username)

            if not mentioned_user:
                continue

            if mentioned_user["uid"] == self.current_user["uid"]:
                continue

            if mentioned_user["uid"] == topic_info["author_id"]:
                continue

            self.notification_model.add_new_notification({
                "trigger_user_id": self.current_user["uid"],
                "involved_type": 0, # 0: mention, 1: reply
                "involved_user_id": mentioned_user["uid"],
                "involved_topic_id": form.tid.data,
                "content": form.content.data,
                "status": 0,
                "occurrence_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        # update reputation of topic author
        if not self.current_user["uid"] == topic_info["author_id"] and not replied_info:
            topic_time_diff = datetime.datetime.now() - topic_info["created"]
            reputation = topic_info["author_reputation"] or 0
            reputation = reputation + 2 * math.log(self.current_user["reputation"] or 0 + topic_time_diff.days + 10, 10)
            self.user_model.set_user_base_info_by_uid(topic_info["author_id"], {"reputation": reputation})

        # self.get(form.tid.data)
        self.redirect("/t/%s#reply%s" % (form.tid.data, topic_info["reply_count"] + 1))

class CreateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, college_node = None, template_variables = {}):
        user_info = self.current_user
        if (user_info["collegename"]=="请设置您的学校"):
            self.redirect(self.get_argument("next", "/register/college"))
        template_variables["user_info"] = user_info
        template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
            "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
        }
        template_variables["gen_random"] = gen_random
        college_id = self.get_argument('c', "0")
        node_slug = self.get_argument('n', "qna")
        node = self.node_model.get_node_by_node_slug(node_slug)
        college = self.college_model.get_college_by_college_id(college_id)
        template_variables["node"] = node
        template_variables["college"] = college
        template_variables["active_page"] = "topic"
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/create.html", **template_variables)

    @tornado.web.authenticated
    def post(self, college_node = None, template_variables = {}):
        print "CreateHandler:post"
        template_variables = {}

        college_id = self.get_argument('c', "0")
        node_slug = self.get_argument('n', "qna")
        node = self.node_model.get_node_by_node_slug(node_slug)
        college = self.college_model.get_college_by_college_id(college_id)

        # validate the fields
        form = CreateForm(self)

        if not form.validate():
            self.get(node_slug, {"errors": form.errors})
            return

        # continue while validate succeed
        
        topic_info = {
            "author_id": self.current_user["uid"],
            "title": form.title.data,
            # "content": XssCleaner().strip(form.content.data),
            "content": form.content.data,
            "node_id": node["id"],
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            "reply_count": 0,
            "last_touched": time.strftime('%Y-%m-%d %H:%M:%S'),
            "college_id": college["id"],
        }

        reply_id = self.topic_model.add_new_topic(topic_info)

        # update toptic count of the node
        topic_count = node["topic_count"] + 1
        self.node_model.set_node_topic_count_by_node_slug(node_slug, topic_count)

        # update reputation of topic author
        reputation = self.current_user["reputation"] or 0
        reputation = reputation - 5
        reputation = 0 if reputation < 0 else reputation
        self.user_model.set_user_base_info_by_uid(topic_info["author_id"], {"reputation": reputation})
        self.redirect("/")

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, topic_id, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
            "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
        }
        template_variables["topic"] = self.topic_model.get_topic_by_topic_id(topic_id)
        template_variables["gen_random"] = gen_random
        template_variables["active_page"] = "topic"
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/edit.html", **template_variables)

    @tornado.web.authenticated
    def post(self, topic_id, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = CreateForm(self)

        if not form.validate():
            self.get(topic_id, {"errors": form.errors})
            return

        # continue while validate succeed

        topic_info = self.topic_model.get_topic_by_topic_id(topic_id)

        if(not topic_info["author_id"] == self.current_user["uid"]):
            template_variables["errors"] = {}
            template_variables["errors"]["invalid_permission"] = [u"没有权限修改该话题"]
            self.get(topic_id, template_variables)
            return

        update_topic_info = {
            "title": form.title.data,
            # "content": XssCleaner().strip(form.content.data),
            "content": form.content.data,
            "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
            "last_touched": time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        reply_id = self.topic_model.update_topic_by_topic_id(topic_id, update_topic_info)

        # update reputation of topic author
        reputation = topic_info["author_reputation"] or 0
        reputation = reputation - 2
        reputation = 0 if reputation < 0 else reputation
        self.user_model.set_user_base_info_by_uid(topic_info["author_id"], {"reputation": reputation})
        self.redirect("/t/%s" % topic_id)

class ProfileHandler(BaseHandler):
    def get(self, user, template_variables = {}):
        current_user_info = self.current_user
        if(re.match(r'^\d+$', user)):
            user_info = self.user_model.get_user_by_uid(user)
        else:
            user_info = self.user_model.get_user_by_username(user)
        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        follow_text = "+关注"
        show_follow = True;
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
            if(current_user_info):
                if(user_info["uid"] == current_user_info["uid"]):
                    show_follow = False;
                else:
                    show_follow = True;
                    follow = self.follow_model.get_follow_info_by_user_id_and_follow_user_id(current_user_info["uid"], user_info["uid"])
                    if(follow):
                        follow_text = "取消关注"                     
        template_variables["follow_text"] = follow_text
        template_variables["show_follow"] = show_follow

        '''
        if user_info["github"]:
            github_repos = self.mc.get(str("%s_github_repos" % user_info["github"])) or json.JSONDecoder().decode(urllib2.urlopen('https://api.github.com/users/%s/repos' % user_info["github"]).read())
            self.mc.set(str("%s_github_repos" % user_info["github"]), github_repos)
            template_variables["github_repos"] = github_repos
        '''

        template_variables["topics"] = self.topic_model.get_user_all_topics(user_info["uid"], current_page = page)
        template_variables["replies"] = self.reply_model.get_user_all_replies(user_info["uid"], current_page = page)
        template_variables["gen_random"] = gen_random
        template_variables["active_page"] = "_blank"
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("topic/profile.html", **template_variables)

class VoteHandler(BaseHandler):
    def get(self, template_variables = {}):
        topic_id = int(self.get_argument("topic_id"))
        topic_info = self.topic_model.get_topic_by_topic_id(topic_id)

        if not topic_info:
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "topic_not_exist",
            }))
            return

        if self.current_user["uid"] == topic_info["author_id"]:
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "can_not_vote_your_topic",
            }))
            return

        if self.vote_model.get_vote_by_topic_id_and_trigger_user_id(topic_id, self.current_user["uid"]):
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "already_voted",
            }))
            return

        self.vote_model.add_new_vote({
            "trigger_user_id": self.current_user["uid"],
            "involved_type": 0, # 0: topic, 1: reply
            "involved_user_id": topic_info["author_id"],
            "involved_topic_id": topic_id,
            "status": 0,
            "occurrence_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        self.write(lib.jsonp.print_JSON({
            "success": 1,
            "message": "thanks_for_your_vote",
        }))

        # update reputation of topic author
        topic_time_diff = datetime.datetime.now() - topic_info["created"]
        reputation = topic_info["author_reputation"] or 0
        reputation = reputation + 2 * math.log(self.current_user["reputation"] or 0 + topic_time_diff.days + 10, 10)
        self.user_model.set_user_base_info_by_uid(topic_info["author_id"], {"reputation": reputation})

class UserTopicsHandler(BaseHandler):
    def get(self, user, template_variables = {}):
        if(re.match(r'^\d+$', user)):
            user_info = self.user_model.get_user_by_uid(user)
        else:
            user_info = self.user_model.get_user_by_username(user)

        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
        template_variables["topics"] = self.topic_model.get_user_all_topics(user_info["uid"], current_page = page)
        template_variables["active_page"] = "topic"
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/user_topics.html", **template_variables)

class UserRepliesHandler(BaseHandler):
    def get(self, user, template_variables = {}):
        if(re.match(r'^\d+$', user)):
            user_info = self.user_model.get_user_by_uid(user)
        else:
            user_info = self.user_model.get_user_by_username(user)

        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
        template_variables["replies"] = self.reply_model.get_user_all_replies(user_info["uid"], current_page = page)
        template_variables["active_page"] = "topic"
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/user_replies.html", **template_variables)

class UserFavoritesHandler(BaseHandler):
    def get(self, user, template_variables = {}):
        if(re.match(r'^\d+$', user)):
            user_info = self.user_model.get_user_by_uid(user)
        else:
            user_info = self.user_model.get_user_by_username(user)

        page = int(self.get_argument("p", "1"))
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
            }
        template_variables["favorites"] = self.favorite_model.get_user_all_favorites(user_info["uid"], current_page = page)
        template_variables["active_page"] = "topic"
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/user_favorites.html", **template_variables)

class ReplyEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, reply_id, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
            "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
        }
        template_variables["reply"] = self.reply_model.get_reply_by_reply_id(reply_id)
        template_variables["gen_random"] = gen_random
        template_variables["active_page"] = "topic"
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()
        self.render("topic/reply_edit.html", **template_variables)

    @tornado.web.authenticated
    def post(self, reply_id, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = ReplyEditForm(self)

        if not form.validate():
            self.get(reply_id, {"errors": form.errors})
            return

        # continue while validate succeed

        reply_info = self.reply_model.get_reply_by_reply_id(reply_id)

        if(not reply_info["author_id"] == self.current_user["uid"]):
            template_variables["errors"] = {}
            template_variables["errors"]["invalid_permission"] = [u"没有权限修改该回复"]
            self.get(reply_id, template_variables)
            return

        update_reply_info = {
            # "content": XssCleaner().strip(form.content.data),
            "content": form.content.data,
            "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        reply_id = self.reply_model.update_reply_by_reply_id(reply_id, update_reply_info)

        # update reputation of topic author
        reputation = self.current_user["reputation"] or 0
        reputation = reputation - 2
        reputation = 0 if reputation < 0 else reputation
        self.user_model.set_user_base_info_by_uid(reply_info["author_id"], {"reputation": reputation})
        self.redirect("/t/%s" % reply_info["topic_id"])

class FavoriteHandler(BaseHandler):
    def get(self, template_variables = {}):
        topic_id = int(self.get_argument("topic_id"))
        topic_info = self.topic_model.get_topic_by_topic_id(topic_id)

        if not topic_info:
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "topic_not_exist",
            }))
            return

        if self.current_user["uid"] == topic_info["author_id"]:
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "can_not_favorite_your_topic",
            }))
            return

        if self.favorite_model.get_favorite_by_topic_id_and_owner_user_id(topic_id, self.current_user["uid"]):
            self.write(lib.jsonp.print_JSON({
                "success": 0,
                "message": "already_favorited",
            }))
            return

        self.favorite_model.add_new_favorite({
            "owner_user_id": self.current_user["uid"],
            "involved_type": 0, # 0: topic, 1: reply
            "involved_topic_id": topic_id,
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        self.write(lib.jsonp.print_JSON({
            "success": 1,
            "message": "favorite_success",
        }))

        # update reputation of topic author
        topic_time_diff = datetime.datetime.now() - topic_info["created"]
        reputation = topic_info["author_reputation"] or 0
        reputation = reputation + 2 * math.log(self.current_user["reputation"] or 0 + topic_time_diff.days + 10, 10)
        self.user_model.set_user_base_info_by_uid(topic_info["author_id"], {"reputation": reputation})

class MembersHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
            "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
            "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
            "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
            "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
        }        
        template_variables["members"] = self.user_model.get_users_by_latest(num = 49)
        template_variables["active_members"] = self.user_model.get_users_by_last_login(num = 49)
        template_variables["gen_random"] = gen_random
        template_variables["active_page"] = "members"
        template_variables["wallpaper"] = self.get_wallpaper()
        template_variables["planes"] = self.plane_model.get_all_planes_with_nodes()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges() 
        self.render("topic/members.html", **template_variables)

class NodesHandler(BaseHandler):
    def get(self, college_node = None, template_variables = {}):
        print "NodesHandler:get"
        user_info = self.current_user
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            }
        template_variables["status_counter"] = {
            "users": self.user_model.get_all_users_count(),
            "nodes": self.node_model.get_all_nodes_count(),
            "topics": self.topic_model.get_all_topics_count(),
            "replies": self.reply_model.get_all_replies_count(),
        }
        college_id = self.get_argument('c', "0")
        college = self.college_model.get_college_by_college_id(college_id)
        if (self.request.path == "/nodes"):
            node_prefix = "/node/"
        else:
            node_prefix = "/t/create/?c="+ str(college.id) +"&n="              
        template_variables["college"] = college
        template_variables["node_prefix"] = node_prefix
        template_variables["planes"] = self.plane_model.get_all_planes_with_nodes()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()  
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()       
        template_variables["gen_random"] = gen_random 
        template_variables["active_page"] = "nodes"  
        template_variables["wallpaper"] = self.get_wallpaper()    
        self.render("topic/nodes.html", **template_variables)

class CollegesHandler(BaseHandler):
    def get(self, college_node = None, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "messages": self.message_model.get_user_unread_message_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            }
        template_variables["status_counter"] = {
            "users": self.user_model.get_all_users_count(),
            "nodes": self.node_model.get_all_nodes_count(),
            "topics": self.topic_model.get_all_topics_count(),
            "replies": self.reply_model.get_all_replies_count(),
        }
        node_slug = self.get_argument('n', "qna")
        node = self.node_model.get_node_by_node_slug(node_slug)
        template_variables["node"] = node
        if (self.request.path == "/colleges"):
            college_prefix = "/college/"
            college_postfix = ""
        else:
            college_prefix = "/t/create/?c="
            college_postfix = "&n=" + node.slug    
        template_variables["college_prefix"] = college_prefix
        template_variables["college_postfix"] = college_postfix   
        template_variables["provinces"] = self.province_model.get_all_provinces_with_colleges()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()
        template_variables["hot_colleges"] = self.college_model.get_all_hot_colleges()         
        template_variables["gen_random"] = gen_random       
        template_variables["active_page"] = "colleges" 
        template_variables["wallpaper"] = self.get_wallpaper() 
        self.render("topic/colleges.html", **template_variables)

class FollowNodeHandler(BaseHandler):
    def get(self, node_slug = None, template_variables = {}):
        user_info = self.current_user
        current_node = self.node_model.get_node_by_node_slug(node_slug);
        if(user_info):
            interest = self.interest_model.get_interest_info_by_user_id_and_node_id(user_info["uid"], current_node["id"])
            if(interest):
                self.interest_model.delete_interest_info_by_user_id_and_node_id(user_info["uid"], current_node["id"])
            else:
                self.interest_model.add_new_interest({
                    "user_id": user_info["uid"],
                    "node_id": current_node["id"],
                    "created": time.strftime('%Y-%m-%d %H:%M:%S'),
                })
            self.redirect("/node/"+node_slug)
        else:
            self.redirect("/login?next=/node/"+node_slug)   

class FollowUserHandler(BaseHandler):
    def get(self, user_name = None, template_variables = {}):
        user_info = self.current_user
        follow_user = self.user_model.get_user_by_username(user_name);
        if(user_info):
            follow = self.follow_model.get_follow_info_by_user_id_and_follow_user_id(user_info["uid"], follow_user["uid"])
            if(follow):
                self.follow_model.delete_follow_info_by_user_id_and_follow_user_id(user_info["uid"], follow_user["uid"])
            else:
                self.follow_model.add_new_follow({
                    "user_id": user_info["uid"],
                    "follow_user_id": follow_user["uid"],
                    "created": time.strftime('%Y-%m-%d %H:%M:%S'),
                })
            self.redirect("/u/"+user_name)
        else:
            self.redirect("/login?next=/u/"+user_name)   