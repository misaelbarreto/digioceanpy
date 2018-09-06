# -*- coding: utf-8 -*-
from __future__ import with_statement

import json
import logging

import requests

from digiocean.utils import show_dict_as_pretty_json, extract_data_from_dict


class DigiOceanEndPoint(object):
    def __init__(self, token=None, endpoint_url=None):
        self.commander = DigiOceanCommander(token=token, endpoint_url=endpoint_url)


class DigiOceanRequest(object):
    def __init__(self, http_method, headers, url, params=None):
        self.headers = headers
        self.url = url
        self.http_method = http_method
        self.params = params


class DigiOceanResponse(object):
    def __init__(self, digi_ocean_command, http_status, is_ok, header, data, command):
        self.digi_ocean_command = digi_ocean_command
        self.http_status = http_status
        self.is_ok = is_ok
        self.header = header
        self.data = data
        self.command = command
        self.data_obj = None

    def parser(self):
        if self.data_obj is not None:
            return self.data_obj
        return None

    def extract_value_from_data(self, full_attribute_name):
        try:
            return extract_data_from_dict(data=self.data, full_attribute_name=full_attribute_name)
        except Exception as e:
            logging.critical('Error on extract value of attribute "{0}" from data of DigitalOceanResponse.'.format(
                full_attribute_name))
            logging.critical(show_dict_as_pretty_json(self.data))
            raise e

    def __str__(self):
        return 'curl_command_example:\n- full:\n {0} \n- detailed:\n {1}' \
               'http_status: {2} \n' \
               'is_ok: {3} \n' \
               'header: {4} \n' \
               'data:\n{5}' \
            .format(self.digi_ocean_command.curl_command_example,
                    self.digi_ocean_command.curl_command_example_to_log,
                    self.http_status,
                    self.is_ok,
                    self.header,
                    show_dict_as_pretty_json(self.data))


class DigiOceanCommand:
    __CURL_EXAMPLE_COMMAND = 'curl \n' \
                             ' -X {http_method} \n' \
                             ' -H "Content-Type: application/json" \n' \
                             ' -H "Authorization: Bearer {token}" \n' \
                             ' {params} \n' \
                             ' "{url}" \n' \
                             ' -i \n'

    def __init__(self, token, url_complement=None, params=None, http_method='GET'):
        if not token:
            raise Exception('Token is required.')

        self.token = token
        self.url_complement = url_complement

        # Montando o objeto de REQUEST.
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self.token)}

        url = 'https://api.digitalocean.com/v2/{0}'.format(self.url_complement)
        request = DigiOceanRequest(http_method=http_method, headers=headers, url=url, params=params)
        self.request = request

    @property
    def curl_command_example(self):
        return self.__mount_curl_example_command()

    @property
    def curl_command_example_to_log(self):
        return self.__mount_curl_example_command(remove_break_lines=False)

    def __mount_curl_example_command(self, remove_break_lines=True):
        if self.request.params:
            params = ' -d \'{0}\''.format(json.dumps(self.request.params))
        else:
            params = ''

        result = self.__CURL_EXAMPLE_COMMAND.format(http_method=self.request.http_method,
                                                    token=self.token,
                                                    params=params,
                                                    url=self.request.url)
        if remove_break_lines:
            result = result.replace(' \n', '')
        return result

    def __str__(self):
        return self.curl_command_example

    def execute(self, parser=None, data_field_to_parser=None, *args, **kwargs):
        response = None
        if self.request.http_method == 'GET':
            response = requests.get(self.request.url, headers=self.request.headers, params=self.request.params)
        elif self.request.http_method == 'POST':
            response = requests.post(self.request.url, headers=self.request.headers, params=self.request.params)
        elif self.request.http_method == 'DELETE':
            response = requests.delete(self.request.url, headers=self.request.headers, params=self.request.params)

        http_status = response.status_code
        http_status_sucess = (200 <= http_status <= 299)
        http_status_client_error = (300 <= http_status <= 399)
        http_status_server_error = (400 <= http_status <= 499)

        is_ok = http_status_sucess

        data = {}
        try:
            data = response.json()
        except:
            pass

        digi_ocean_response = DigiOceanResponse(
            digi_ocean_command=self,
            http_status=http_status,
            is_ok=is_ok,
            header=response.headers,
            data=data,
            command=self
        )

        if is_ok and data and parser and data_field_to_parser:
            digi_ocean_response.data_obj = parser.load(data[data_field_to_parser])

        msgLog = 'Response:\n{0}'.format(digi_ocean_response)

        message = digi_ocean_response.data.get('message', '')
        # TODO: Analyse if a error on DELETE is critical too?
        # If the error is critical...
        if (digi_ocean_response.http_status == 401) \
                or (http_status_server_error and self.request.http_method in ['POST', 'PUT', 'DELETE']):
            logging.critical(msgLog)
            raise Exception('Critical error on execute command. Impossible to continue. HttpStatus: {}. Message: {}.'.format(digi_ocean_response.http_status, message))
        else:
            logging.debug(msgLog)


        if http_status_sucess:
            msg_info = kwargs.get('msg_info', None)
            if msg_info:
                if '{total}' in msg_info:
                    total = digi_ocean_response.data.get('meta', {}).get('total', None)
                    if total is None:
                        total = 'no information'
                    else:
                        total = str(total)

                    msg_info = msg_info.format(total=str(total))

                logging.info(msg_info)
        else:
            if self.request.http_method == 'GET':
                msg_warm = kwargs.get('msg_warn', None)
                if msg_warm:
                    if message:
                        logging.warn(u'{} {}'.format(msg_warm, message))
                    else:
                        logging.warn(msg_warm)
            else:
                msg_error = kwargs.get('msg_error', None)
                if msg_error:
                    if message:
                        logging.error(u'{} {}'.format(msg_error, message))
                    else:
                        logging.error(msg_error)

        return digi_ocean_response


class DigiOceanCommander:
    def __init__(self, token, endpoint_url):
        self.token = token
        self.endpoint_url = endpoint_url

    def create_command(self, endpoint_url_complement='', params=None, http_method='GET'):
        return DigiOceanCommand(token=self.token,
                                url_complement=self.endpoint_url + endpoint_url_complement,
                                params=params,
                                http_method=http_method)
