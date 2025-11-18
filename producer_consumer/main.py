import random
import time
from collections import deque
from threading import Condition, Thread
from typing import Deque, Iterable, List, Sequence


class BlockingQueue:
    """Simple bounded queue with condition-based blocking semantics."""

    def __init__(self, maxsize: int = 5) -> None:
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self._maxsize = maxsize
        self._queue: Deque[object] = deque()
        self._cond = Condition()

    def put(self, item: object, *, actor: str = "Producer") -> None:
        with self._cond:
            while len(self._queue) >= self._maxsize:
                self._cond.wait()
            self._queue.append(item)
            print(f"[{actor}] enqueued {item}; queue={list(self._queue)}")
            self._cond.notify_all()

    def get(self, *, actor: str = "Consumer") -> object:
        with self._cond:
            while not self._queue:
                self._cond.wait()
            item = self._queue.popleft()
            print(f"[{actor}] dequeued {item}; queue={list(self._queue)}")
            self._cond.notify_all()
            return item

    def size(self) -> int:
        with self._cond:
            return len(self._queue)


class Producer(Thread):
    """Feeds items from the source container into the queue."""

    def __init__(self, source: Sequence[int], queue: BlockingQueue, sentinel: object) -> None:
        super().__init__(daemon=True, name="Producer")
        self._source = list(source)
        self._queue = queue
        self._sentinel = sentinel

    def run(self) -> None:
        for item in self._source:
            time.sleep(random.uniform(0, 1))
            self._queue.put(item, actor=self.name)
        time.sleep(random.uniform(0, 1))
        self._queue.put(self._sentinel, actor=self.name)


class Consumer(Thread):
    """Drains items from the queue into the destination container."""

    def __init__(self, queue: BlockingQueue, destination: List[int], sentinel: object) -> None:
        super().__init__(daemon=True, name="Consumer")
        self._queue = queue
        self._destination = destination
        self._sentinel = sentinel

    def run(self) -> None:
        while True:
            time.sleep(random.uniform(0, 1))
            item = self._queue.get(actor=self.name)
            if item == self._sentinel:
                break
            self._destination.append(item)


def run_transfer(source: Iterable[int], maxsize: int = 5) -> List[int]:
    """Helper that wires the producer and consumer and returns the drained values."""

    data = list(source)
    destination: List[int] = []
    sentinel = object()
    queue = BlockingQueue(maxsize=maxsize)

    producer = Producer(data, queue, sentinel)
    consumer = Consumer(queue, destination, sentinel)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    return destination


def main() -> None:
    numbers = list(range(1, 11))
    print("Source items:", numbers)
    drained = run_transfer(numbers, maxsize=3)
    print("Drained items:", drained)
    print("Lists match:", numbers == drained)


if __name__ == "__main__":
    main()
