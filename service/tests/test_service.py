import pytest

import grpc
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc


class TestProductService:
    def test_given_valid_product_should_add_it_to_warehouse(self, products_client: warehouse_pb2_grpc.ProductsStub):
        valid_product = warehouse_pb2.Product(id=1, name="sanitizer", amount=10)

        stored_product = products_client.AddOrUpdate(valid_product)

        retrieved_product = products_client.Query(warehouse_pb2.ProductQuery(id=valid_product.id))

        assert retrieved_product == stored_product

    def test_given_non_existing_product_id_should_raise_exception(
        self, products_client: warehouse_pb2_grpc.ProductsStub
    ):
        non_existing_product_id = 9999999

        with pytest.raises(grpc.RpcError) as exception_info:
            products_client.Query(warehouse_pb2.ProductQuery(id=non_existing_product_id))

        assert exception_info.value.code() == grpc.StatusCode.NOT_FOUND

    def test_given_existing_product_should_delete_it_from_warehouse(
        self, products_client: warehouse_pb2_grpc.ProductsStub
    ):
        valid_product = warehouse_pb2.Product(id=1, name="sanitizer", amount=10)

        stored_product = products_client.AddOrUpdate(valid_product)

        products_client.Delete(warehouse_pb2.ProductQuery(id=stored_product.id))

        with pytest.raises(grpc.RpcError) as exception_info:
            products_client.Query(warehouse_pb2.ProductQuery(id=stored_product.id))

        assert exception_info.value.code() == grpc.StatusCode.NOT_FOUND
