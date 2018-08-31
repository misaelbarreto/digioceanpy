from digitalocean import DigitalOcean
# Create your "tests/settings.py" file based on the "tests/base_settings.py".
from settings import DIGITAL_OCEAN_TOKEN, DOMAIN_NAME, DOMAIN_IP_ADDRESS
import logging
import unittest
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
#digitalocean = DigitalOcean(token=DIGITAL_OCEAN_TOKEN)

class DomainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.digitalocean = DigitalOcean(token=DIGITAL_OCEAN_TOKEN)
        cls.domain_name = 'www.digioceanpytest{0}.com'.format(random.randint(1000, 9999))

    @classmethod
    def tearDownClass(cls):
        cls.digitalocean = None

    def test_list(self):
        domains = self.digitalocean.domains.list().parser()
        print domains
        self.assertTrue(domains is not None, 'Problem to list domains.')

    def test_create(self):
        domain = self.digitalocean.domains.create(name=self.domain_name, ip_address='1.2.3.4').parser()
        self.assertTrue(domain, 'Problem on create a domain.')
    #
    # def test_destroy(self):
    #     domains = self.digitalocean.domains.delete(name=self.domain_name)
    #     self.assertTrue(domains.is_ok, 'Problem on delete a domain.')

    # def test_list(self):
    #     domains_response = self.digitalocean.domains.list()
    #     for domain in domains_response.data['domains']:
    #         domains_response_delete = self.digitalocean.domains.delete(name=domain['name'])
    #         self.assertTrue(domains_response_delete.is_ok, 'Problem on delete a domain.')

            # def domain_examle():
#     # Create a domain...
#     domain = digitalocean.domains.create(name=DOMAIN_NAME, ip_address=DOMAIN_IP_ADDRESS)
#     if domain.is_ok:
#         # Find the domain was just created...
#         domain = digitalocean.domains.get(domain.data['domain'])
#
#     domains = digitalocean.domains.list()
#     if domains.is_ok:
#         for domain in domains.data['domains']:
#             print domains['name']
#
#
#     # Deleting the domain was just created...
#     domain = digitalocean.domains.delete(name=DOMAIN_NAME)
#
# if __name__ == '__main__':
#     domain_examle()