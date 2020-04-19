# client

A toy client demonstrating use of `grpc` python bindings. After starting `server` in `service` module run:

* `python client/src/warehouse/client/product.py upsert '{"id": 1, "name": "sanitizer", "amount":3}'` to add 3 sanitizers to warehouse
* `python client/src/warehouse/client/product.py query 1` to query for product with `id` `1`
* `python client/src/warehouse/client/product.py delete 1` to delete product with `id` `1`
