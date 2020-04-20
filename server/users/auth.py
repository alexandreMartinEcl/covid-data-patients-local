"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from requests import post

from server import settings
from server.settings import AUTH_SERVER_URL, AUTH_SERVER_TOKEN


class IDServer:
    headers = {'Key-auth': AUTH_SERVER_TOKEN}

    @classmethod
    def check_ids(cls, username, password):
        # reponse.json() must return dict(username, email, firstname, lastname)
        if settings.SERVER_VERSION.lower() == "dev":
            return dict(
                username= "user1",
                email="eeek@gk.com",
                firstname="yes",
                lastname="no"
            )

        resp = post("{}/user/authenticate".format(AUTH_SERVER_URL),
                    data={"username": username, "password": password},
                    headers=cls.headers)
        if resp.status_code != 200:
            raise ValueError("Invalid username or password")

        tokens = resp.json()
        attributes = tokens["data"]["attributes"]
        user_info = dict(
            username=attributes["sAMAccountName"],
            email=attributes["mail"],
            firstname=attributes["givenName"],
            lastname=attributes["sn"],
        )
        return user_info
