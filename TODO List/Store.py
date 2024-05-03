import json

todo_list = []


def saveTasks():
    with open("tasks.json", "w") as f:
        json.dump(todo_list, f)


def loadTasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            for task in data:
                todo_list.append(tuple(task))
    except FileNotFoundError:
        pass
