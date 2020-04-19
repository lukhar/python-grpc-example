import json

import click
from loguru import logger

import grpc
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc


def _channel(host="localhost", port=50051):
    return grpc.insecure_channel(f"{host}:{port}")


@click.group()
@click.option("--host", default="localhost")
@click.option("--port", default=50051)
@click.pass_context
def order(ctx, host, port):
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["port"] = port


@order.command()
@click.pass_context
@click.argument("orders")
def place(ctx, orders):
    logger.info(f"Ordering: {orders}")
    orders = json.loads(orders)
    with _channel(ctx.obj["host"], ctx.obj["port"]) as channel:
        client = warehouse_pb2_grpc.OrdersStub(channel)
        for confirmation in client.Place(
            warehouse_pb2.Order(id=order["id"], amount=order["amount"]) for order in orders
        ):
            logger.info(f"Product status:\n {confirmation}")


if __name__ == "__main__":
    order()
