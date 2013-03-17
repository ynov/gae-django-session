from google.appengine.ext import db
from google.appengine.api import memcache
mcache = memcache.Client()

class Task(db.Model):
    name = db.StringProperty()
    message = db.StringProperty()
    deadline = db.DateTimeProperty()

    def cache_and_put(self):
        mcache.set(key=self.name, value=self)
        self.put()

    @staticmethod
    def get_by_name(name):
        if mcache.get(key=name) == None:
            t = Task.all()
            t.filter('name =', name)

            task = t.get()

            mcache.set(key=name, value=task)
            return task

        else:
            print "From cache get!"
            return mcache.get(key=name)