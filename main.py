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
import json

from google.appengine.ext import db
from google.appengine.api import users

class Producer(db.Model):
    """Models a producer (e.g. farmer) with a name and produce"""
    name = db.StringProperty()
    produce = db.StringListProperty()

class ProducerHandler(webapp2.RequestHandler):
    def post(self): # create
        if (self.request.content_type == 'application/json'):
            producer_dict = json.loads(self.request.body)
            producer = Producer()
            producer.name = producer_dict['name']
            producer.produce = producer_dict['produce']
            key = producer.put()
            self.response.content_type = 'application/json'
            self.response.body = json.dumps({'id': key.id()})
    def get(self, producer_id): # read
        producer = Producer.get_by_id(int(producer_id))
        if producer is None:
            pass # TODO handle error
        self.response.content_type = 'application/json'
        self.response.body = json.dumps(db.to_dict(producer))
    # def put(self): # update
    def delete(self, producer_id):
        producer = Producer.get_by_id(int(producer_id))
        if producer is None:
            pass # TODO error
        producer.delete()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Goodbye ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/producer', ProducerHandler),
    ('/producer/(\d+)', ProducerHandler)
], debug=True)
