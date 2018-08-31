# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
from digitalocean.api import DigiOceanEndPoint, DigiOceanCommand, DigiOceanResponse


class SshKey(DigiOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(SshKey, self).__init__(*args, **kwargs)

    def list(self):
        '''
        To list all of the keys in your account

        Based in DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#list-all-keys

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/account/keys"

        :return: a DigitalOceanResponse.
        '''
        logging.info('Listing all SSH Keys...')
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='account/keys/')
        command = self.commander.create_command()
        return self.execute(command=command,
                                                msgInfo='SSH Keys found (total: {total}).',
                                                msgWarn='No SSH Keys found.')

    def get(self, id_or_fingerprint):
        logging.info('Find the SSH Keys {0}...'.format(id_or_fingerprint))
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='account/keys/' + str(id_or_fingerprint))
        command = self.commander.create_command(endpoint_url_complement=str(id_or_fingerprint))
        return self.execute(command=command,
                                                msgInfo='SSH Key found.',
                                                msgWarn='No SSH Key found.')

    def extra_get_by_public_key(self, public_key):
        response = DigiOceanResponse(digital_ocean_command=None,
                                     http_status=None,
                                     is_ok=False,
                                     header=None,
                                     data={'id': 'key_not_found',
                                              'message': 'There is no ssh key with this signature.'})

        public_key_first_letters = public_key[:30]
        logging.info('Find SSH Keys using the public key "{0}..."'.format(public_key_first_letters))
        all_ssh_keys = self.list()
        if all_ssh_keys.is_ok:
            for key in all_ssh_keys.data['ssh_keys']:
                if key['public_key'] == public_key:
                    response = DigiOceanResponse(digital_ocean_command=None,
                                                 http_status=None,
                                                 is_ok=True,
                                                 header=None,
                                                 data={'ssh_key': key})

                    break

        if response.is_ok:
            logging.info('One of the ssh keys found has the signature "{0}".'.format(public_key_first_letters))
        else:
            logging.warn('None of the ssh keys has the signature "{0}".'.format(public_key_first_letters))

        return response

    def create(self, name, public_key):
        logging.info('Create the SSH Keys "{0}"...'.format(name))
        params = {'name': name, 'public_key': public_key}
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='account/keys/',
        #                               params=params,
        #                               http_method='POST')
        command = self.commander.create_command(params=params,
                                                http_method='POST')
        return self.execute(command=command,
                                                msgInfo='SSH Key created with success.',
                                                msgError='Error on create ssh key.')

    def delete(self, id_or_fingerprint):
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='account/keys/' + str(id_or_fingerprint),
        #                               http_method='DELETE')
        command = self.commander.create_command(endpoint_url_complement=(id_or_fingerprint),
                                                http_method='DELETE')
        return self.execute(command=command,
                                                msgInfo='SSH Key deleted with success.',
                                                msgError='Error on delete ssh key.')
