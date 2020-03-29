import os
import site
from builtins import print

from invoke import task, call

config = dict(
    build_artifacts=[
        "build",
        "dist",
        ".eggs",
        "*.egg-info",
        "*.egg",
        "pip-wheel-metadata",
    ],
    runtime_artifacts=[
        "*.pyc",
        "*.pyo",
        "*~",
        "__pycache__",
        "*_pb2_grpc.py",
        "*_pb2.py",
    ],
)


@task
def clean(ctx, include_lock=False):
    print("Cleaning build and runtime artifacts")

    artifacts_to_delete = (
        config["runtime_artifacts"] + config["build_artifacts"] + (["poetry.lock"]
        if include_lock
        else [])
    )

    for artifact in artifacts_to_delete:
        command = f"find . -name {artifact} | xargs rm -rfv"
        ctx.run(command)


@task
def resolve(ctx, rich_output=True):
    ctx.run("poetry install -vvv", pty=rich_output)


@task
def init(ctx, include_lock=False, rich_output=True):
    clean(ctx, include_lock)
    resolve(ctx, rich_output=rich_output)


@task
def format(ctx):
    ctx.run("black .")


@task
def test(ctx, rich_output=True):
    ctx.run("pytest -s --show-capture=no", pty=rich_output)


@task(pre=[call(test, rich_output=False)])
def build(ctx, rich_output=True):
    ctx.run("poetry build", pty=rich_output)
