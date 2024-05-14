import os

from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import MemoryStorage, JSONStorage

doc = {'none': [None, None], 'int': 42, 'float': 3.1415899999999999,
       'list': ['LITE', 'RES_ACID', 'SUS_DEXT'],
       'dict': {'hp': 13, 'sp': 5},
       'bool': [True, False, True, False]}


def test_caching(storage):
    # Write contents
    storage.write(doc)

    # Verify contents
    assert doc == storage.read()


def test_caching_read():
    from tinydb import TinyDB, MemoryStorage
    from tinydb.middlewares import CachingMiddleware

    db = TinyDB(storage=CachingMiddleware(MemoryStorage()))
    assert db.all() == []


def test_caching_write_many(storage):
    storage.WRITE_CACHE_SIZE = 3

    # Storage should be still empty
    assert not hasattr(storage.storage, 'memory') or storage.storage.memory is None

    # Write contents
    for x in range(2):
        storage.write(doc)
        assert storage.storage.memory is None  # Still cached

    storage.write(doc)

    # Verify contents: Cache should be emptied and written to storage
    assert storage.storage.memory


def test_caching_flush(storage):
    doc = {'key': 'value'}
    for _ in range(CachingMiddleware.WRITE_CACHE_SIZE - 1):
        storage.write(doc)
    assert not storage.memory
    storage.flush()
    assert storage.memory == {}


def test_caching_flush_manually(storage):
    doc = {'key': 'value'}
    storage.write(doc)
    storage.flush()
    assert storage.memory == {}


def test_caching_write(storage):
    doc = {'key': 'value'}
    storage.write(doc)
    storage.close()
    assert storage.storage.memory == {'_default': {'1': doc}}


def test_nested():
    storage = CachingMiddleware(MemoryStorage)
    storage()  # Initialization

    # Write contents
    storage.write(doc)

    # Verify contents
    assert doc == storage.read()


def test_caching_json_write(tmpdir):
    path = str(tmpdir.join('test.db'))
    with TinyDB(path, storage=CachingMiddleware(JSONStorage)) as db:
        db.insert({'key': 'value'})
