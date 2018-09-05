# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
from digiocean.endpoints import DigiOceanEndPoint, DigiOceanResponse


class Droplet(DigiOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(Droplet, self).__init__(*args, **kwargs)

    def list(self):
        '''
        To retrieve a list of all droplets in your account.

        Based in DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#list-all-droplets

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digiocean.com/v2/droplets?page=1&per_page=1"

        :return: a DigitalOceanResponse.
        '''
        logging.info('Retrieving all droplets...')
        # command = DigitalOceanCommand(token=self.token, url_complement='droplets/')
        command = self.commander.create_command()
        return command.execute(command=command, msgInfo='Droplets found (total: {total}).', msgWarn='No droplets found.')

    def get(self, id):
        logging.info('Find the Droplet with id {0}...'.format(id))
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='droplets/' + str(id))
        command = self.commander.create_command(endpoint_url_complement=str(id))
        return command.execute(command=command, msgInfo='Droplet found.', msgWarn='No droplet found.')

    def extra_get_by_name(self, name):
        response = DigiOceanResponse(digi_ocean_command=None,
                                     http_status=None,
                                     is_ok=False,
                                     header=None,
                                     data={'id': 'droplet_not_found',
                                              'message': 'There is no droplet with this name.'})

        logging.info('Find Droplet with the name "{0}"...'.format(name))
        all_droplets = self.list()
        if all_droplets.is_ok:
            for droplet in all_droplets.data['droplets']:
                if droplet['name'] == name:
                    response = DigiOceanResponse(digi_ocean_command=None,
                                                 http_status=None,
                                                 is_ok=True,
                                                 header=None,
                                                 data={'droplet': droplet})

                    break

        if response.is_ok:
            logging.info('One of the droplets found is called "{0}".'.format(name))
        else:
            logging.warn('None of the droplets found is called "{0}".'.format(name))

        return response

    def create(self,
               name,
               region='nyc3',
               size='512mb',
               image='debian-8-x64',
               ssh_keys=None,
               backups=False,
               ipv6=True,
               user_data=None,
               private_networking=None,
               volumes=None,
               tags=None):
        '''
        Create a new Droplet.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#create-a-new-droplet

        Example:
        curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" -d '{"name":"examples.com","region":"nyc3","size":"512mb","image":"ubuntu-14-04-x64","ssh_keys":null,"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["web"]}' "https://api.digiocean.com/v2/droplets"

        To see details params, view DigitalOcean API Documentation.
        :return: a DigitalOceanResponse.
        '''
        logging.info('Creating droplet "{0}"...'.format(name))

        if isinstance(ssh_keys, DigiOceanResponse):
            logging.debug('Obtain the ssh key id from a DigitalOceanResponse...')
            ssh_keys = ssh_keys.extract_value_from_data('ssh_key.id')
            if not isinstance(ssh_keys, list):
                ssh_keys = [ssh_keys]
            logging.debug('Ssh key id obtained with success. IDs: {0}'.format(ssh_keys))


        params = {'name': name,
                  'region': region,
                  'size': size,
                  'image': image,
                  'ssh_keys': ssh_keys,
                  'backups': backups,
                  'ipv6': ipv6,
                  'user_data': user_data,
                  'private_networking': private_networking,
                  'volumes': volumes,
                  'tags': tags}
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='droplets/',
        #                               params=params,
        #                               http_method='POST')
        command = self.commander.create_command(params=params,
                                                http_method='POST')
        return command.execute(command=command,
                                                msgInfo='Droplet created with success.',
                                                msgError='Error on create droplet.')