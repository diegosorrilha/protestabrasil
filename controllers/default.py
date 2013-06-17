# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    return dict()


@service.json
def load_tweets():
    if request.vars.current_id:
        from twython import Twython, TwythonError
        from tokens import tokens
        from datetime import datetime

        twitter = tokens("twitter")
        APP_KEY = twitter["APP_KEY"]
        APP_SECRET = twitter["APP_SECRET"]
        OAUTH_TOKEN = twitter["OAUTH_TOKEN"]
        OAUTH_TOKEN_SECRET = twitter["OAUTH_TOKEN_SECRET"]

        # Requires Authentication as of Twitter API v1.1
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        search = 'protestabrasil'

        try:
            if request.vars.current_id == "0":
                search_results = twitter.search(q=search, count=10)
            else:
                current_id = int(request.vars.current_id,10)
                # Margin to correct. Sometimes strangely repeated the last result
                current_id -= 100
                search_results = twitter.search(q=search, count=5, max_id=current_id)
        except TwythonError as e:
            print e

        updates = []
        post = {}

        for tweet in search_results['statuses']:
            post["avatar"] = tweet['user']['profile_image_url']
            post["user"] = '%s @%s' % (tweet['user']['name'].encode('utf-8'), tweet['user']['screen_name'].encode('utf-8'))
            date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            post["created_at"] = prettydate(date,T)
            post["text"] = tweet['text'].encode('utf-8')
            post["location"] = tweet['user']['location'].encode('utf-8')
            post["id_str"] = tweet["id_str"]
            updates.append(post.copy())

    return updates


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
