import json

import click

import grpc
from loguru import logger
from warehouse.grpc import warehouse_pb2, warehouse_pb2_grpc


def _channel(host="localhost", port=50051):
    return grpc.insecure_channel(f"{host}:{port}")


@click.group()
@click.option("--host", default="localhost")
@click.option("--port", default=50051)
@click.pass_context
def product(ctx, host, port):
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["port"] = port


@product.command()
@click.pass_context
@click.argument("product")
def upsert(ctx, product):
    logger.info(f"Upserting {product}")
    product = json.loads(product)
    with _channel(ctx.obj["host"], ctx.obj["port"]) as channel:
        client = warehouse_pb2_grpc.ProductsStub(channel)
        client.AddOrUpdate(warehouse_pb2.Product(id=product["id"], name=product["name"], amount=product["amount"]))


@product.command()
@click.pass_context
@click.argument("product_id", type=int)
def query(ctx, product_id):
    logger.info(f"Querying {product_id}")
    with _channel(ctx.obj["host"], ctx.obj["port"]) as channel:
        client = warehouse_pb2_grpc.ProductsStub(channel)
        print(client.Query(warehouse_pb2.ProductQuery(id=product_id)))


@product.command()
@click.pass_context
@click.argument("product_id", type=int)
def delete(ctx, product_id):
    logger.info(f"Deleting {product_id}")
    with _channel(ctx.obj["host"], ctx.obj["port"]) as channel:
        client = warehouse_pb2_grpc.ProductsStub(channel)
        print(client.Delete(warehouse_pb2.ProductQuery(id=product_id)))


if __name__ == "__main__":
    product()
