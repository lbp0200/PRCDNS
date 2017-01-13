import rocksdb


class DomainCache:
    def read(self):
        db = rocksdb.DB("/tmp/test.db", rocksdb.Options(create_if_missing=True))
        # Store
        db.put(b"key", b"value")

        # Get
        print(db.get(b"key"))

        # Delete
        db.delete(b"key")
