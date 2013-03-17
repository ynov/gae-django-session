import json
import random

from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache
mcache = memcache.Client()

SYMBOLS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()'
def generate_sessid():
    return ''.join([SYMBOLS[random.randrange(0, len(SYMBOLS))] for i in range(64)])

class SessionDb(db.Model):
    stored_kv = db.TextProperty()
    modification_time = db.DateTimeProperty(auto_now=True)

    @staticmethod
    def load_session(sessid):
        parent_key = db.Key.from_path('SESSION_ID', sessid)

        q = SessionDb.all()
        q.ancestor(parent_key)
        sessdb = q.get()

        return sessdb

    @staticmethod
    def create_session(sessid):
        parent_key = db.Key.from_path('SESSION_ID', sessid)
        sessdb = SessionDb.load_session(sessid)

        if sessdb == None:
            sessdb = SessionDb(parent=parent_key)
            sessdb.set_kv({})
            sessdb.put()

        return sessdb

    def set_kv(self, kv):
        self.stored_kv = json.dumps(kv)

    def get_kv(self):
        return json.loads(self.stored_kv)

class Session:
    def __init__(self, request):        
        self.request = request
        try:
            self.sessid = self.request.COOKIES['SESSION_ID']
        except KeyError:
            self.sessid = generate_sessid()

        self.cookie_cleared = False

        if self.get_all() == None:
            self.cookie_cleared = True
            return

        tmp_access = self.get('tmp_access')
        if tmp_access == None:
            tmp_access = str(datetime.now()).split('.')[0]
            self.set('tmp_access', tmp_access)
        elif (datetime.strptime(tmp_access, '%Y-%m-%d %H:%M:%S') <= datetime.now() - timedelta(days=1)):
            tmp_access = str(datetime.now()).split('.')[0]
            self.set('tmp_access', tmp_access)

    def set(self, key, val):
        sessdb = SessionDb.load_session(self.sessid) or \
            SessionDb.create_session(self.sessid)

        stored_kv = sessdb.get_kv()
        stored_kv[key] = val

        sessdb.set_kv(stored_kv)
        sessdb.put()
        mcache.set(key=self.sessid, value=stored_kv)
        self.cookie_cleared = False

    def get(self, key):
        try:
            stored_kv = mcache.get(self.sessid)

            if stored_kv == None:
                sessdb = SessionDb.load_session(self.sessid)
                if sessdb == None:
                    return None
                else:
                    stored_kv = sessdb.get_kv()
                    mcache.set(self.sessid, stored_kv)

            value = stored_kv[key]
            return value
        except:
            return None

    def get_all(self):
        kv = mcache.get(self.sessid)
        if kv == None:
            sessdb = SessionDb.load_session(self.sessid)
            if sessdb:
                kv = sessdb.get_kv()

        return kv

    def delete(self, key):
        sessdb = SessionDb.load_session(self.sessid)
        stored_kv = sessdb.get_kv()

        if stored_kv != None:
            try:
                stored_kv.pop(key)

                sessdb.set_kv(stored_kv)
                sessdb.put()
                mcache.set(self.sessid, stored_kv)
            except:
                pass

    def clear(self):
        sessdb = SessionDb.load_session(self.sessid)
        if sessdb:
            sessdb.delete()

        mcache.delete(self.sessid)
        self.cookie_cleared = True

class SessionMiddleware:
    def process_request(self, request):
        request.session = Session(request)

    def process_response(self, request, response):
        try:
            if not request.session.cookie_cleared:
                response.set_cookie(key='SESSION_ID', value=request.session.sessid,
                                    expires=datetime.now() + timedelta(days=7))
            else:
                response.delete_cookie(key='SESSION_ID')
        except AttributeError:
            pass

        return response
