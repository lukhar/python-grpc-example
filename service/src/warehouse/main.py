import grpc
import time

from concurrent import futures
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc
from warehouse.repository import InMemoryProductRepository
from warehouse.service import ProductsService


class Server:

    ONE_DAY_IN_SECONDS = 60 * 60 * 24

    def __init__(self, products_repository=InMemoryProductRepository(), port=50051, max_workers=10):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        self._port = port
        self._server.add_insecure_port(f"[::]:{self._port}")

        warehouse_pb2_grpc.add_ProductsServicer_to_server(
            ProductsService(products_repository), self._server
        )

    @property
    def port(self):
        return self._port

    def start(self, timeout=None, testing=False):
        if not timeout:
            timeout = Server.ONE_DAY_IN_SECONDS

        self._server.start()

        if testing:
            return

        try:
            while True:
                time.sleep(timeout)
        except KeyboardInterrupt:
            self._server.stop(grace=0)

    def stop(self):
        self._server.stop(grace=0)


if __name__ == "__main__":
    Server().start()
