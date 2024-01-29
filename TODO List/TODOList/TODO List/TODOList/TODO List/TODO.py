list = []

def addTask():
    task = input("Введите новую задачу: ")
    list.append(task)
    print("Задача успешно добавлена!")

def removeTask():
    if len(list) == 0:
        print("Список дел пуст.")
    else:
        print("Список дел:")
        for index, task in enumerate(list):
            print(f"{index + 1}. {task}")
        taskInd = int(input("Введите номер задачи для удаления: ")) - 1
        if taskInd < 0 or taskInd >= len(list):
            print("Неверный номер задачи.")
        else:
           deletedTask = list.pop(taskInd)
           print(f"Задача '{deletedTask}' успешно удалена.")

def viewTasks():
    if len(list) == 0:
        print("Список дел пуст.")
    else:
        print("Список дел:")
        for index, task in enumerate(list):
            print(f"{index + 1}. {task}")

def clear_list():
    list.clear()
    print("Список дел успешно очищен.")

def main():
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
            clear_list()
        elif choice == "5":
            break
        else:
            print("Неверный номер операции.")

main()