from google.protobuf import empty_pb2
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc
from typing import Iterable


class ProductsService(warehouse_pb2_grpc.ProductsServicer):

    def __init__(self, repository):
        self._products = repository

    def AddOrUpdate(self, product: warehouse_pb2.Product, context) -> warehouse_pb2.Product:
        return product

    def Delete(self, query: warehouse_pb2.ProductQuery, context) -> empty_pb2.Empty:
        return empty_pb2.Empty

    def Query(self, query: warehouse_pb2.ProductQuery, context) -> Iterable[warehouse_pb2.Confirmation]:
        return warehouse_pb2.Confirmation()


class OrdersService(warehouse_pb2_grpc.OrdersServicer):
    def Place(self, orders: Iterable[warehouse_pb2.Order], context) -> Iterable[warehouse_pb2.Confirmation]:
        raise NotImplementedError
