__author__ = 'Rob'


class Symbol(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name