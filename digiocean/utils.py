# -*- coding: utf-8 -*-
from __future__ import with_statement

import logging
import os
from os import path
import json

#from fabric.api import local


def show_dict_as_pretty_json(data):
    return json.dumps(data, indent=4, sort_keys=True)
#
# def get_or_create_local_ssh_key():
#     home_dir = local('echo $HOME', capture=True)
#     ssh_dir = path.join(home_dir, '.ssh')
#     public_key_path = path.join(ssh_dir, 'id_rsa.pub')
#
#     if not os.path.exists(ssh_dir):
#         local('mkdir %s' % ssh_dir)
#
#     logging.info('Checking if exists the file "{0}"...'.format(public_key_path))
#     if not path.exists(public_key_path):
#         logging.info('File not exists. It will be created...')
#         local("ssh-keygen -f %s/id_rsa -t rsa -N ''" % ssh_dir)
#         logging.info('File created.')
#     else:
#         logging.info('File exists.')
#
#
#     public_key = open(public_key_path, 'r').read().strip()
#     logging.info('Local public key got with success...')
#     return public_key


def extract_data_from_dict(data, full_attribute_name, result=None):
    '''
    Is a util method to extract data from a dictionary using a simple sintaxe.

    Example:
    users = {'users': [
        {'id': 1, 'name': 'Misael', 'address':{'number': 111, 'state': 'RN'}},
        {'id': 2, 'name': 'Anita', 'address':{'number': 333, 'state': 'CE'}},
    ]}
    print extract_data_from_dict(users, 'users.address.number')
    > [111, 333]
    print extract_data_from_dict(users, 'users.address')
    > [{'state': 'RN', 'number': 111}, {'state': 'CE', 'number': 333}]


    users = {'users': 'Misael'}
    print extract_data_from_dict(users, 'users')
    > Misael


    users = [
        {'id': 1, 'name': 'Misael', 'address':{'number': 111, 'state': 'RN'}},
        {'id': 2, 'name': 'Anita', 'address':{'number': 333, 'state': 'CE'}},
    ]
    print extract_data_from_dict(users, 'id')
    [1, 2]


    :param data is a dict or a list of dicts
    :param full_attribute_name: the full field name. Ex: users.name
    :param result: internal param necessary to recursive process.
    :return: the data request. As a dictionary, the return type can be any type.
    '''
    msg_exception = 'The data param must be a dictionary or a list of dictionaries'
    if not isinstance(data, dict) and not isinstance(data, list):
        raise Exception(msg_exception)

    att_current = full_attribute_name.split('.')[0]
    atts_rest = '.'.join(full_attribute_name.split('.')[1:])

    if result is None:
        result = list()

    # data_list is a strategy to always use the loop below to do
    # the job, independent of data be a dict or a list.
    data_list = list()
    if isinstance(data, dict):
        data_list.append(data)
    else:
        data_list = data

    # d is a dict
    for d in data_list:
        if not isinstance(d, dict):
            raise Exception(msg_exception)

        info = d[att_current]

        if atts_rest:
            if (isinstance(info, list) or isinstance(info, dict)):
                extract_data_from_dict(info, atts_rest, result)
            else:
                raise Exception('Attributte "{0}" not exists'.format(atts_rest[0]))
        else:
            result.append(info)

    if len(result)==1:
        return result[0]
    else:
        return result