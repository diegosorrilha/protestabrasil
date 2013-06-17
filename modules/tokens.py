# -*- coding: utf-8 -*-
def tokens(params):
    """Function receives the type of social network variables and then returns to the respective keys.
    """

    if params == "twitter":

        APP_KEY = ""
        APP_SECRET = ""
        OAUTH_TOKEN = ""
        OAUTH_TOKEN_SECRET = ""

        return dict(
            APP_KEY=APP_KEY,
            APP_SECRET=APP_SECRET,
            OAUTH_TOKEN=OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET=OAUTH_TOKEN_SECRET
            )

    return False