# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
from digitalocean.api import DigiOceanEndPoint, DigiOceanCommand
from digitalocean.endpoints import DigiOceanModel


class Domain(DigiOceanModel):
    def __init__(self, name=None, ttl=None, zone_file=None, *args, **kwargs):
        self.name = name
        self.ttl = ttl
        self.zone_file = zone_file
        # super(Domain, self).__init__(*args, **kwargs)


class DomainEndpoint(DigiOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(DomainEndpoint, self).__init__(*args, **kwargs)

    def list(self, return_response=False):
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
        result = command.execute(parser=Domain, data_field_to_parser='domains',
                                 msg_info='Domains found (total: {total}).', msg_warn='No domains found.')
        # result.data_obj = Domain.load(result.data['domains'])
        return result

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
        return command.execute(command=command,
                               msg_info='Domain found.',
                               msg_warn='Domain not found.')

    def create(self, name, ip_address):
        '''
        Create a new domain.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#create-a-new-domain

        Example:
        curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" -d '{"name":"examples.com","ip_address":"1.2.3.4"}' "https://api.digitalocean.com/v2/domains"

        :param name: The name of domain. Ex: app.myname.com
        :param ip_address: This attribute contains the IP address you want the domain to point to.
        :return: a DigitalOceanResponse.
        '''
        logging.info('Creating the domain {0} with ip {1}...'.format(name, ip_address))
        params = {'name': name, 'ip_address': ip_address}
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='domains/',
        #                               params=params,
        #                               http_method='POST')
        command = self.commander.create_command(params=params, http_method='POST')
        response = command.execute(parser=Domain, data_field_to_parser='domain',
                                   msg_info='Domains found (total: {total}).',
                                   msg_warn='No domains found.',)
        return response

    def delete(self, name):
        logging.info('Deleting the domain "{0}"...'.format(name))
        # command = DigitalOceanCommand(token=self.token,
        #                               url_complement='domains/' + str(name),
        #                               http_method='DELETE')
        command = self.commander.create_command(endpoint_url_complement=str(name),
                                                http_method='DELETE')
        return command.execute(command=command,
                               msg_info='Domain deleted with success.',
                               msgError='Error on delete domain.')
