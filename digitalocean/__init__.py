# -*- coding: utf-8 -*-
from __future__ import with_statement

from .endpoints.ssh_keys import SshKey
from .endpoints.domains import Domain
from .endpoints.droplets import Droplet


class DigitalOcean:
    def __init__(self, token):
        self.domains = Domain(token=token, endpoint_url='domains/')
        self.ssh_keys = SshKey(token=token, endpoint_url='account/keys/')
        self.droplets = Droplet(token=token, endpoint_url='droplets/')

    # def check_params(params):
    #     '''
    #
    #     :param params:
    #     :return:
    #     '''
    #     erro = list()
    #     for p in params:
    #         if globals().has_key(p) and globals()[p] is not None and str(globals()[p]) <> '':
    #             yield globals()[p]
    #         else:
    #             erro.append(p)
    #     if erro:
    #         raise Exception('Parâmetros não informados: {0}'.format(', '.join(erro)))

    # def __debug(self, s):
    #     print '\n\n\n\n\n[%s] %s' % (datetime.now(), s)