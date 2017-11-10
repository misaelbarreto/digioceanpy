# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
from digitalocean.api import DigitalOceanEndPoint, DigitalOceanCommand


class Domain(DigitalOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(Domain, self).__init__(*args, **kwargs)

    def list(self):
        '''
        To retrieve a list of all of the domains in your account,

        Based in DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#list-all-domains

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/domains"

        :return: a DigitalOceanResponse.
        '''
        logging.info('Retrieving all domains...')
        # command = DigitalOceanCommand(token=self.token, url_complement='domains/')
        command = self.commander.create_command()
        return self._execute_command_and_log_it(command=command,
                                                msgInfo='Domains found (total: {total}).',
                                                msgWarn='No domains found.')

    def get(self, domain_name):
        '''
        Retrieve information about a specific domain.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#retrieve-an-existing-domain

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/domains/examples.com"

        :param domain_name: The name of domain. Ex: mydomain.com
        :return: a DigitalOceanResponse
        '''
        logging.info('Retrieving the domain "{0}"...'.format(domain_name))
        # command = DigitalOceanCommand(token=self.token,
        #                              url_complement='domains/{0}'.format(domain_name))
        command = self.commander.create_command(endpoint_url_complement=domain_name)
        return self._execute_command_and_log_it(command=command,
                                                msgInfo='Domain found.',
                                                msgWarn='Domain not found.')

    def create(self, domain_name, ip_address):
        '''
        Create a new domain.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#create-a-new-domain

        Example:
        curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" -d '{"name":"examples.com","ip_address":"1.2.3.4"}' "https://api.digitalocean.com/v2/domains"

        :param domain_name: The name of domain. Ex: app.myname.com
        :param ip_address: This attribute contains the IP address you want the domain to point to.
        :return: a DigitalOceanResponse.
        '''
        logging.info('Creating the domain {0} with ip {1}...'.format(domain_name, ip_address))
        params = {'name': domain_name, 'ip_address': ip_address}
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='domains/',
        #                               params=params,
        #                               http_method='POST')
        command = self.commander.create_command(params=params, http_method='POST')
        return self._execute_command_and_log_it(command=command,
                                                msgInfo='Domain created with success.',
                                                msgError='Error on create domain.')

    def delete(self, name):
        logging.info('Deleting the domain "{0}"...'.format(name))
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='domains/' + str(name),
        #                               http_method='DELETE')
        command = self.commander.create_command(endpoint_url_complement=str(name),
                                                http_method='DELETE')
        return self._execute_command_and_log_it(command=command,
                                                msgInfo='Domain deleted with success.',
                                                msgError='Error on delete domain.')
