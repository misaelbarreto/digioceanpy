# -*- coding: utf-8 -*-
from __future__ import with_statement

from digiocean import DigiOcean
from settings import TOKEN
import logging
import unittest
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


class DomainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.digi_ocean = DigiOcean(token=TOKEN)

    @classmethod
    def tearDownClass(cls):
        cls.digiocean = None

    # def test_01_create(self):
    #     domain = self.digiocean.domains.create(name=self.domain_name, ip_address='1.2.3.4').parser()
    #     self.assertTrue(domain, 'Problem on create a domain.')
    #
    # def test_02_get(self):
    #     domain = self.digiocean.domains.get(name=self.domain_name)
    #     self.assertTrue(domain, 'Problem on get a domain.')
    #
    def test_03_list(self):
        ssh_keys = self.digi_ocean.ssh_keys.list().parser()
        self.assertTrue(len(ssh_keys), 'Problem to list domains.')
    #
    # def test_04_destroy(self):
    #     digiocean_response = self.digiocean.domains.delete(name=self.domain_name)
    #     self.assertTrue(digiocean_response.is_ok, 'Problem on delete a domain.')