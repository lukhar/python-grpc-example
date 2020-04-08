from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc


def test_given_valid_product_should_add_it_to_warehouse(products_client: warehouse_pb2_grpc.ProductsStub):
    valid_product = warehouse_pb2.Product(id=1, name="sanitizer", amount=10)

    stored_product = products_client.AddOrUpdate(valid_product)

    assert valid_product == stored_product
