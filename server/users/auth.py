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
            username=attributes["sAMAAccountName"],
            email=attributes["mail"],
            firstname=attributes["givenName"],
            lastname=attributes["sn"],
        )
        return user_info
