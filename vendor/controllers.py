from vendor.models import Amazon
import logging
from amazon.api import AmazonAPI

logger = logging.getLogger(__name__)

class AmazonController:

    def __init__(self):
        keys = Amazon.objects.all()
        key = keys[0]
        self.amazon = AmazonAPI(key.access_key.encode('ascii'), key.secret_key.encode('ascii'), key.assoc_tag.encode('ascii'))

    def lookup(self, item_id, id_type = 'ASIN', search_index = ''):
        try:
            response = self.amazon.lookup(ItemId = item_id, IdType = id_type, SearchIndex = search_index)
            return response

        except:
            return None
