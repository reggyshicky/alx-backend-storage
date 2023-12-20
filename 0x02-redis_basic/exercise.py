#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis()) and flush the
instance using flushdb. Create a store method that takes a data argument and
returns a string. The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.
Type-annotate store correctly.data can be a str, bytes, int or float.
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self) -> None:
        """Initializes the class Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()  # starts an empty cache

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in redis caches"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Get data from the redis Cache
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get data as a string from redis cache
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get data as integer from redis cache
        """
        return self.get(key, int)