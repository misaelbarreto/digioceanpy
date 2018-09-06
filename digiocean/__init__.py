# -*- coding: utf-8 -*-
from __future__ import with_statement

from .endpoints.domains import DomainEndpoint
from .endpoints.ssh_keys import SshKeyEndpoint
from .endpoints.droplets import DropletEndpoint


class DigiOcean:
    def __init__(self, token):
        self.domains = DomainEndpoint(token=token, endpoint_url='domains/')
        self.ssh_keys = SshKeyEndpoint(token=token, endpoint_url='account/keys/')
        self.droplets = DropletEndpoint(token=token, endpoint_url='droplets/')

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