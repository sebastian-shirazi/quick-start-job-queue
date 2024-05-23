from project import main


def test_enqueue():
    q = main.Queue()
    q.enqueue("123", "task")
    assert q.queue == [("123", "task", 10)]
