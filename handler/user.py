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
import urllib
import tornado.web
import lib.jsonp

from base import *
from lib.sendmail import send
from lib.variables import gen_random
from lib.gravatar import Gravatar
from form.user import *

def do_login(self, user_id):
    user_info = self.user_model.get_user_by_uid(user_id)
    user_id = user_info["uid"]
    self.session["uid"] = user_id
    self.session["username"] = user_info["username"]
    self.session["email"] = user_info["email"]
    self.session["password"] = user_info["password"]
    self.session.save()
    self.set_secure_cookie("user", str(user_id))

def do_logout(self):
    # destroy sessions
    self.session["uid"] = None
    self.session["username"] = None
    self.session["email"] = None
    self.session["password"] = None
    self.session.save()

    # destroy cookies
    self.clear_cookie("user")

class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_email = self.current_user['email']
        self.write(user_email)

class SettingHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, template_variables = {}):
        user_info = self.get_current_user()
        template_variables["user_info"] = user_info
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/setting.html", **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = SettingForm(self)

        if not form.validate():
            self.get({"errors": form.errors})
            return

        # continue while validate succeed

        user_info = self.current_user
        update_result = self.user_model.set_user_base_info_by_uid(user_info["uid"], {
            "nickname": form.nickname.data,
            "signature": form.signature.data,
            "location": form.location.data,
            "website": form.website.data,
            "company": form.company.data,
            "github": form.github.data,
            "twitter": form.twitter.data,
            "douban": form.douban.data,
            "self_intro": form.self_intro.data,
        })

        template_variables["success_message"] = [u"用户基本资料更新成功"]
        # update `updated`
        updated = self.user_model.set_user_base_info_by_uid(user_info["uid"], {"updated": time.strftime('%Y-%m-%d %H:%M:%S')})
        self.get(template_variables)

class SettingAvatarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, template_variables = {}):
        user_info = self.get_current_user()
        template_variables["user_info"] = user_info
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/setting_avatar.html", **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables = {}):
        template_variables = {}

        if(not "avatar" in self.request.files):
            template_variables["errors"] = {}
            template_variables["errors"]["invalid_avatar"] = [u"请先选择要上传的头像"]
            self.get(template_variables)
            return

        user_info = self.current_user
        user_id = user_info["uid"]
        avatar_name = "%s" % uuid.uuid5(uuid.NAMESPACE_DNS, str(user_id))
        avatar_raw = self.request.files["avatar"][0]["body"]
        avatar_buffer = StringIO.StringIO(avatar_raw)
        avatar = Image.open(avatar_buffer)

        # crop avatar if it's not square
        avatar_w, avatar_h = avatar.size
        avatar_border = avatar_w if avatar_w < avatar_h else avatar_h
        avatar_crop_region = (0, 0, avatar_border, avatar_border)
        avatar = avatar.crop(avatar_crop_region)

        avatar_96x96 = avatar.resize((96, 96), Image.ANTIALIAS)
        avatar_48x48 = avatar.resize((48, 48), Image.ANTIALIAS)
        avatar_32x32 = avatar.resize((32, 32), Image.ANTIALIAS)
        avatar_96x96.save("/srv/www/3n1b.com/static/avatar/b_%s.png" % avatar_name, "PNG")
        avatar_48x48.save("/srv/www/3n1b.com/static/avatar/m_%s.png" % avatar_name, "PNG")
        avatar_32x32.save("/srv/www/3n1b.com/static/avatar/s_%s.png" % avatar_name, "PNG")
        result = self.user_model.set_user_avatar_by_uid(user_id, "%s.png" % avatar_name)
        template_variables["success_message"] = [u"用户头像更新成功"]
        # update `updated`
        updated = self.user_model.set_user_base_info_by_uid(user_id, {"updated": time.strftime('%Y-%m-%d %H:%M:%S')})
        self.get(template_variables)

class SettingAvatarFromGravatarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, template_variables = {}):
        user_info = self.current_user
        user_id = user_info["uid"]
        avatar_name = "%s" % uuid.uuid5(uuid.NAMESPACE_DNS, str(user_id))
        gravatar = Gravatar(user_info["email"])
        avatar_96x96 = gravatar.get_image(size = 96, filetype_extension = False)
        avatar_48x48 = gravatar.get_image(size = 48, filetype_extension = False)
        avatar_32x32 = gravatar.get_image(size = 32, filetype_extension = False)
        urllib.urlretrieve(avatar_96x96, "/srv/www/3n1b.com/static/avatar/b_%s.png" % avatar_name)
        urllib.urlretrieve(avatar_48x48, "/srv/www/3n1b.com/static/avatar/m_%s.png" % avatar_name)
        urllib.urlretrieve(avatar_32x32, "/srv/www/3n1b.com/static/avatar/s_%s.png" % avatar_name)
        result = self.user_model.set_user_avatar_by_uid(user_id, "%s.png" % avatar_name)
        template_variables["success_message"] = [u"用户头像更新成功"]
        # update `updated`
        updated = self.user_model.set_user_base_info_by_uid(user_id, {"updated": time.strftime('%Y-%m-%d %H:%M:%S')})
        template_variables["user_info"] = user_info
        template_variables["gen_random"] = gen_random
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/setting_avatar.html", **template_variables)

class SettingPasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, template_variables = {}):
        user_info = self.get_current_user()
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/setting_password.html", **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = SettingPasswordForm(self)

        if not form.validate():
            self.get({"errors": form.errors})
            return

        # validate the password

        user_info = self.current_user
        user_id = user_info["uid"]
        secure_password = hashlib.sha1(form.password_old.data).hexdigest()
        secure_new_password = hashlib.sha1(form.password.data).hexdigest()

        if(not user_info["password"] == secure_password):
            template_variables["errors"] = {}
            template_variables["errors"]["error_password"] = [u"当前密码输入有误"]
            self.get(template_variables)
            return

        # continue while validate succeed

        update_result = self.user_model.set_user_password_by_uid(user_id, secure_new_password)
        template_variables["success_message"] = [u"您的用户密码已更新"]
        # update `updated`
        updated = self.user_model.set_user_base_info_by_uid(user_id, {"updated": time.strftime('%Y-%m-%d %H:%M:%S')})
        self.get(template_variables)

class ForgotPasswordHandler(BaseHandler):
    def get(self, template_variables = {}):
        do_logout(self)
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/forgot_password.html", **template_variables)

    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = ForgotPasswordForm(self)

        if not form.validate():
            self.get({"errors": form.errors})
            return


        # validate the post value

        user_info = self.user_model.get_user_by_email_and_username(form.email.data, form.username.data)

        if(not user_info):
            template_variables["errors"] = {}
            template_variables["errors"]["invalid_email_or_username"] = [u"所填用户名和邮箱有误"]
            self.get(template_variables)
            return

        # continue while validate succeed
        # update password

        new_password = uuid.uuid1().hex
        new_secure_password = hashlib.sha1(new_password).hexdigest()
        update_result = self.user_model.set_user_password_by_uid(user_info["uid"], new_secure_password)

        # send password reset link to user

        mail_title = u"叁年壹班（3n1b.com）找回密码"
        template_variables = {"email": form.email.data, "new_password": new_password};
        template_variables["success_message"] = [u"新密码已发送至您的注册邮箱"]
        mail_content = self.render_string("user/forgot_password_mail.html", **template_variables)
        send(mail_title, mail_content, form.email.data)

        self.get(template_variables)

class LoginHandler(BaseHandler):
    def get(self, template_variables = {}):
        do_logout(self)
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/login.html", **template_variables)

    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = LoginForm(self)

        if not form.validate():
            self.get({"errors": form.errors})
            return

        # continue while validate succeed
        
        secure_password = hashlib.sha1(form.password.data).hexdigest()
        secure_password_md5 = hashlib.md5(form.password.data).hexdigest()
        user_info = self.user_model.get_user_by_email_and_password(form.email.data, secure_password)
        user_info = user_info or self.user_model.get_user_by_email_and_password(form.email.data, secure_password_md5)
        
        if(user_info):
            do_login(self, user_info["uid"])
            # update `last_login`
            updated = self.user_model.set_user_base_info_by_uid(user_info["uid"], {"last_login": time.strftime('%Y-%m-%d %H:%M:%S')})
            user_college = self.college_model.get_college_by_college_name(user_info["collegename"])
            redirect_path = self.get_argument("next", "/")
            print redirect_path
            redirect_path = redirect_path.replace('1001', str(user_college.id))
            print redirect_path
            self.redirect(redirect_path)
            return

        template_variables["errors"] = {"invalid_email_or_password": [u"邮箱或者密码不正确"]}
        self.get(template_variables)

class LogoutHandler(BaseHandler):
    def get(self):
        do_logout(self)
        # redirect
        self.redirect(self.get_argument("next", "/"))

class RegisterHandler(BaseHandler):
    def get(self, template_variables = {}):
        do_logout(self)
        template_variables["wallpaper"] = self.get_wallpaper()
        self.render("user/register.html", **template_variables)

    def post(self, template_variables = {}):
        template_variables = {}

        # validate the fields

        form = RegisterForm(self)

        if not form.validate():
            self.get({"errors": form.errors})
            return

        # validate duplicated

        duplicated_email = self.user_model.get_user_by_email(form.email.data)
        duplicated_username = self.user_model.get_user_by_username(form.username.data)
        #duplicated_collegename = self.college_model.get_college_by_college_name(form.collegename.data)

        if(duplicated_email or duplicated_username):
            template_variables["errors"] = {}

            if(duplicated_email):
                template_variables["errors"]["duplicated_email"] = [u"所填邮箱已经被注册过"]

            if(duplicated_username):
                template_variables["errors"]["duplicated_username"] = [u"所填用户名已经被注册过"]

            self.get(template_variables)
            return

        # validate reserved

        if(form.username.data in self.settings.get("reserved")):
            template_variables["errors"] = {}
            template_variables["errors"]["reserved_username"] = [u"用户名被保留不可用"]
            self.get(template_variables)
            return

        # validate college name
        #if duplicated_collegename is None:
         #   template_variables["errors"] = {}
          #  template_variables["errors"]["duplicated_collegename"] = [u"学校名称不正确（进入所有学校页面 3n1b.com/colleges 核对你想输入的学校名称）"]
           # self.get(template_variables)
           # return

        # continue while validate succeed

        secure_password = hashlib.sha1(form.password.data).hexdigest()

        user_info = {
            "email": form.email.data,
            "password": secure_password,
            "username": form.username.data,
            "collegename": "请设置您的学校",
            "created": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        if(self.current_user):
            return
        
        user_id = self.user_model.add_new_user(user_info)
        
        if(user_id):
            do_login(self, user_id)

            # send register success mail to user

            mail_title = u"叁年壹班 注册成功通知"
            mail_content = self.render_string("user/register_mail.html")
            send(mail_title, mail_content, form.email.data)

        self.redirect(self.get_argument("next", "/register/college"))

class RegisterCollegeHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        if(user_info):
            template_variables["user_info"]["counter"] = {
                "topics": self.topic_model.get_user_all_topics_count(user_info["uid"]),
                "replies": self.reply_model.get_user_all_replies_count(user_info["uid"]),
                "notifications": self.notification_model.get_user_unread_notification_count(user_info["uid"]),
                "favorites": self.favorite_model.get_user_favorite_count(user_info["uid"]),
            }
        template_variables["status_counter"] = {
            "users": self.user_model.get_all_users_count(),
            "nodes": self.node_model.get_all_nodes_count(),
            "topics": self.topic_model.get_all_topics_count(),
            "replies": self.reply_model.get_all_replies_count(),
        }
        college_prefix = "/register/college/?c="
        template_variables["college_prefix"] = college_prefix 
        template_variables["provinces"] = self.province_model.get_all_provinces_with_colleges()
        template_variables["hot_nodes"] = self.node_model.get_all_hot_nodes()        
        template_variables["gen_random"] = gen_random       
        template_variables["active_page"] = "colleges" 
        template_variables["wallpaper"] = self.get_wallpaper() 
        self.render("user/registercollege.html", **template_variables)

class SetCollegeHandler(BaseHandler):
    def get(self, college = None, template_variables = {}):
        user_info = self.current_user
        template_variables["user_info"] = user_info
        college_id = self.get_argument('c', "0")
        college = self.college_model.get_college_by_college_id(college_id)
        collegename = college["name"]
        print collegename
        update_result = self.user_model.set_user_collegename_by_uid(user_info["uid"], collegename)
        self.redirect(self.get_argument("next", "/"))