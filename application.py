#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

# cat /etc/mime.types
# application/octet-stream    crx

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path
import re
import memcache
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import handler.base
import handler.user
import handler.topic
import handler.page
import handler.notification
import handler.message

from tornado.options import define, options
from lib.loader import Loader
from lib.session import Session, SessionManager
from jinja2 import Environment, FileSystemLoader

define("port", default = 80, help = "run on the given port", type = int)
define("mysql_host", default = "localhost", help = "community database host")
define("mysql_database", default = "3n1b", help = "community database name")
define("mysql_user", default = "3n1b", help = "community database user")
define("mysql_password", default = "3n1b", help = "community database password")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            blog_title = u"叁年壹班",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            cookie_secret = "cookie_secret_code",
            login_url = "/login",
            autoescape = None,
            jinja2 = Environment(loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")), trim_blocks = True),
            reserved = ["user", "topic", "home", "setting", "forgot", "login", "logout", "register", "admin"],
            debug=True,
        )

        handlers = [
            (r"/", handler.topic.IndexHandler),
            (r"/t/(\d+)", handler.topic.ViewHandler),
            (r"/t/create/(.*)", handler.topic.CreateHandler),
            (r"/t/edit/(.*)", handler.topic.EditHandler),
            (r"/reply/edit/(.*)", handler.topic.ReplyEditHandler),
            (r"/node/(.*)", handler.topic.NodeTopicsHandler),
            (r"/college/(.*)", handler.topic.CollegeTopicsHandler),
            (r"/u/(.*)/topics", handler.topic.UserTopicsHandler),
            (r"/u/(.*)/replies", handler.topic.UserRepliesHandler),
            (r"/u/(.*)/favorites", handler.topic.UserFavoritesHandler),
            (r"/u/(.*)", handler.topic.ProfileHandler),
            (r"/vote", handler.topic.VoteHandler),
            (r"/favorite", handler.topic.FavoriteHandler),
            (r"/notifications", handler.notification.ListHandler),
            (r"/members", handler.topic.MembersHandler),
            (r"/nodes", handler.topic.NodesHandler),
            (r"/colleges", handler.topic.CollegesHandler),
            (r"/setting", handler.user.SettingHandler),
            (r"/setting/avatar", handler.user.SettingAvatarHandler),
            (r"/setting/avatar/gravatar", handler.user.SettingAvatarFromGravatarHandler),
            (r"/setting/password", handler.user.SettingPasswordHandler),
            (r"/forgot", handler.user.ForgotPasswordHandler),
            (r"/login", handler.user.LoginHandler),
            (r"/logout", handler.user.LogoutHandler),
            (r"/register", handler.user.RegisterHandler),
            (r"/register/college", handler.user.RegisterCollegeHandler),
            (r"/register/college/(.*)", handler.user.SetCollegeHandler),
            (r"/s/college/(.*)", handler.topic.CollegesHandler),
            (r"/s/node/(.*)", handler.topic.NodesHandler),
            (r"/f/node/(.*)", handler.topic.FollowNodeHandler),
            (r"/f/user/(.*)", handler.topic.FollowUserHandler),
            (r"/m/(.*)", handler.message.CreateMessageHandler),
            (r"/messages", handler.message.MessagesHandler),
            (r"/about", handler.page.AboutHandler),
            (r"/license", handler.page.AboutHandler),
            (r"/feedback", handler.page.AboutHandler),
            (r"/guide", handler.page.AboutHandler),

            (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path = settings["static_path"])),
            (r"/(sitemap.*$)", tornado.web.StaticFileHandler, dict(path = settings["static_path"])),
            (r"/(bdsitemap\.txt)", tornado.web.StaticFileHandler, dict(path = settings["static_path"])),
            (r"/(orca\.txt)", tornado.web.StaticFileHandler, dict(path = settings["static_path"])),
            (r"/(.*)", handler.topic.ProfileHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host = options.mysql_host, database = options.mysql_database,
            user = options.mysql_user, password = options.mysql_password
        )

        # Have one global loader for loading models and handles
        self.loader = Loader(self.db)

        # Have one global model for db query
        self.user_model = self.loader.use("user.model")
        self.topic_model = self.loader.use("topic.model")
        self.reply_model = self.loader.use("reply.model")
        self.plane_model = self.loader.use("plane.model")
        self.node_model = self.loader.use("node.model")
        self.college_model = self.loader.use("college.model")
        self.province_model = self.loader.use("province.model")
        self.notification_model = self.loader.use("notification.model")
        self.vote_model = self.loader.use("vote.model")
        self.favorite_model = self.loader.use("favorite.model")
        self.interest_model = self.loader.use("interest.model")
        self.follow_model = self.loader.use("follow.model")
        self.message_model = self.loader.use("message.model")

        # Have one global session controller
        self.session_manager = SessionManager(settings["cookie_secret"], ["127.0.0.1:11211"], 0)

        # Have one global memcache controller
        self.mc = memcache.Client(["127.0.0.1:11211"])

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

