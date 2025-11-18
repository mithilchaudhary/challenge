# challenge

This folder contains a self-contained producer/consumer simulation. Everything
from the queue implementation to the CLI entry point lives right here. The
producer and consumer add a random 0–1 second pause before every queue action
and verbosely print the queue contents so you can watch the flow.

## Run the demo (repo root)

```pwsh
python producer_consumer/main.py
```

## Run the tests (repo root)

```pwsh
python -m pytest producer_consumer/tests
```

## Sample output

```text
Source items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[Producer] enqueued 1; queue=[1]
[Consumer] dequeued 1; queue=[]
[Producer] enqueued 2; queue=[2]
[Consumer] dequeued 2; queue=[]
[Producer] enqueued 3; queue=[3]
[Consumer] dequeued 3; queue=[]
[Consumer] dequeued 3; queue=[]
[Producer] enqueued 4; queue=[4]
[Consumer] dequeued 4; queue=[]
[Consumer] dequeued 4; queue=[]
[Producer] enqueued 5; queue=[5]
[Consumer] dequeued 5; queue=[]
[Producer] enqueued 6; queue=[6]
[Producer] enqueued 7; queue=[6, 7]
[Consumer] dequeued 5; queue=[]
[Producer] enqueued 6; queue=[6]
[Producer] enqueued 7; queue=[6, 7]
[Producer] enqueued 6; queue=[6]
[Producer] enqueued 7; queue=[6, 7]
[Producer] enqueued 7; queue=[6, 7]
[Producer] enqueued 8; queue=[6, 7, 8]
[Consumer] dequeued 6; queue=[7, 8]
[Producer] enqueued 9; queue=[7, 8, 9]
[Consumer] dequeued 7; queue=[8, 9]
[Producer] enqueued 10; queue=[8, 9, 10]
[Consumer] dequeued 8; queue=[9, 10]
[Producer] enqueued <object object at 0x0000022A90818480>; queue=[9, 10, <object object at 0x0000022A90818480>]
[Consumer] dequeued 9; queue=[10, <object object at 0x0000022A90818480>]
[Consumer] dequeued 10; queue=[<object object at 0x0000022A90818480>]
[Consumer] dequeued <object object at 0x0000022A90818480>; queue=[]
Drained items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Lists match: True
```

## Assumptions

- Exactly one producer thread feeds the queue and one consumer drains it.
- Each queue interaction sleeps for a random 0–1 seconds to make the flow visible.
- A unique sentinel object marks completion; it is enqueued after the final payload and the consumer exits as soon as it dequeues that marker.
- Logging is intentionally noisy so you can observe every enqueue/dequeue; tests also exercise the real logging/delay behavior.

## Looking ahead

A separate folder will host part 2 (CSV-based sales analytics with functional
style streams). Keeping this simulation isolated here lets each part evolve
independently.