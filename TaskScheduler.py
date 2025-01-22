from ADTs import MyQueue, Stack
from Task import Task
from Worker import Worker
from id_generator import id_generator


class TaskScheduler:
    def __init__(self):
        self.__tasks=Stack()
        self.__workers=MyQueue()
        self.__completed_tasks=Stack()


    def add_task(self, task):
        helper_stack = Stack()
        task_added = False

        while not self.__tasks.is_empty():
            current_task = self.__tasks.pop()

            if not task_added and (task.urgency > current_task.urgency or(task.urgency == current_task.urgency and task.importance > current_task.importance) or( task.urgency == current_task.urgency and task.importance == current_task.importance and task.time_window < current_task.time_window)):
                helper_stack.push(task)
                task_added = True

            helper_stack.push(current_task)

        if not task_added:
            helper_stack.push(task)

        while not helper_stack.is_empty():
            self.__tasks.push(helper_stack.pop())



    def add_worker(self, worker):
        if not isinstance(worker,Worker):
            raise TypeError("worker must to be from type Worker!")
        self.__workers.enqueue(worker)

    def allocate_task(self):
        if self.__tasks.is_empty():
            return

        task = self.__tasks.pop()
        task_allocated = False
        temp_worker_queue = MyQueue()

        while not self.__workers.is_empty():
            worker = self.__workers.dequeue()
            if not task_allocated and all(
                    skill in worker.get_skills() and worker.get_skills()[skill] >= task.needed_skills[skill] for skill
                    in task.needed_skills):
                if any(start <= task.time_window[0] and end >= task.time_window[1] for (start, end) in
                       worker.get_availability()):
                    self.__completed_tasks.push(task)
                    task_allocated = True
            temp_worker_queue.enqueue(worker)

        while not temp_worker_queue.is_empty():
            self.__workers.enqueue(temp_worker_queue.dequeue())

        if not task_allocated:
            self.__tasks.push(task)

    def add_another_task(self, task):
        self.__tasks.push(task)

    def update_task(self, task_id, **kwargs):
        helper_stack = Stack()
        found_task = None

        while not self.__tasks.is_empty():
            task = self.__tasks.pop()
            if task.get_task_id() == task_id:
                found_task = task
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                    else:
                        raise ValueError(f"Task does not have attribute '{key}'")
            helper_stack.push(task)

        while not helper_stack.is_empty():
            self.add_task(helper_stack.pop())

        if found_task is None:
            raise ValueError(f"Task with id {task_id} not found!")

    def __repr__(self):
        pass

    def completed_tasks_gen(self):
        temp_stack = Stack()
        helper_stack = Stack()

        while not self.__completed_tasks.is_empty():
            task = self.__completed_tasks.pop()
            temp_stack.push(task)
            helper_stack.push(task)

        while not temp_stack.is_empty():
            self.__completed_tasks.push(temp_stack.pop())

        copied_stack = Stack()
        while not helper_stack.is_empty():
            copied_stack.push(helper_stack.pop())

        while not copied_stack.is_empty():
            yield copied_stack.pop()

    def workers_gen(self):
        temp_queue = MyQueue()
        copied_queue = MyQueue()

        while not self.__workers.is_empty():
            worker = self.__workers.dequeue()
            temp_queue.enqueue(worker)
            copied_queue.enqueue(worker)

        while not temp_queue.is_empty():
            self.__workers.enqueue(temp_queue.dequeue())

        while not copied_queue.is_empty():
            yield copied_queue.dequeue()

    def undo_task(self):
        if self.__completed_tasks.is_empty():
            return print("No tasks to undo.")
        task = self.__completed_tasks.pop()
        self.add_task(task)

    def promote_senior(self):
        if self.__workers.is_empty():
            return

        most_senior = self.__workers.dequeue()
        most_senior.update_salary(1000)

        temp_queue = MyQueue()
        while not self.__workers.is_empty():
            temp_queue.enqueue(self.__workers.dequeue())

        while not temp_queue.is_empty():
            self.__workers.enqueue(temp_queue.dequeue())

        self.__workers.enqueue(most_senior)

    def yearly_update(self):
        if self.__workers.is_empty():
            return

        worker_list = []
        for _ in range(self.__workers.__len__()):
            worker = self.__workers.dequeue()
            skills = worker.get_skills()
            for skill in skills:
                skills[skill] += 1
            worker_list.append(worker)

        for worker in worker_list:
            self.__workers.enqueue(worker)

    def peek_task(self):
        if self.__tasks.is_empty():
            return "No tasks in waiting tasks."
        return self.__tasks.peek()

    def get_tasks(self):
        return self.__tasks


scheduler = TaskScheduler()
auto_worker_id_gen = id_generator(12)
auto_task_id_gen = id_generator(20)
# Add tasks
print("Adding tasks to the scheduler:")
task0 = Task(
    task_id=next(auto_task_id_gen),
    description="Task 0: Analyze data",
    urgency=5,
    importance=8,
    time_window=(9, 12),
    needed_skills={"Python": 3, "Data Analysis": 2}
)
task1 = Task(
    task_id=next(auto_task_id_gen),
    description="Task 1: Prepare report",
    urgency=2,
    importance=6,
    time_window=(18, 22),
    needed_skills={"Word Processing": 2}
)
task2 = Task(
    task_id=next(auto_task_id_gen),
    description="Task 2: Team presentation",
    urgency=4,
    importance=7,
    time_window=(10, 11),
    needed_skills={"Presentation Software": 1}
)
task3 = Task(
    task_id=next(auto_task_id_gen),
    description="Task 3: Analyze data",
    urgency=4,
    importance=7,
    time_window=(9, 12),
    needed_skills={"Presentation Software": 3, "Data Analysis": 2}
)

task4 = Task(
    task_id=next(auto_task_id_gen),
    description="Task 4: Analyze data",
    urgency=4,
    importance=8,
    time_window=(18, 20),
    needed_skills={"Java": 5, "Data Analysis v.2": 2}
)
scheduler.add_task(task0)
scheduler.add_task(task1)
scheduler.add_task(task2)
scheduler.add_task(task3)
scheduler.add_task(task4)

print(scheduler.get_tasks())

# Add workers
print("Adding workers to the scheduler:")
worker1 = Worker(
    worker_id=next(auto_worker_id_gen),
    name="Alice",
    skills={"Python": 5, "Data Analysis": 5, "Word Processing": 3},
    availability=[(9, 12), (14, 18)],
    salary=2000
)
worker2 = Worker(
    worker_id=next(auto_worker_id_gen),
    name="Bob",
    skills={"Presentation Software": 2, "Word Processing": 2},
    availability=[(10, 12), (14, 16)],
    salary=20000
)
worker3 = Worker(
    worker_id=next(auto_worker_id_gen),
    name="Jennifer",
    skills={'Data Analysis v.2': 2, "Java": 7},
    availability=[(6, 12), (14, 18)],
    salary=25000
)
scheduler.add_worker(worker1)
scheduler.add_worker(worker2)
scheduler.add_worker(worker3)
worker_gen = scheduler.workers_gen()
for worker in worker_gen:
    print(worker)

# Allocate tasks
print("Allocating tasks to workers:")
scheduler.allocate_task()
scheduler.allocate_task()
scheduler.allocate_task()
print(f"Completed tasks: {[task.description for task in scheduler.completed_tasks_gen()]}")
print()

# Update a task
print("Updating a task...")
try:
    scheduler.update_task(task1.get_task_id(), urgency=10)
    print("Updating ended successfully.")
except Exception as e:
    print(e)
    print(f"Updated Task: {task1}")
    print()

# Generate completed tasks
print("Iterating through completed tasks:")
for completed_task in scheduler.completed_tasks_gen():
    print(completed_task)

print("Iterating through completed tasks post undo task:")
scheduler.undo_task()
for completed_task in scheduler.completed_tasks_gen():
    print(completed_task)

print("Undo another task")
scheduler.undo_task()
for completed_task in scheduler.completed_tasks_gen():
    print(completed_task)

print("Promoting senior....")
scheduler.promote_senior()
worker_gen = scheduler.workers_gen()
for worker in worker_gen:
    print(worker)

print("Yearly updating all workers....")
scheduler.yearly_update()
worker_gen = scheduler.workers_gen()
for worker in worker_gen:
    print(worker)

print(scheduler.peek_task())