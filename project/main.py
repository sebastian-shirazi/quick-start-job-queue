import sys


class Queue:
    """An implemenation of a basic queue (FIFO)"""

    def __init__(self):
        self.queue = []
        self.choice = None
        self.sort_method = None
        self.DEFAULT_PRIORITY = 10

    def enqueue(self, uuid, name, priority=10):
        """
        Adds a job to the queue
        :param uuid: str: the unique identifier for the job
        :param name: str: the name of the job
        :param priority: int: the priority of the job
        """
        if int(priority) < 1:
            priority = self.DEFAULT_PRIORITY
        try:
            self.queue.append((uuid, name, int(priority)))
        except ValueError:
            print("Invalid type (priority must be an integer)")

    def dequeue(self):
        if self.queue:
            print("Running " + self.queue[0][1])
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
                print(f"Job {str(count + 1)}: {job}")
        else:
            print("Queue is empty!")

    def custom_sort(self):
        if(self.sort_method == "fifo"):
            return
        elif(self.sort_method == "lifo"):
            self.queue = self.queue[::-1]
            return self.queue
        elif(self.sort_method == "priority"):
            self.queue.sort(key=lambda x: x[2])
            return self.queue
        else:
            print("Invalid sort method, must choose one of the three options")
            self.prompt_sort()

    def add_task(self):
        uuid = input("Enter the UUID: ")
        name = input("Enter the name: ")
        priority = input("Enter the priority (default is 10): ")
        if not priority:
            self.enqueue(uuid, name)
        else:
            self.enqueue(uuid, name, priority)
        self.priotity_sort()
        print("Task added")


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
                        self.enqueue(line[0].strip(), line[1].strip(), line[2].strip())
                else:
                    print(f"Invalid job format - \"{line}\" - line skipped")

    def prompt_user(self):
        print(
            "Enter '1' to add a task, '2' to run a task, '3' to view the queue, '4' to exit"
        )
        self.choice = input().strip()
        return self.choice

    def prompt_sort(self):
        print(
            "How would you like the queue sorted? Enter 'FIFO' for first in first out, 'LIFO' for last in first out, or 'priority' for priority: "
            )
        self.sort_method = input().strip().lower()
        return self.sort_method

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
    q.prompt_sort()
    q.custom_sort()
    print("Queue created")
    q.prompt_user()
    while q.choice:
        q.handle_input()
    sys.exit()


if __name__ == "__main__":
    main()
