import grpc
import time

from concurrent import futures


class Server:

    ONE_DAY_IN_SECONDS = 60 * 60 * 24

    def __init__(self, port=50051, max_workers=10):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    @property
    def port(self):
        return self._port

    def start(self, timeout=None, testing=False):
        if not timeout:
            timeout = Server.ONE_DAY_IN_SECONDS

        if testing:
            return

        try:
            while True:
                time.sleep(timeout)
        except KeyboardInterrupt:
            self._server.stop(grace=0)


if __name__ == "__main__":
    Server().start()
