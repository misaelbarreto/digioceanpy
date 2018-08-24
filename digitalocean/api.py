# -*- coding: utf-8 -*-
from __future__ import with_statement

import json
import logging
import requests

from .utils import show_dict_as_pretty_json, extract_data_from_dict


class DigitalOceanEndPoint(object):
    def __init__(self, token, endpoint_url):
        self.commander = DigitalOceanCommander(token=token, endpoint_url=endpoint_url)

    def _execute_command_and_log_it(self, command, *args, **kwargs):
        response = command.execute()

        if response.is_ok:
            msg_info = kwargs.get('msg_info', None)
            if msg_info:
                if '{total}' in msg_info:
                    total = response.data.get('meta', {}).get('total', None)
                    if total is None:
                        total = 'no information'
                    else:
                        total = str(total)

                    msg_info = msg_info.format(total=str(total))

                logging.info(msg_info)
        else:
            msg_warm = kwargs.get('msg_warn', None)
            if msg_warm:
                logging.warn(msg_warm)
            else:
                msg_error = kwargs.get('msg_error', None)
                if msg_error:
                    logging.error(msg_error)

        return response


class DigitalOceanResponse(object):
    def __init__(self, digital_ocean_command, http_status, is_ok, header, data):
        self.digital_ocean_command = digital_ocean_command
        self.http_status = http_status
        self.is_ok = is_ok
        self.header = header
        self.data = data

    def extract_value_from_data(self, full_attribute_name):
        try:
            return extract_data_from_dict(data=self.data, full_attribute_name=full_attribute_name)
        except Exception as e:
            logging.critical('Error on extract value of attribute "{0}" from data of DigitalOceanResponse.'.format(
                full_attribute_name))
            logging.critical(show_dict_as_pretty_json(self.data))
            raise e

    def __str__(self):
        return 'digital_ocean_command:\n- full: {0} \n- detailed:\n {1}' \
               'http_status: {2} \n' \
               'is_ok: {3} \n' \
               'header: {4} \n' \
               'data:\n{5}' \
            .format(self.digital_ocean_command.curl_example_command,
                    self.digital_ocean_command.curl_example_command_to_log,
                    self.http_status,
                    self.is_ok,
                    self.header,
                    show_dict_as_pretty_json(self.data))


class DigitalOceanCommand:
    __CURL_EXAMPLE_COMMAND = 'curl \n' \
                             ' -X {http_method} \n' \
                             ' -H "Content-Type: application/json" \n' \
                             ' -H "Authorization: Bearer {token}" \n' \
                             ' {params} \n' \
                             ' "https://api.digitalocean.com/v2/{url_complement}" \n' \
                             ' -i \n'

    def __init__(self, token, url_complement, params=None, http_method='GET'):
        if not token:
            raise Exception('Token is required.')

        self.token = token
        self.url_complement = url_complement
        self.params = params
        self.http_method = http_method

    @property
    def curl_example_command(self):
        return self.__mount_curl_example_command()

    @property
    def curl_example_command_to_log(self):
        return self.__mount_curl_example_command(remove_break_lines=False)

    def __mount_curl_example_command(self, remove_break_lines=True):
        if self.params:
            params = ' -d \'{0}\''.format(json.dumps(self.params))
        else:
            params = ''

        result = self.__CURL_EXAMPLE_COMMAND.format(http_method=self.http_method,
                                                    token=self.token,
                                                    params=params,
                                                    url_complement=self.url_complement)
        if remove_break_lines:
            result = result.replace(' \n', '')
        return result

    def __str__(self):
        return self.curl_example_command

    def execute(self):
        request_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self.token)}

        url = 'https://api.digitalocean.com/v2/{0}'.format(self.url_complement)

        response = None
        if self.http_method == 'GET':
            response = requests.get(url, headers=request_headers, params=self.params)
        elif self.http_method == 'POST':
            response = requests.post(url, headers=request_headers, params=self.params)
        elif self.http_method == 'DELETE':
            response = requests.delete(url, headers=request_headers, params=self.params)


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

        digitalocean_response = DigitalOceanResponse(
            digital_ocean_command=self,
            http_status=http_status,
            is_ok=is_ok,
            header=response.headers,
            data=data
        )

        msgLog = 'Response:\n{0}'.format(digitalocean_response)

        # If the error is critical...
        if (digitalocean_response.http_status == 401) \
                or (http_status_server_error and self.http_method in ['POST', 'PUT']):
            logging.critical(msgLog)
            raise Exception('Critical error on execute command. Impossible to continue. Detail: {0}.'.format(digitalocean_response.http_status))
        else:
            logging.debug(msgLog)

        return digitalocean_response


class DigitalOceanCommander:
    def __init__(self, token, endpoint_url):
        self.token = token
        self.endpoint_url = endpoint_url

    def create_command(self, endpoint_url_complement='', params=None, http_method='GET'):
        return DigitalOceanCommand(token=self.token,
                                   url_complement=self.endpoint_url + endpoint_url_complement,
                                   params=params,
                                   http_method=http_method)
