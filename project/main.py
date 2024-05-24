import sys


class Queue:
    """A class that represents a job queue"""

    def __init__(self):
        self.queue = []
        self.choice = None
        self.sort_method = None
        self.DEFAULT_PRIORITY = 10

    def enqueue(self, uuid, name, order, priority=10):
        """
        Adds a job to the queue based on the sort method
        :param uuid: str: the unique identifier for the job
        :param name: str: the name of the job
        :param priority: int: the priority of the job
        """
        if int(priority) < 1:
            priority = self.DEFAULT_PRIORITY
        try:
            self.queue.append((uuid, name, int(priority), order))
        except ValueError:
            print("Invalid type (priority must be an integer)")

    def dequeue(self):
        """Removes the job from the front of the queue if present, otherwise prints message"""
        if not self.is_empty():
            print("Running " + self.queue[0][1])
            return self.queue.pop(0)
        print("Queue is empty!")
        return None

    def peek(self):
        """Returns the job at the front of the queue if present, otherwise prints message"""
        if not self.is_empty():
            return self.queue[0]
        print("Queue is empty!")
        return None

    def size(self):
        """Returns the number of jobs in the queue"""
        return len(self.queue)

    def is_empty(self):
        """Returns True if the queue is empty, otherwise False"""
        return len(self.queue) == 0

    def print_queue(self):
        """Prints the jobs in the queue"""
        if not self.is_empty():
            for count, job in enumerate(self.queue):
                print(f"No. {str(count + 1)}: {job[0]}, {job[1]} - Priority: {job[2]}")
        else:
            print("Queue is empty!")

    def custom_sort(self):
        """Sorts the queue based on the sort method passed in by user"""
        if self.sort_method == "fifo":
            self.queue.sort(key=lambda x: x[3])
        if self.sort_method == "lifo":
            self.queue.sort(key=lambda x: x[3], reverse=True)
        if self.sort_method == "priority":
            self.queue.sort(key=lambda x: (x[2], x[3]))

    def add_task(self):
        """Prompts the user to enter a UUID, name, and priority for a job
        and adds it to the queue, resorts if it is a priority queue"""
        uuid = input("Enter the UUID: ")
        name = input("Enter the name: ")
        priority = input("Enter the priority (default is 10): ")
        if not priority:
            self.enqueue(uuid, name, self.size() + 1)
        else:
            if priority.isdigit():
                self.enqueue(uuid, name, self.size() + 1, priority)
            else:
                print("Invalid priority - must be an integer")
                self.add_task()
        self.custom_sort()
        print("Task added")


    def run_task(self):
        """Wrapper method for running tasks in the queue"""
        self.dequeue()

    def get_queue(self):
        """Wrapper method for accessing the queue"""
        self.print_queue()

    def read_file(self, filepath):
        """
        Reads a file and adds the jobs to the queue by parsing lines of file
        :param filepath: str: the path to the file to be read (or name if in root directory)
        """

        if "txt" not in filepath:
            raise FileNotFoundError(
                "Invalid file format - file not found or not a .txt file"
            )
        with open(filepath, "r", encoding="utf-8") as file:
            for order, line in enumerate(file, 1):
                if ",," not in line and line.count(",") == 2:
                    line = line.strip().split(",")
                    if line:
                        self.enqueue(line[0].strip("\'").strip(),
                                    line[1].strip("\'").strip(),
                                    order,
                                    line[2].strip())
                else:
                    print(f"Invalid job format - \"{line}\" - line skipped")

    def prompt_choice_select(self):
        """Prompts the user to enter a choice to add a task,
        run a task, view the queue, or exit the program"""
        print(
            "Enter '1' to add a task, '2' to run a task, '3' to view the queue, '4' to change the sorting of the queue, '5' to exit"
        )
        self.choice = input().strip()
        return self.choice

    def prompt_sort_select(self):
        """Prompts the user to enter a sort method for the queue"""
        print(
            "How would you like the queue sorted? Enter 'FIFO' for first in first out, 'LIFO' for last in first out, or 'priority' for priority: "
            )
        self.sort_method = input().strip().lower()
        if self.sort_method not in ["fifo", "lifo", "priority"]:
            print("Invalid sort method")
            self.prompt_sort_select()
        else:
            print(f"Queue will be sorted by {self.sort_method.upper()}")
            self.custom_sort()
        return self.sort_method

    def handle_input(self):
        """Handles the user input by calling the appropriate method based on the choice"""
        options = {
            "1": self.add_task,
            "2": self.run_task,
            "3": self.get_queue,
            "4": self.prompt_sort_select,
            "5": sys.exit,
        }
        if self.choice in options:
            options[self.choice]()
        else:
            print("Invalid choice")
        self.prompt_choice_select()


def main():
    """Main function to run the program"""
    q = Queue()
    filepath = input("Enter filepath: ")
    q.read_file(filepath)
    while not q.sort_method:
        q.prompt_sort_select()
    print("Queue created")
    q.prompt_choice_select()
    while q.choice:
        q.handle_input()
    sys.exit()


if __name__ == "__main__":
    main()
