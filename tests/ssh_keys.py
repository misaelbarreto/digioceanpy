# -*- coding: utf-8 -*-
from __future__ import with_statement

from digiocean import DigiOcean
from settings import TOKEN, SSH_PUBLIC_KEY
import logging
import unittest

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)


class SshKeyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.digi_ocean = DigiOcean(token=TOKEN)
        cls.base_ssh_name = 'digiocean-test'
        cls.ssh_key_created = None

    @classmethod
    def tearDownClass(cls):
        cls.digiocean = None

    def test_01_create(self):
        ssh_key = self.digi_ocean.ssh_keys.create(name=self.base_ssh_name, public_key=SSH_PUBLIC_KEY).parser()
        SshKeyTest.ssh_key_created = ssh_key
        self.assertTrue(ssh_key, 'Problem on create a ssh key.')

    def test_02_get(self):
        ssh_key = self.digi_ocean.ssh_keys.get(id_or_fingerprint=self.ssh_key_created.id).parser()
        self.assertTrue(ssh_key, 'Problem on get a ssh key.')

    def test_03_list(self):
        ssh_keys = self.digi_ocean.ssh_keys.list().parser()
        self.assertTrue(len(ssh_keys), 'Problem to list domains.')

    def test_05_destroy_all_test_ssh_keys(self):
        logging.info('Deleting all test ssh keys...')
        ssh_keys = self.digi_ocean.ssh_keys.list().parser()
        for s in ssh_keys:
            if self.base_ssh_name in s.name:
                self.digi_ocean.ssh_keys.delete(id_or_fingerprint=s.id)