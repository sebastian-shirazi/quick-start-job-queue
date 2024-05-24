from project.main import Queue


def test_can_enqueue_a_job_defualt_priority():
    q = Queue()
    q.enqueue("123", "task")
    assert q.queue == [("123", "task", 10)]

def test_can_enqueue_a_job():
    q = Queue()
    q.enqueue("123", "task", 5)
    assert q.queue == [("123", "task", 5)]

def test_can_dequeue_a_queued_job():
    q = Queue()
    q.queue = [("123", "task", 5), ("456", "task2", 10)]
    assert ("123", "task", 5) == q.dequeue()
    assert q.queue == [("456", "task2", 10)]

def test_priority_jobs_are_dequeued_first():
    pass

def test_dequeue_on_empty_queue_returns_none():
    q = Queue()
    assert q.dequeue() == None

def test_can_list_jobs_in_queue():
    q = Queue()
    q.queue = [("123", "task", 5), ("456", "task2", 10)]
    assert q.get_queue() == print(f"Job 1: {q.queue[0]}\nJob 2: {q.queue[1]}")

def test_can_read_jobs_from_file():
    q = Queue()
    q.read_file("project/sample.txt")
    assert q.queue == [('c8fd914b-8339-4ea0-907a-dc685a8f4758', 'Task 5', 2),
        ('eda49cfe-c2f5-49f7-917d-ffc3d3111e63', 'Task 4', 3),
        ('8b0f47f2-a833-4f12-bc9e-096e49c015ad', 'Task 3', 2),
        ('5cb139e2-2344-4ede-aa4c-4ec1e940ab28', 'Task 2', 1),
        ('b0293ea7-f8bc-4c3a-af5e-9b1d858ed18a', 'Task 1', 3),
    ]

def test_throws_error_when_file_not_found():
    q = Queue()
    try:
        q.read_file("Sample.csv")
    except FileNotFoundError as err:
        assert str(err) == "Invalid file format - file not found or not a .txt file"

def test_can_sort_queue_fifo_from_file():
    q = Queue()
    q.read_file("project/sample.txt")
    q.sort_method = "fifo"
    q.custom_sort()
    assert q.queue == [('b0293ea7-f8bc-4c3a-af5e-9b1d858ed18a', 'Task 1', 3),
        ('5cb139e2-2344-4ede-aa4c-4ec1e940ab28', 'Task 2', 1),
        ('8b0f47f2-a833-4f12-bc9e-096e49c015ad', 'Task 3', 2),
        ('eda49cfe-c2f5-49f7-917d-ffc3d3111e63', 'Task 4', 3),
        ('c8fd914b-8339-4ea0-907a-dc685a8f4758', 'Task 5', 2),
        ]

def test_can_sort_queue_lifo_from_file():
    q = Queue()
    q.read_file("project/sample.txt")
    q.sort_method = "lifo"
    q.custom_sort()
    assert q.queue == [('c8fd914b-8339-4ea0-907a-dc685a8f4758', 'Task 5', 2),
        ('eda49cfe-c2f5-49f7-917d-ffc3d3111e63', 'Task 4', 3),
        ('8b0f47f2-a833-4f12-bc9e-096e49c015ad', 'Task 3', 2),
        ('5cb139e2-2344-4ede-aa4c-4ec1e940ab28', 'Task 2', 1),
        ('b0293ea7-f8bc-4c3a-af5e-9b1d858ed18a', 'Task 1', 3),
        ]

def test_can_sort_queue_priority_from_file():
    q = Queue()
    q.read_file("project/sample.txt")
    q.sort_method = "priority"
    q.custom_sort()
    assert q.queue == [('5cb139e2-2344-4ede-aa4c-4ec1e940ab28', 'Task 2', 1),
        ('c8fd914b-8339-4ea0-907a-dc685a8f4758', 'Task 5', 2),
        ('8b0f47f2-a833-4f12-bc9e-096e49c015ad', 'Task 3', 2),
        ('eda49cfe-c2f5-49f7-917d-ffc3d3111e63', 'Task 4', 3),
        ('b0293ea7-f8bc-4c3a-af5e-9b1d858ed18a', 'Task 1', 3),
        ]


