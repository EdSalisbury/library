from vendor.models import Amazon
from amazon.api import AmazonAPI

class AmazonController:

    def __init__(self):
        keys = Amazon.objects.all()
        key = keys[0]
        self.amazon = AmazonAPI(key.access_key.encode('ascii'), key.secret_key.encode('ascii'), key.assoc_tag.encode('ascii'))

    def lookup(self, item_id, id_type = 'ASIN', search_index = ''):

        try:
            product = self.amazon.lookup(ItemId = item_id, IdType = id_type, SearchIndex = search_index)
            if type(product) == 'list':
                return product[0]
            else:
                return product
        except:
            return None
