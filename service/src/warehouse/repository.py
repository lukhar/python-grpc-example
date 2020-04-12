class InMemoryProductRepository:
    def __init__(self):
        self._datastore = {}

    def upsert(self, product):
        self._datastore[product.id] = product

    def query(self, product_id):
        return self._datastore.get(product_id)

    def delete(self, product_id):
        del self._datastore[product_id]
