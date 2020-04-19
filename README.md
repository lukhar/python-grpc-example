# python-grpc-example

A very simple python grpc project example simulating a warehouse. We can manage the stock using product API and places orders with order API.

## Project Structure

The project is separate into 3 independent modules each managed by `poetry`:

* `grpc` - this is where the `grpc` protobuf definitions and python biding live. It's possible to build and publish it independently so consumers of the API can implement their own clients to the warehouse service

* `service` - module contains a toy implementation of `grpc` server hosting `order` and `product` APIs implementations

* `client` - an example of command line clients using the `grpc` python binding to interact with the `server`


## Setup

1. Create virtual environment for the project with your favourite tool (ex. `pyenv`, `conda`)
2. Install latest version of [poetry](https://github.com/python-poetry/poetry)
3. Install [invoke](https://pypi.org/project/invoke/) - `pip install invoke`
4. Run `inv init` to install the dependencies.


## Useful Commands

* `inv init --include-lock` upgrade all projects dependencies and regenerate `poetry` lock files.
* `inv clean` clean `python` cache/build and other miscellaneous files
* `inv protogen` generate python `grpc` biddings from `.proto` definitions file
* `inv test` run `pytest` tests
* `inv format` format projects code base with `black`
