import time
import threading
from tests.integration import IntegrationTest
from parameterized import parameterized
from uuid import uuid4
from limits.storage import MemoryStorage
from limits.strategies import FixedWindowRateLimiter, MovingWindowRateLimiter
from limits.limits import RateLimitItemPerSecond

class ConcurrencyTests(IntegrationTest):
    def setUp(self):
        super(ConcurrencyTests, self).setUp()

    @parameterized.expand((k,) for k in range(100))
    def test_memory_storage_fixed_window(self, _):
        storage = MemoryStorage()
        limiter = FixedWindowRateLimiter(storage)
        per_second = RateLimitItemPerSecond(1000)

        [limiter.hit(per_second, uuid4().hex) for _ in range(1000)]

        key = uuid4().hex
        hits = []

        def hit():
            for i in range(1000):
                if limiter.hit(per_second, key):
                    hits.append(None)

        start = time.time()

        threads = [threading.Thread(target=hit) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]

        self.assertTrue(time.time() - start < 1)
        self.assertEqual(len(hits), 1000)

    @parameterized.expand((k,) for k in range(100))
    def test_memory_storage_moving_window(self, _):
        storage = MemoryStorage()
        limiter = MovingWindowRateLimiter(storage)
        per_second = RateLimitItemPerSecond(1000)

        [limiter.hit(per_second, uuid4().hex) for _ in range(1000)]

        key = uuid4().hex
        hits = []

        def hit():
            for i in range(1000):
                if limiter.hit(per_second, key):
                    hits.append(None)

        start = time.time()

        threads = [threading.Thread(target=hit) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]

        self.assertTrue(time.time() - start < 1)
        self.assertEqual(len(hits), 1000)

