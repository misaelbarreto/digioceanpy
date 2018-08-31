# -*- coding: utf-8 -*-
from __future__ import with_statement

class DigiOceanModel(object):

    # def __init__(self, *args, **kwargs):
    #     super(DigiOceanModel, self).__init__(*args, **kwargs)

    @classmethod
    def load(cls, data):
        if isinstance(data, list):
            objs = list()
            for d in data:
                objs.append(cls(**d))
            return objs
        else:
            obj = cls(**data)
            return obj

    def __repr__(self):
        if self.__dict__:
            atts = u', '.join([u'='.join([key, str(val)]) for key, val in self.__dict__.items()])
            return '{} ({})'.format(self.__class__.__name__, atts)
        return ''