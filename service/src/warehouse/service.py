from typing import Iterable

from google.protobuf import empty_pb2
from loguru import logger

import grpc
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc
from warehouse.repository import InMemoryProductRepository


class ProductsService(warehouse_pb2_grpc.ProductsServicer):
    def __init__(self, repository: InMemoryProductRepository) -> None:
        self._products = repository

    def AddOrUpdate(self, product: warehouse_pb2.Product, context) -> warehouse_pb2.Product:
        logger.info(f"Upsert product: [id={product.id}, name={product.name}, amount={product.amount}]")
        self._products.upsert(product)
        return product

    def Delete(self, query: warehouse_pb2.ProductQuery, context) -> empty_pb2.Empty:
        logger.info(f"Delete product id={query.id}")
        self._products.delete(product_id=query.id)
        return empty_pb2.Empty()

    def Query(self, query: warehouse_pb2.ProductQuery, context: grpc.ServicerContext) -> warehouse_pb2.Product:
        logger.info(f"Query product id={query.id}")
        product = self._products.query(product_id=query.id)
        if not product:
            not_found_message = f"Product: {query.id} not found!"
            logger.info(not_found_message)
            context.abort(grpc.StatusCode.NOT_FOUND, not_found_message)

        return self._products.query(product_id=query.id)


class OrdersService(warehouse_pb2_grpc.OrdersServicer):
    def __init__(self, repository: InMemoryProductRepository) -> None:
        self._products = repository

    def Place(self, orders: Iterable[warehouse_pb2.Order], context) -> Iterable[warehouse_pb2.Confirmation]:
        for order in orders:
            logger.info(f"Order product id={order.id} amount={order.amount}")
            product = self._products.query(product_id=order.id)
            if product and order.amount <= product.amount:
                yield warehouse_pb2.Confirmation(
                    status=warehouse_pb2.Confirmation.Status.APPROVED,
                    product=warehouse_pb2.Product(id=product.id, name=product.name, amount=order.amount),
                )
                self._products.upsert(
                    warehouse_pb2.Product(id=product.id, name=product.name, amount=product.amount - order.amount)
                )
            else:
                logger.warning(f"Failed to order product id={order.id} amount={order.amount}")
                yield warehouse_pb2.Confirmation(status=warehouse_pb2.Confirmation.Status.DECLINED)
