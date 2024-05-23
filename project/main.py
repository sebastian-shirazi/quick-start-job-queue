import sys


class Queue:
    """An implemenation of a basic queue (FIFO)"""

    def __init__(self):
        self.queue = []
        self.choice = None
        self.default_priority = 10

    def enqueue(self, uuid, name, priority=10):
        """
        Adds a job to the queue
        :param uuid: str: the unique identifier for the job
        :param name: str: the name of the job
        :param priority: int: the priority of the job
        """
        if int(priority) < 1:
            priority = self.default_priority
        try:
            self.queue.append((uuid, name, int(priority)))
            print("Task added")
        except ValueError:
            print("Invalid type (priority must be an integer)")
        self.queue.sort(key=lambda x: x[2])

    def dequeue(self):
        if self.queue:
            print("Running " + self.queue[0][0])
            return self.queue.pop(0)
        print("Queue is empty!")
        return None

    def peek(self):
        if self.queue:
            return self.queue[0]
        print("Queue is empty!")
        return None

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def print_queue(self):
        if not self.is_empty():
            for count, job in enumerate(self.queue):
                print("Job", str(count + 1) + ":", job)
        else:
            print("Queue is empty!")

    def add_task(self):
        uuid = input("Enter the UUID: ")
        name = input("Enter the name: ")
        priority = input("Enter the priority (default is 10): ")
        if not priority:
            self.enqueue(uuid, name)
        else:
            self.enqueue(uuid, name, priority)

    def run_task(self):
        self.dequeue()

    def get_queue(self):
        self.print_queue()

    def read_file(self, filepath):
        if "txt" not in filepath:
            raise FileNotFoundError(
                "Invalid file format - file not found or not a .txt file"
            )
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                if ",," not in line and line.count(",") == 2:
                    line = line.strip().split(",")
                    if line:
                        self.enqueue(line[0], line[1], line[2])
                else:
                    print(f"Invalid job format - \"{line}\" - line skipped")

    def prompt_user(self):
        print(
            "Enter '1' to add a task, '2' to run a task, '3' to view the queue, '4' to exit"
        )
        self.choice = input().strip()
        return self.choice

    def handle_input(self):
        options = {
            "1": self.add_task,
            "2": self.run_task,
            "3": self.get_queue,
            "4": sys.exit,
        }
        if self.choice not in options:
            print("Invalid choice")
            self.prompt_user()
            return
        options[self.choice]()
        self.prompt_user()


def main():
    q = Queue()
    filepath = input("Enter filepath: ")
    q.read_file(filepath)
    print("Queue created")
    q.prompt_user()
    while q.choice:
        q.handle_input()
    sys.exit()


if __name__ == "__main__":
    main()
