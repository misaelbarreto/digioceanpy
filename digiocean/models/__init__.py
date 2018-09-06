# -*- coding: utf-8 -*-
from __future__ import with_statement

class DigiOceanModel:

    # def __init__(self, *args, **kwargs):
    #     super(DigiOceanModel, self).__init__()

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
        return u''


class Domain(DigiOceanModel):
    def __init__(self, name=None, ttl=None, zone_file=None, *args, **kwargs):
        self.name = name
        self.ttl = ttl
        self.zone_file = zone_file
        # super(Domain, self).__init__(*args, **kwargs)


class SshKey(DigiOceanModel):
    def __init__(self, id=None, fingerprint=None, public_key=None, name=None, *args, **kwargs):
        self.id = id
        self.fingerprint = fingerprint
        self.public_key = public_key
        self.name = name
        # super(SshKey, self).__init__(*args, **kwargs)

