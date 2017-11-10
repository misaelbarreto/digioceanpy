from digitalocean import DigitalOcean
from settings import DIGITAL_OCEAN_TOKEN

digitalocean = DigitalOcean(token=DIGITAL_OCEAN_TOKEN)
print digitalocean.domains.list()

