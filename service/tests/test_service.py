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


@pytest.fixture
def process_orders(orders_client):
    def process(*orders):
        return [*orders_client.Place(order for order in orders)]

    return process


class TestOrderSerivce:
    def test_given_no_products_in_warehouse_should_decline_order(self, process_orders):
        a_valid_order = warehouse_pb2.Order(id=1, amount=3)

        confirmations = process_orders(a_valid_order)

        assert confirmations == [warehouse_pb2.Confirmation(status=warehouse_pb2.Confirmation.Status.DECLINED)]

    def test_given_matching_products_in_warehouse_should_place_order(self, products_client, process_orders):
        sanitizer = warehouse_pb2.Product(id=1, name="sanitizer", amount=10)
        products_client.AddOrUpdate(sanitizer)

        sanitizer_order = warehouse_pb2.Order(id=sanitizer.id, amount=3)
        confirmations = process_orders(sanitizer_order)

        assert confirmations == [
            warehouse_pb2.Confirmation(
                status=warehouse_pb2.Confirmation.Status.APPROVED,
                product=warehouse_pb2.Product(id=1, name="sanitizer", amount=3),
            )
        ]

    def test_given_insuffiecnt_amount_of_products_in_warehouse_should_decline_the_order(
        self, products_client, process_orders
    ):
        toilet_paper = warehouse_pb2.Product(id=2, name="toilet_paper", amount=2)
        products_client.AddOrUpdate(toilet_paper)

        toilet_paper_order = warehouse_pb2.Order(id=toilet_paper.id, amount=3)
        confirmations = process_orders(toilet_paper_order)

        assert confirmations == [warehouse_pb2.Confirmation(status=warehouse_pb2.Confirmation.Status.DECLINED)]

    def test_given_subsequent_orders_should_start_declining_when_there_is_not_enough_products_in_warehouse(
        self, products_client, process_orders
    ):
        toilet_paper = warehouse_pb2.Product(id=2, name="toilet_paper", amount=10)
        products_client.AddOrUpdate(toilet_paper)

        toliet_paper_orders = [
            warehouse_pb2.Order(id=toilet_paper.id, amount=3),
            warehouse_pb2.Order(id=toilet_paper.id, amount=6),
            warehouse_pb2.Order(id=toilet_paper.id, amount=3),
        ]
        confirmations = process_orders(*toliet_paper_orders)

        assert confirmations == [
            warehouse_pb2.Confirmation(
                status=warehouse_pb2.Confirmation.Status.APPROVED,
                product=warehouse_pb2.Product(id=2, name="toilet_paper", amount=3),
            ),
            warehouse_pb2.Confirmation(
                status=warehouse_pb2.Confirmation.Status.APPROVED,
                product=warehouse_pb2.Product(id=2, name="toilet_paper", amount=6),
            ),
            warehouse_pb2.Confirmation(status=warehouse_pb2.Confirmation.Status.DECLINED),
        ]
