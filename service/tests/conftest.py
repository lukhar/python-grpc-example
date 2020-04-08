import grpc
import pytest

from warehouse.repository import InMemoryProductRepository
from warehouse.main import Server
from warehouse.grpc import warehouse_pb2_grpc


@pytest.fixture
def server():
    server = Server(InMemoryProductRepository())
    server.start(testing=True)
    yield server
    server.stop()


@pytest.fixture
def products_client(server):
    with grpc.insecure_channel(f"localhost:{server.port}") as channel:
        yield warehouse_pb2_grpc.ProductsStub(channel)
