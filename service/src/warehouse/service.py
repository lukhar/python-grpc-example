from typing import Iterable

from google.protobuf import empty_pb2

import grpc
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc
from warehouse.repository import InMemoryProductRepository


class ProductsService(warehouse_pb2_grpc.ProductsServicer):
    def __init__(self, repository: InMemoryProductRepository) -> None:
        self._products = repository

    def AddOrUpdate(self, product: warehouse_pb2.Product, context) -> warehouse_pb2.Product:
        self._products.upsert(product)
        return product

    def Delete(self, query: warehouse_pb2.ProductQuery, context) -> empty_pb2.Empty:
        self._products.delete(product_id=query.id)
        return empty_pb2.Empty()

    def Query(self, query: warehouse_pb2.ProductQuery, context: grpc.ServicerContext) -> warehouse_pb2.Product:
        product = self._products.query(product_id=query.id)
        if not product:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Product: {query.id} not found!")

        return self._products.query(product_id=query.id)


class OrdersService(warehouse_pb2_grpc.OrdersServicer):
    def Place(self, orders: Iterable[warehouse_pb2.Order], context) -> Iterable[warehouse_pb2.Confirmation]:
        raise NotImplementedError
