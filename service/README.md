# sevice

A very simple implementation of a toy `grpc` server exposing two APIs:

* `product` for adding/querying/delete products from the warehouse
* `order` for order products from the warehouse

you can inspect `service/src/warehouse/service.py` and `service/tests/test_service.py` for the details.

To start the server run:

```bash
python service/src/warehouse/main.py
```

from the root directory of the project.
