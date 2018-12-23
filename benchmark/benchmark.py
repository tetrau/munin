import munin
import requests
import itertools
import os
import time

TEST_URL = "https://github.com/tetrau/munin"
TEST_SIZE = (0, 100, 1000)
TEST_DATABASE = "test.db"

response = requests.get(TEST_URL)

print("web page size: {} KiB".format(len(response.content) // 1024))


def display_config(c):
    s = []
    for k, v in sorted(c.items()):
        s.append("{}={}".format(k, v))
    return ", ".join(s)


configs = ("compress", "index", "synchronous")

for _config in itertools.product((True, False), repeat=len(configs)):
    config = dict(zip(configs, _config))
    session = munin.Session(TEST_DATABASE, **config)
    pickle_size = len(session._serialize_response(response))
    insert_timestamps = [time.time()]
    for idx, size in enumerate(TEST_SIZE[:-1]):
        next_size = TEST_SIZE[idx + 1]
        for i in range(size, next_size):
            session._put_response(TEST_URL + "/" + str(i), response)
        insert_timestamps.append(time.time())
    print("configuration:", display_config(config))
    for idx_1, size in enumerate(TEST_SIZE[1:]):
        print("{:0.6} response/s for {} write".format(size / (insert_timestamps[idx_1 + 1] - insert_timestamps[0]),
                                                      size))

    get_timestamps = [time.time()]
    for idx, size in enumerate(TEST_SIZE[:-1]):
        next_size = TEST_SIZE[idx + 1]
        for i in range(size, next_size):
            session.get(TEST_URL + "/" + str(i))
        get_timestamps.append(time.time())
    for idx_1, size in enumerate(TEST_SIZE[1:]):
        print("{:0.6} response/s for {} read".format(size / (get_timestamps[idx_1 + 1] - get_timestamps[0]),
                                                     size))
    print('database size {:.6} MiB'.format(os.path.getsize(TEST_DATABASE) / 1024 / 1024))
    os.remove(TEST_DATABASE)
    print()
