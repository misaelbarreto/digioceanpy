# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging

from digiocean.endpoints import DigiOceanEndPoint
from digiocean.models import Domain


class DomainEndpoint(DigiOceanEndPoint):
    def __init__(self, *args, **kwargs):
        super(DomainEndpoint, self).__init__(*args, **kwargs)

    def list(self, return_response=False):
        '''
        To retrieve a list of all of the domains in your account,

        Based in DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#list-all-domains

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digiocean.com/v2/domains"

        :return: a DigitalOceanResponse.
        '''
        logging.info('Retrieving all domains...')
        command = self.commander.create_command()
        result = command.execute(parser=Domain, data_field_to_parser='domains',
                                 msg_info='Domains found (total: {total}).',
                                 msg_warn='No domains found.')
        return result

    def get(self, name):
        '''
        Retrieve information about a specific domain.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#retrieve-an-existing-domain

        Example:
        curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digiocean.com/v2/domains/examples.com"

        :param name: The name of domain. Ex: mydomain.com
        :return: a DigitalOceanResponse
        '''
        logging.info('Retrieving the domain "{}"...'.format(name))
        command = self.commander.create_command(endpoint_url_complement=name)
        return command.execute(command=command,
                               msg_info='Domain found.',
                               msg_warn='Domain not found.')

    def create(self, name, ip_address):
        '''
        Create a new domain.

        Based on DigitalOcean API:
        Url: https://developers.digitalocean.com/documentation/v2/#create-a-new-domain

        Example:
        curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" -d '{"name":"examples.com","ip_address":"1.2.3.4"}' "https://api.digiocean.com/v2/domains"

        :param name: The name of domain. Ex: app.myname.com
        :param ip_address: This attribute contains the IP address you want the domain to point to.
        :return: a DigitalOceanResponse.
        '''
        logging.info('Creating the domain {0} with ip {1}...'.format(name, ip_address))
        params = {'name': name, 'ip_address': ip_address}
        command = self.commander.create_command(params=params, http_method='POST')
        response = command.execute(parser=Domain, data_field_to_parser='domain',
                                   msg_info='Domains created.',
                                   msg_error='Error on create domain.', )
        return response

    def delete(self, name):
        '''
        To delete a domain, send a DELETE request to /v2/domains/$DOMAIN_NAME.
        The domain will be removed from your account and a response status of 204 will be returned. This indicates a successful request with no response body.

        Based on DigitalOcean API:
        https://developers.digitalocean.com/documentation/v2/#delete-a-domain

        Example:
        curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer b7d03a6947b217efb6f3ec3bd3504582" "https://api.digitalocean.com/v2/domains/example.com"

        :param name: The name of domain. Ex: app.myname.com
        :return: a DigitalOceanResponse
        '''

        logging.info('Deleting the domain "{0}"...'.format(name))
        command = self.commander.create_command(endpoint_url_complement=str(name),
                                                http_method='DELETE')
        return command.execute(command=command,
                               msg_info='Domain deleted with success.',
                               msg_error='Error on delete domain.')
