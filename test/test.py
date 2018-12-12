import unittest
import munin
import time


class TestMunin(unittest.TestCase):
    def setUp(self):
        self.session = munin.Session(":memory:")

    def test_simple(self):
        self.session.headers.update({"User-Agent": "test"})
        self.assertFalse(self.session.get("https://www.example.com").from_cache)
        self.assertTrue(self.session.get("https://www.example.com").from_cache)

    def test_cache(self):
        r = self.session.get("https://www.example.com")
        self.session.sleep(1)
        text = r.text
        start_time = time.time()
        for i in range(100):
            r = self.session.get("https://www.example.com")
            self.session.sleep(1)
            self.assertEqual(r.text, text)
        self.assertGreater(1, time.time() - start_time)

    def test_get_cache(self):
        r = self.session.get("https://www.example.com")
        self.session.sleep(1)
        text = r.text
        cached_r = self.session.get_cached_response("https://www.example.com")
        self.assertEqual(cached_r.text, text)

    def test_get_multi_cache(self):
        self.session.get("https://www.example.com")
        self.session.sleep(1)
        self.session.get("https://www.example.com", use_cache=False)
        caches = self.session.get_all_cached_response("https://www.example.com")
        self.assertEqual(2, len(caches))

    def tearDown(self):
        self.session.close()
