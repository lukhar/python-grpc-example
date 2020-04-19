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
        config["runtime_artifacts"]
        + config["build_artifacts"]
        + (["poetry.lock"] if include_lock else [])
    )

    for artifact in artifacts_to_delete:
        command = f"find . -name {artifact} | xargs rm -rfv"
        ctx.run(command)


@task
def protogen(ctx):
    print("\nGenerating protobufs\n")

    with ctx.cd("grpc"):
        service_definitions_path = "src"
        library_definitions_path = site.getsitepackages().pop()
        code_path = "src"
        command = f"""python -m grpc.tools.protoc \
                --proto_path={service_definitions_path} \
                --proto_path={library_definitions_path} \
                --python_out={code_path} \
                --grpc_python_out={code_path} {service_definitions_path}/warehouse/grpc/warehouse.proto
                """
        ctx.run(command)


@task(post=[protogen])
def resolve(ctx, rich_output=True):
    with ctx.cd("grpc"):
        print("\nResolving grpc dependencies...\n")
        ctx.run("poetry install -vvv", pty=rich_output)
    with ctx.cd("service"):
        print("\nResolving service dependencies...\n")
        ctx.run("poetry install -vvv", pty=rich_output)
    with ctx.cd("client"):
        print("\nResolving client dependencies...\n")
        ctx.run("poetry install -vvv", pty=rich_output)


@task
def init(ctx, include_lock=False, rich_output=True):
    clean(ctx, include_lock)
    resolve(ctx, rich_output=rich_output)
    protogen(ctx)


@task
def format(ctx):
    with ctx.cd("service"):
        ctx.run("black .")
    with ctx.cd("grpc"):
        ctx.run("black .")
    with ctx.cd("client"):
        ctx.run("black .")


@task
def test(ctx, rich_output=True):
    ctx.run("pytest -s --show-capture=no", pty=rich_output)
