# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin


class User(UserMixin):
    id_ = 'm0ng0h4sh'
    
    def get_id(self):
        return unicode(self.id_)
