import datetime

class Database:
    
    def __init__(self):
        self.entries = []

    def add_db(self, todo):
        self.entries.append(todo)
        print("\nToDo Successfully Added!")

    def edit_db(self, oldTodoIndex, newTodo):
        self.entries[oldTodoIndex] = newTodo
        print("\nToDo Successfully Edited!")

    def delete_db(self, todoIndex):
        self.entries.pop(todoIndex)
        print("\nToDo Successfully Deleted!")

    def getAll(self):
        return self.entries


class Manager:
    
    def __init__(self, database):
        self.database = database

    def add(self, todo, deadline):

        while True:
            try:
                deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
                break

            except ValueError:
                print("Invalid deadline format! Please enter a deadline in the format dd/mm/yyyy hh:mm")
                deadline = input("Deadline (dd/mm/yyyy hh:mm): ")
                continue
        
        if not todo.strip():
            print("Error: ToDo item can't be empty! Please enter a valid ToDo item")
            return
    
        todo = Todo(todo, deadline)
        self.database.add_db(todo)


    def edit(self, oldTodoIndex, newTodo):
        while True:
            deadline = input("New deadline (dd/mm/yyyy hh:mm): ")
            try:
                new_deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
                newTodo.deadline = new_deadline
                break

            except ValueError:
                print("Invalid deadline format! Please enter a deadline in the format dd/mm/yyyy hh:mm")
                

        self.database.edit_db(oldTodoIndex, newTodo)

    def delete(self, todoIndex):
        self.database.delete_db(todoIndex)

    def checkData(self):
        return len(self.database.getAll())

    def showAll(self):
        entries = self.database.getAll()

        for index, item in enumerate(entries, 1):
            if isinstance(item, Todo):
              print("\n")
              print("-" * 25 + str(index) + "-" * 25)
              print(item)
              print("-" * 51)


    def search(self, searchString):
        entries = self.database.getAll()
        results = []

        for index, item in enumerate(entries, 1):
            if isinstance(item, Todo) and searchString.lower() in item.text.lower():
                results.append((index, item))

        if results:
            print(f"\nFound {len(results)} matching ToDo items:")
            for index, item in results:
                print(f"\n-{index}-")
                print(item)
                print("-" * 51)
        else:
            print(f"No matching ToDo items found for '{searchString}'")

    def sort(self, sort_type):
        entries = self.database.getAll()

        if sort_type == "deadline":
            sorted_entries = sorted(entries, key=lambda item: item.deadline if isinstance(item, Todo) else None)
        elif sort_type == "date_added":
            sorted_entries = sorted(entries, key=lambda item: item.date if isinstance(item, Todo) else None)
        else:
            print(f"Unknown sort type '{sort_type}'")
            return

        self.database.entries = sorted_entries
        print(f"\nTo-Do list sorted by {sort_type}!")

class Todo:
    
    def __init__(self, text, deadline):
        self.text = text
        self.date = datetime.datetime.now()
        try:
            self.deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
        except ValueError:
            print("Error: Invalid deadline format! Please enter a deadline in the format dd/mm/yyyy hh:mm")
            self.deadline = None

    def __str__(self):
        if self.deadline:
            return f"Date: {self.date.strftime('%d/%m/%Y %H:%M')}\nToDo: {self.text}\nDeadline: {self.deadline.strftime('%d/%m/%Y %H:%M')}"
        else:
            return f"Date: {self.date.strftime('%d/%m/%Y %H:%M')}\nToDo: {self.text}\nDeadline: Invalid deadline format"


def menu():
    
    choice = None
    database = Database()
    manager = Manager(database)


    while choice != "q":
        print("\nToDo App Menu:")
        print("a) Add")
        print("e) Edit")
        print("d) Delete")
        print("s) Show All")
        print("q) Quit")

        choice = input("\nAction: ")


        if choice == "a":
            
            text = input("ToDo: ")
            deadline = input("Deadline (dd/mm/yyyy hh:mm): ")
            manager.add(text, deadline)


        elif choice == "e":
            
            if manager.checkData():
                
                manager.showAll()
                while True:
                    
                    todoIndex = input("Choose the index: ")
                    if not todoIndex.isdigit() or int(todoIndex) not in range(1, len(manager.database.entries)+1):
                         print("Error: Invalid index! Please enter a valid index")
                         continue

                    text = input("Enter the new text for the ToDo item: ")
                    deadline = input("Deadline (dd/mm/yyyy hh:mm): ")
                    newTodo = Todo(text, deadline)

                    oldTodoIndex = int(todoIndex) - 1

                    manager.edit(oldTodoIndex, newTodo)
                    break


            else:
                print("There is no DATA in DB!")

            

        elif choice == "d":
          if manager.checkData():
             manager.showAll()
             while True:
                 try:
                    todoIndex = int(input("Enter the index of the task to be deleted: "))
                    if todoIndex not in range(1, len(manager.database.entries)+1):
                       print("Error: Invalid index! Please enter a valid index")
                       continue
                    manager.delete(todoIndex-1)
                    break
                 except ValueError:
                    print("Error: Invalid index! Please enter a valid index")
                    continue
          else:
             print("There is no DATA in DB!")
 

        elif choice == "s":
            if manager.checkData():
               manager.showAll()
            else:
               print("There is no data in the database.")
               
         
        elif choice == "q":
            print("See you soon!")
            	
        else:
            print("Unknown command!")


menu()
