# выводить время, когда была добавлена задача
import Store

Store.loadTasks(), Store.saveTasks()

todo_list = []


def addTask():
    task = input("Введите новую задачу: ")
    priority = input("Введите приоритет задачи (важный/обычный): ").lower()
    while priority.lower() not in ["важный", "обычный"]:
        print("Неверный приоритет. Попробуйте еще раз.")
        priority = input("Введите приоритет задачи (важный/обычный): ").lower()
    todo_list.append((task, priority))
    print("Задача успешно добавлена!")


def removeTask():
    if len(todo_list) == 0:
        print("Список дел пуст.")
    else:
        print("Список дел:")
        for index, task in enumerate(todo_list):
            print(f"{index + 1}. {task}")
        task_index = int(input("Введите номер задачи для удаления: ")) - 1
        if task_index < 0 or task_index >= len(todo_list):
            print("Неверный номер задачи.")
        else:
            deleted_task = todo_list.pop(task_index)
            print(f"Задача '{deleted_task}' успешно удалена.")


def sortTasks():
    todo_list.sort()
    print("Список задач отсортирован по алфавиту.")


def viewTasks():
    if len(todo_list) == 0:
        print("Список дел пуст.")
    else:
        print("Список дел:")
        important_tasks = []
        ordinary_tasks = []
        for task in todo_list:
            if task[1] == "важный":
                important_tasks.append(task[0])
            else:
                ordinary_tasks.append(task[0])
        if important_tasks:
            print("HIGH:")
            for index, task in enumerate(important_tasks):
                print(f"{index + 1}. {task}")
        if ordinary_tasks:
            print("LOW:")
            for index, task in enumerate(ordinary_tasks):
                print(f"{index + 1}. {task}")

            option = input("Для сортировки задач по алфавиту нажмите 's': ")
            if option.lower() == 's':
                sortTasks()
                print("Задачи отсортированы по алфавиту.")


def clearList():
    todo_list.clear()
    print("Список дел успешно очищен.")


def main():
    Store.loadTasks()
    while True:
        print("===============================")
        print("Меню:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Просмотреть список дел")
        print("4. Очистить список дел")
        print("5. Выйти")
        choice = input("Введите номер операции: ")
        print("===============================")

        if choice == "1":
            addTask()
        elif choice == "2":
            removeTask()
        elif choice == "3":
            viewTasks()
        elif choice == "4":
            clearList()
        elif choice == "5":
            break
        else:
            print("Неверный номер операции.")
        Store.saveTasks()


main()
