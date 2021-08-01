import datetime
import json

STATUSES = ['new', 'in progress', 'done']
PRIORITIES = ['low', 'normal', 'high']


class Task:
    id: int
    description: str
    deadline: datetime
    status: str
    priority: str

    def __init__(self):
        description = input('Print description: ')
        self.description = description
        date_ok = False
        while not date_ok:
            try:
                deadlineStr = input('Print deadline date (dd/mm/yyyy): ')
                # parse str to datetime strptime
                deadline = datetime.datetime.strptime(deadlineStr, "%d/%m/%Y")
                if deadline >= datetime.datetime.today():
                    date_ok = True
                    self.deadline = deadline.isoformat()
            except:
                print('error in parsing')
        # while
        priority_ok = False
        while not priority_ok:
            priority = input("Choose priority['low', 'normal', 'high']: ")
            if priority in PRIORITIES:
                self.priority = priority
                priority_ok = True
            else:
                print('incorrect value entered')
        self.status = 'new'
        self.id = 0

    def __str__(self):
        pass

    @staticmethod
    def change_priority(file_name):
        priority_ok = False
        while not priority_ok:
            pr = input(f'Choose new priority {PRIORITIES}: ')
            if pr in PRIORITIES:
                tasks = Task.read_tasks(file_name)
                id = int(input('enter task id'))
                for task in tasks:
                    if task['id'] == id:
                        task['priority'] = pr
                        priority_ok = True
                        print(f'task {task["id"]} priority changed')
                Task.write_tasks(file_name, tasks)
            else:
                print('incorrect value entered')
        # validation

    @staticmethod
    def change_status(file_name):
        status_ok = False
        while not status_ok:
            st = input(f'Choose new status {STATUSES}: ')
            if st in STATUSES:
                tasks = Task.read_tasks(file_name)
                id = int(input('enter task id'))
                for task in tasks:
                    if task['id'] == id:
                        task['status'] = st
                        status_ok = True
                        print(f'task {task["id"]} status changed')
                Task.write_tasks(file_name, tasks)
            else:
                print('incorrect value entered')

    @staticmethod
    def change_deadline(file_name):
        date_ok = False
        while not date_ok:
            try:
                deadlinestr = input('Print deadline date (dd/mm/yyyy): ')
                # parse str to datetime strptime
                deadline = datetime.datetime.strptime(deadlinestr, "%d/%m/%Y")
                if deadline >= datetime.datetime.today():
                    tasks = Task.read_tasks(file_name)
                    id = int(input('enter task id'))
                    for task in tasks:
                        if task['id'] == id:
                            date_ok = True
                            task['deadline'] = deadline.isoformat()
                            print(f'task {task["id"]} deadline changed')
                    Task.write_tasks(file_name, tasks)
            except:
                print('error in parsing')

    @staticmethod
    def close_task(file_name):
        close_yes = False
        id = int(input('enter task id'))
        tasks = Task.read_tasks(file_name)
        for task in tasks:
            if task['id'] == id:
                task['status'] = 'done'
                close_yes = True
        if close_yes == True:
            Task.write_tasks(file_name, tasks)
            print(f'task {id} closed')
        else:
            print('task not found')

    @staticmethod
    def find_task(file_name):
        foundTask = []
        id = int(input('enter task id'))
        tasks = Task.read_tasks(file_name)
        for task in tasks:
            if task['id'] == id:
                foundTask.append(task)
        return foundTask

    @staticmethod
    def read_tasks(file_name):
        try:
            with open(file_name, 'r') as tasks_file:
                tasks = json.load(tasks_file)
        except:
            tasks = []
        return tasks

    @staticmethod
    def find_lastID(file_name):
        lastID = 0
        try:
            with open(file_name, 'r') as tasks_file:
                tasks = json.load(tasks_file)
                for task in tasks:
                    if lastID < task['id']:
                        lastID = task['id']
        except:
            return lastID
        return lastID + 1

    @staticmethod
    def app_task(file_name):
        task = Task().__dict__
        lastID = Task.find_lastID(file_name)
        task['id'] = lastID
        tasks = Task.read_tasks(file_name)
        tasks.append(task)
        Task.write_tasks(file_name, tasks)

    @staticmethod
    def write_tasks(file_name, tasks):
        with open(file_name, 'w') as tasks_file:
            json.dump(tasks, tasks_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    file_name = 'tasks.json'
    while True:
        Command = input('Enter the command'
                        '\n"a"- print tasks'
                        '\n"b"- adding a task'
                        '\n"c" - close the task'
                        '\n"d" - find a task by id'
                        '\n"ch_priority" - change priority'
                        '\n"ch_status" - change status'
                        '\n"ch_deadline" - change deadline'
                        '\n"exit" -to finish work')
        # вывод задач
        if Command == 'a':
            tasks = Task.read_tasks(file_name)
            for task in tasks:
                print(task)
        # добавление задачи
        elif Command == 'b':
            Task.app_task(file_name)
        # закрытие задачи
        elif Command == 'c':
            Task.close_task(file_name)
        # поиск задачи по id
        elif Command == 'd':
            print(Task.find_task(file_name))
        # изменение приоритета
        elif Command == 'ch_priority':
            Task.change_priority(file_name)
        # изменение статуса
        elif Command == 'ch_status':
            Task.change_status(file_name)
        # изменение даты дедлайна
        elif Command == 'ch_deadline':
            Task.change_deadline(file_name)
        # завершение
        elif Command == 'exit':
            break


"""
1. добить инициализацию и валидацию
2. change_priority, change_status, change_deadline, close_task - доделать
3. протестить чтение/запись файла
4*. реализаовать цикл для работы с пользователем через консоль "while True:"
    а) вывод задач
    б) добавление задачи
    г) закрытие задачи
    д) вывод одной задачи по id 
"""
