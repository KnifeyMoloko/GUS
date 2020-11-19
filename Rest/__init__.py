from rest.gus_rest_client import GUSClient
from common.helpers import get_api_key

client = GUSClient(ssl=True, api_key=get_api_key())
