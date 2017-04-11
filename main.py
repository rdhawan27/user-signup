#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re


page_header="""<!DOCTYPE html>
<html>
<head>
    <title>SigUp</title>
    <style type="text/css">
        .error{color:red;}
    </style>
</head>
<body>
    <h1>
        <a href="/">SignUp</a>
    </h1>
"""
def verify(password,verifypassword):
    len_password=len(password)
    len_verifypassword=len(verifypassword)

    if len_password!=len_verifypassword:
        return False
    else:
        for i in range (len_password):
            if password[i]!= verifypassword[i]:
                return False
        return True



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE= re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE= re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

Usersignup_form="""<form method="post">
    <h1><a href="/">SignUp</a></h1>
    <label>Username: <input type="text" name="uname" value=%(username)s></label><span class="error" style="color:red"> %(error_username)s</span><br><br>
    <label>Password: <input type="password" name="upass"/></label><span class="error" style="color:red">%(error_password)s</span><br><br>
    <label>VerifyPassword: <input type="password" name="vpass"/></label><span class="error" style="color:red">%(error_verifypassword)s</span><br><br>
    <label>Valid Email: <input type="email" name="email" /></label><span class="error" style="color:red">%(error_email)s</span><br><br>
    <input type="submit"/>
    </form>"""



class MainHandler(webapp2.RequestHandler):

    def writeform(self,Get_Username="",error_username="",error_password="",error_verifypassword="",error_email=""):
        self.response.write(Usersignup_form % {'username': Get_Username,
                                                'error_username':error_username,
                                                'error_password':error_password,
                                                'error_verifypassword':error_verifypassword,
                                                'error_email':error_email
                                                })

    def get(self):
        self.writeform()

    def post(self,Get_Username="",error_username="",error_password="",error_verifypassword="",error_email=""):
        have_error=False
        Username=valid_username(self.request.get("uname"))
        Password=valid_password(self.request.get("upass"))
        Email=valid_email(self.request.get("email"))

        Get_password=self.request.get("upass")
        Get_verify_password=self.request.get("vpass")
        Get_Username=self.request.get("uname")
        Get_email=self.request.get("email")
        Len_email=len(Get_email)


        if not Username:
            error_username="This is not a valid username"
            have_error=True
        if not Password:
            error_password="This is not a valid password"
            have_error=True
        if Get_password != Get_verify_password:
            error_verifypassword="Password do not match"
            have_error=True
        if not Email:
            error_email = "That is not a valid email"

        if have_error:
            self.writeform(Get_Username,error_username,error_password,error_verifypassword)

        else:
            self.redirect("/welcome?uname=" + Get_Username)
            #self.response.write("%sWelcome to HTML"% (Get_Username))

class Welcome(MainHandler):

    def get(self):
        username=self.request.get("uname")
        self.response.write("%s Welcome to HTML"% (
    username))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
