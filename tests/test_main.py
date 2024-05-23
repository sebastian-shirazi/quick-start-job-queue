from project.main import Queue


def test_enqueue_default():
    q = Queue()
    q = Queue()
    q.enqueue("123", "task")
    assert q.queue == [("123", "task", 10)]

def test_enqueue_priority():
    q = Queue()
    q.enqueue("123", "task", 5)
    assert q.queue == [("123", "task", 5)]

def test_dequeue():
    q = Queue()
    q.queue = [("123", "task", 5), ("456", "task2", 10)]
    assert ("123", "task", 5) == q.dequeue()
    assert q.queue == [("456", "task2", 10)]

def test_dequeue_empty():
    q = Queue()
    assert q.dequeue() == None

