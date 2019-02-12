import requests
import pickle
import gzip
import time
from .sqlite3db import SQLite3Database

__version__ = "0.2.0"


class Session:
    def __init__(self, database, compress=True, index=True, synchronous=True):
        self._compress = compress
        self._database = SQLite3Database(database, index, synchronous)
        self._index = index
        self._synchronous = synchronous
        self._session = requests.session()
        self._last_response_time = 0
        self._last_response_use_cache = True

    def _put_response(self, url, response):
        response = self._serialize_response(response)
        self._database.put_response(url, response)

    def _get_response(self, url):
        response = self._database.get_response(url)
        if response is None:
            return response
        else:
            return self._deserialize_response(response)

    def __getattr__(self, name):
        if name == "get":
            return self._get
        else:
            return getattr(self._session, name)

    def _get(self, url, use_cache=True, **kwargs):
        cached_response = self._get_response(url) if use_cache else None
        if cached_response is not None:
            cached_response.from_cache = True
            self._last_response_use_cache = True
            return cached_response
        else:
            response = self._session.get(url, **kwargs)
            response.from_cache = False
            self._last_response_use_cache = False
            self._last_response_time = time.time()
            self._put_response(url, response)
            return response

    def _serialize_response(self, response):
        pickled_response = pickle.dumps(response)
        if self._compress:
            return gzip.compress(pickled_response)
        else:
            return pickled_response

    def _deserialize_response(self, s_response):
        if self._compress:
            pickled_response = gzip.decompress(s_response)
        else:
            pickled_response = s_response
        return pickle.loads(pickled_response)

    def delete_cache(self, url):
        self._database.delete_response(url)

    def get_cached_response(self, url):
        return self._get_response(url)

    def sleep(self, secs):
        if not self._last_response_use_cache:
            time_now = time.time()
            time.sleep(max(secs - (time_now - self._last_response_time), 0))
