# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
from digiocean.endpoints import DigiOceanEndPoint, DigiOceanResponse
from digiocean.models import SshKey



class SshKeyEndpoint(DigiOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(SshKeyEndpoint, self).__init__(*args, **kwargs)

    def list(self):
        '''
        To list all of the keys in your account

        Based in DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#list-all-keys

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digiocean.com/v2/account/keys"

        :return: a DigitalOceanResponse.
        '''
        logging.info('Listing all SSH Keys...')
        command = self.commander.create_command()
        response = command.execute(parser=SshKey,
                                   data_field_to_parser='ssh_keys',
                                   msgInfo='SSH Keys found (total: {total}).',
                                   msgWarn='No SSH Keys found.')

        return response

    def get(self, id_or_fingerprint):
        '''
        To show information about a key.

        Based in DigitalOcean API:
        https://developers.digitalocean.com/documentation/v2/#retrieve-an-existing-key

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/account/keys/512190"

        :param id_or_fingerprint:
        :return: a DigitalOceanResponse.
        '''

        logging.info(u'Find the SSH Keys {}...'.format(id_or_fingerprint))
        command = self.commander.create_command(endpoint_url_complement=str(id_or_fingerprint))
        response = command.execute(parser=SshKey,
                                   data_field_to_parser='ssh_keys',
                                   msgInfo='SSH Key found.',
                                   msgWarn='No SSH Key found.')

        return response


    def extra_get_by_public_key(self, public_key):
        '''
        To show information about a key based on the public key. Obs: This method is exclusive of the DigiOcean python wrapper.

        :param public_key
        :return: a DigitalOceanResponse.
        '''
        response = DigiOceanResponse(digi_ocean_command=None,
                                     http_status=None,
                                     is_ok=False,
                                     header=None,
                                     data={'id': 'key_not_found',
                                              'message': 'There is no ssh key with this signature.'})

        public_key_first_letters = public_key[:30]
        logging.info('Find SSH Keys using the public key "{}..."'.format(public_key_first_letters))
        all_ssh_keys = self.list()
        if all_ssh_keys.is_ok:
            for key in all_ssh_keys.data['ssh_keys']:
                if key['public_key'] == public_key:
                    response = DigiOceanResponse(digi_ocean_command=None,
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
        '''
        To add a new SSH public key to your DigitalOcean account.

        Based in DigitalOcean API:
        https://developers.digitalocean.com/documentation/v2/#create-a-new-key

        Example:
        curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" -d '{"name":"My SSH Public Key","public_key":"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQDDHr/jh2Jy4yALcK4JyWbVkPRaWmhck3IgCoeOO3z1e2dBowLh64QAM+Qb72pxekALga2oi4GvT+TlWNhzPH4V example"}' "https://api.digitalocean.com/v2/account/keys"

        :param name:
        :param public_key:
        :return: a DigitalOceanResponse.
        '''

        logging.info('Create the SSH Keys "{}"...'.format(name))
        params = {'name': name, 'public_key': public_key}
        command = self.commander.create_command(params=params,
                                                http_method='POST')
        response = command.execute(parser=SshKey,
                                   data_field_to_parser='ssh_key',
                                   msgInfo='SSH Key created with success.',
                                   msgError='Error on create ssh key.')
        return response

    def delete(self, id_or_fingerprint):
        '''
        To destroy a public SSH key that you have in your account.

        Based in DigitalOcean API:
        https://developers.digitalocean.com/documentation/v2/#destroy-a-key

        Example:
        curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/account/keys/512190"


        :param id_or_fingerprint:
        :return: a DigitalOceanResponse.
        '''
        command = self.commander.create_command(endpoint_url_complement=id_or_fingerprint,
                                                http_method='DELETE')
        response = command.execute(msgInfo='SSH Key deleted with success.',
                                   msgError='Error on delete ssh key.')
        return response
