# -*- coding: utf-8 -*-
from __future__ import with_statement

from digiocean import DigiOcean
# Create your "tests/settings.py" file based on the "tests/base_settings.py".
from settings import digi_ocean_TOKEN, DOMAIN_NAME, DOMAIN_IP_ADDRESS
import logging
import unittest
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class DomainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.digiocean = DigiOcean(token=digi_ocean_TOKEN)
        cls.base_domain_name = 'www.digioceanpy-test-'
        cls.domain_name = '{}{}.com'.format(cls.base_domain_name, random.randint(1000, 9999))

    @classmethod
    def tearDownClass(cls):
        cls.digiocean = None

    def test_01_create(self):
        domain = self.digiocean.domains.create(name=self.domain_name, ip_address='1.2.3.4').parser()
        self.assertTrue(domain, 'Problem on create a domain.')

    def test_02_get(self):
        domain = self.digiocean.domains.get(name=self.domain_name)
        self.assertTrue(domain, 'Problem on get a domain.')

    def test_03_list(self):
        domains = self.digiocean.domains.list().parser()
        self.assertTrue(len(domains)>0, 'Problem to list domains.')

    def test_04_destroy(self):
        digiocean_response = self.digiocean.domains.delete(name=self.domain_name)
        self.assertTrue(digiocean_response.is_ok, 'Problem on delete a domain.')

    def test_05_destroy_inexisting_domain(self):
        digiocean_response = self.digiocean.domains.delete(name=self.domain_name+'xxx')
        self.assertFalse(digiocean_response.is_ok, 'Not problem on try to delete a domain that not exists')

    def test_06_destroy_all_test_domains(self):
        # Deleting all test domanis, if exists!
        logging.info('Deleting all test domains...')
        domains = self.digiocean.domains.list().parser()
        for d in domains:
            if self.base_domain_name in d.name:
                self.digiocean.domains.delete(name=d.name)