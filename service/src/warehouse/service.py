from google.protobuf import empty_pb2
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc
from typing import Iterable


class ProductsService(warehouse_pb2_grpc.ProductsServicer):
    def AddOrUpdate(self, product: warehouse_pb2.Product) -> warehouse_pb2.Product:
        raise NotImplementedError

    def Delete(self, query: warehouse_pb2.ProductQuery) -> empty_pb2.Empty:
        return empty_pb2.Empty

    def Query(self, query: warehouse_pb2.ProductQuery) -> Iterable[warehouse_pb2.Confirmation]:
        raise NotImplementedError


class OrdersService(warehouse_pb2_grpc.OrdersServicer):
    def Place(self, orders: Iterable[warehouse_pb2.Order]) -> Iterable[warehouse_pb2.Confirmation]:
        raise NotADirectoryError
