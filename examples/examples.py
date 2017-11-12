from digitalocean import DigitalOcean
# Create your "examples/settings.py" file based on the "examples/base_settings.py".
from settings import DIGITAL_OCEAN_TOKEN, DOMAIN_NAME, DOMAIN_IP_ADDRESS
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
digitalocean = DigitalOcean(token=DIGITAL_OCEAN_TOKEN)

def domain_examle():
    # Create a domain...
    domain = digitalocean.domains.create(name=DOMAIN_NAME, ip_address=DOMAIN_IP_ADDRESS)
    if domain.is_ok:
        # Find the domain was just created...
        domain = digitalocean.domains.get(domain.data['domain'])

    domains = digitalocean.domains.list()
    if domains.is_ok:
        for domain in domains.data['domains']:
            print domains['name']


    # Deleting the domain was just created...
    domain = digitalocean.domains.delete(name=DOMAIN_NAME)

if __name__ == '__main__':
    domain_examle()