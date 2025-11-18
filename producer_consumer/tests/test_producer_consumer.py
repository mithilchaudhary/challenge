import sys
import time
from pathlib import Path
from threading import Event, Thread
import unittest

MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import main as pc 




class RunTransferTests(unittest.TestCase):
    def test_transfer_moves_all_items(self) -> None:
        print("Running: transfer moves all items")
        numbers = list(range(1, 6))
        result = pc.run_transfer(numbers, maxsize=2)
        self.assertEqual(result, numbers)

    def test_transfer_handles_empty_source(self) -> None:
        print("Running: transfer handles empty source")
        result = pc.run_transfer([], maxsize=2)
        self.assertEqual(result, [])


class ConsumerLifecycleTests(unittest.TestCase):
    def test_consumer_stops_on_sentinel(self) -> None:
        print("Running: consumer stops on sentinel")
        queue = pc.BlockingQueue(maxsize=3)
        destination: list[int] = []
        sentinel = object()
        consumer = pc.Consumer(queue, destination, sentinel)
        consumer.start()

        queue.put(42)
        queue.put(99)
        queue.put(sentinel)

        consumer.join(timeout=5)
        self.assertFalse(consumer.is_alive())
        self.assertEqual(destination, [42, 99])


class BlockingQueueTests(unittest.TestCase):
    def test_put_blocks_until_space_available(self) -> None:
        print("Running: queue blocks until space available")
        queue = pc.BlockingQueue(maxsize=1)
        first_put = Event()
        second_put = Event()

        def producer() -> None:
            queue.put(1)
            first_put.set()
            queue.put(2)
            second_put.set()

        worker = Thread(target=producer, daemon=True)
        worker.start()

        self.assertTrue(first_put.wait(timeout=1), "first put never happened")
        time.sleep(0.05)
        self.assertFalse(second_put.is_set(), "producer should block on a full queue")

        self.assertEqual(queue.get(), 1)
        self.assertTrue(second_put.wait(timeout=1), "producer failed to unblock after dequeue")
        self.assertEqual(queue.get(), 2)

        worker.join(timeout=1)
        self.assertFalse(worker.is_alive(), "worker thread did not finish")


if __name__ == "__main__":
    unittest.main()
