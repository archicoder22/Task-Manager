# this program helps to manage tasks assigned to each member of the team

# ===== importing libraries =====
import datetime
import os

# ===== global variables =====
usernames_list = []
passwords_list = []

YELLOW = '\033[93m'
PINK = '\033[91m'
WHITE = '\033[0m'
BOLD = '\033[1m'


# ===== function definitions =====

# define a function that registers a new user
def reg_user():
    new_user = input("\nPlease enter a new username:")  # request a new username

    while new_user in usernames_list:  # check if the username exists
        new_user = input("This user already exists. Please choose different username:")

    new_password = input("Please enter a new password:")  # request a password for the new user
    new_password_check = input("Please confirm a new password:")  # request a password confirmation

    while new_password != new_password_check:  # check if new password and confirmation match
        new_password = input("Passwords do not match. Please re-type a new password:")
        new_password_check = input("Please confirm a new password:")

    if new_password == new_password_check:
        with open("user.txt", "a", encoding="utf-8") as new_user_data:  # add username to the file "user.txt"
            new_user_data.write(f"\n{new_user}, {new_password}")
        usernames_list.append(new_user)  # add username to username list

    print(f"\nNew user {PINK}{BOLD}{new_user}{WHITE} registered successfully!")


# define a function that adds a new task
def add_task():
    n_task_user = input("\nWhich user this task will be assigned to:")

    while n_task_user not in usernames_list:  # check if username exists
        n_task_user = input("This username does not exist. Please type the username again:")

    n_task_title = input("What is the title of the new task?")
    n_task_descr = input("Please type a new task description:")
    n_task_assign_date = datetime.datetime.now().strftime("%d %b %Y")
    n_task_due_date = input("What is the due date for the new task? (dd mmm yyyy)")

    while True:  # check if the given date is in the correct format
        try:
            datetime.datetime.strptime(n_task_due_date, "%d %b %Y")
            break
        except ValueError:
            n_task_due_date = input("Wrong format, enter again.")

    with open("tasks.txt", "a", encoding="utf-8") as tasks:  # write a new task details to the file "tasks.txt"
        tasks.write(f"\n{n_task_user}, {n_task_title}, {n_task_descr}, {n_task_assign_date}, {n_task_due_date}, No")

    print(f"\n{YELLOW}New task added successfully!{WHITE}")


# define function that reads from file and returns a list of tasks
def task_read():
    all_tasks_list = []

    with open("tasks.txt", "r", encoding="utf-8") as all_tasks_data:  # read data from "tasks.txt"
        all_tasks_read = all_tasks_data.readlines()

    for task_line in all_tasks_read:  # place all tasks in the list
        all_split_data = task_line.strip("\n").split(", ")
        all_tasks_list.append(all_split_data)

    return all_tasks_list


# define a function that reads from file displays details of all tasks
def view_all():
    with open("tasks.txt", "r", encoding="utf-8") as all_tasks_data:  # read data from "tasks.txt"
        all_tasks_read = all_tasks_data.readlines()

    for all_lines in all_tasks_read:  # display all tasks details
        all_lines_data = all_lines.split(", ")
        all_output = "\n"
        all_output += f"{YELLOW}Task:               {WHITE}{all_lines_data[1]}\n"
        all_output += f"{YELLOW}Task Description:   {WHITE}{all_lines_data[2]}\n"
        all_output += f"{YELLOW}Assigned to:        {WHITE}{all_lines_data[0]}\n"
        all_output += f"{YELLOW}Assignment Date:    {WHITE}{all_lines_data[3]}\n"
        all_output += f"{YELLOW}Due Date:           {WHITE}{all_lines_data[4]}\n"
        all_output += f"{YELLOW}Task Complete?      {WHITE}{all_lines_data[5]}"

        print(all_output)


# define a function that reads from file and displays details of all tasks assigned to signed-in user
def view_mine():
    task_list = task_read()
    user_task_list = []
    task_counter = 0
    task_mod_num = "-1"

    for i in range(len(task_list)):  # place user's tasks in a separate list, include task numbers
        if task_list[i][0] == username:
            task_counter += 1
            user_task_list.append([str(task_counter)] + task_list[i])
            task_list[i].insert(0, str(task_counter))

    if task_counter == 0:  # check if there are any tasks registered to the user
        print(f"There are no tasks registered to user {PINK}{username}{WHITE}.")
    else:
        print(f"\n{YELLOW}Tasks assigned to user {PINK}{username}{WHITE}\n")

        for i in range(len(user_task_list)):  # display user's tasks data
            print(f"{YELLOW}Task number:               {WHITE}{user_task_list[i][0]}\n"
                  f"{YELLOW}Task:                      {WHITE}{user_task_list[i][2]}\n"
                  f"{YELLOW}Task Description:          {WHITE}{user_task_list[i][3]}\n"
                  f"{YELLOW}Assignment Date:           {WHITE}{user_task_list[i][4]}\n"
                  f"{YELLOW}Due Date:                  {WHITE}{user_task_list[i][5]}\n"
                  f"{YELLOW}Task Complete?             {WHITE}{user_task_list[i][6]}\n")

        task_mod_num = input(f"Select {PINK}task number{WHITE} to modify.\n"  # next step selection
                             f"Type \"{PINK}-1{WHITE}\" to return to the main menu.")

    task_mod(task_list, user_task_list, task_mod_num, task_counter)


# define a function that allows task modification
def task_mod(all_tasks, user_tasks, task, counter):
    task_list = all_tasks
    user_t_list = user_tasks
    task_mod_num = task
    task_counter = counter

    while True:
        if task_mod_num == "-1":  # return to the main menu
            break
        elif int(task_mod_num) in range(1, task_counter + 1):  # task number chosen
            while True:
                if user_t_list[int(task_mod_num) - 1][-1] == "Yes":  # check if task is completed
                    task_mod_num = input("This task is completed, choose another one:")
                else:
                    choice = input("\"c\" to complete or \"m\" to modify user")  # next step choice
                    break
            while True:
                if choice == "c":  # mark task as complete
                    for i in range(len(task_list)):
                        if task_list[i][0] == task_mod_num:
                            task_list[i][-1] = "Yes"
                            task_list[i].pop(0)
                    break
                elif choice == "m":  # modify task
                    mod_step = input("\"u\" for user or \"d\" for date:")
                    while True:
                        if mod_step == "u":  # assign different user to the task
                            new_user = input("Which username to assign this task to?")
                            while not new_user in usernames_list:  # check if username exists
                                new_user = input("You typed incorrect username. Please enter a correct username:")
                            for i in range(len(task_list)):
                                if task_list[i][0] == task_mod_num:
                                    task_list[i][1] = new_user  # change user
                                    task_list[i].pop(0)  # remove task number
                            print("User changed successfully.")
                            break
                        elif mod_step == "d":  # modify tasks date
                            new_date = input(f"What is the new due date for the task {task_mod_num}? "
                                             f"Enter a date in the format DD MMM YYYY")
                            while True:  # check if date is in the correct format
                                try:
                                    datetime.datetime.strptime(new_date, "%d %b %Y")
                                    break
                                except ValueError:
                                    new_date = input("Wrong format, enter again.")

                            for i in range(len(task_list)):  # update date in the tasks list
                                if task_list[i][0] == task_mod_num:
                                    task_list[i][-2] = new_date
                            print(f"\n{YELLOW}Date updated successfully.{WHITE}")
                            break
                        else:
                            mod_step = input("try again")
                    break
                else:
                    choice = input("Incorrect, choose again")
            break
        else:
            task_mod_num = input("Incorrect entry, please choose one of user's tasks.")

    for i in range(len(task_list)):  # remove all task numbers assigned for manipulation
        for j in range(1, task_counter + 1):
            if task_list[i][0] == str(j):
                task_list[i].pop(0)

    with open("tasks.txt", "w", encoding="utf-8") as all_tasks_data:  # update "tasks.txt" file
        for i in range(len(task_list)):
            all_tasks_string = ", ".join(task_list[i]) + "\n"
            all_tasks_data.write(all_tasks_string)

    return task_list


# define a function writing a task overview to the file
def task_overview():
    t_list = task_read()
    t_total = 0
    t_completed = 0
    t_over_uncompleted = 0

    for i in range(len(t_list)):
        t_total += 1
        if t_list[i][-1] == "Yes":
            t_completed += 1

    t_uncompleted = t_total - t_completed
    perc_uncompleted = round(t_uncompleted / t_total * 100, 2)

    for i in range(len(t_list)):  # check if the date is in the correct format
        due_date = datetime.datetime.strptime(t_list[i][-2], "%d %b %Y")
        curr_date = datetime.datetime.today()

        if due_date < curr_date and t_list[i][-1] == "No":
            t_over_uncompleted += 1

    perc_over_uncompleted = round(t_over_uncompleted / t_total * 100, 2)

    with open("task_overview.txt", "w", encoding="utf-8") as t_overview:  # write task overview to the file
        output = (f"Total number of tasks:               {t_total}\n"
                  f"Total number of completed tasks:     {t_completed}\n"
                  f"Total number of uncompleted tasks:   {t_uncompleted}\n"
                  f"Total number of overdue uncompleted: {t_over_uncompleted}\n"
                  f"Percentage of uncompleted tasks:     {perc_uncompleted}%\n"
                  f"Percentage of overdue:               {perc_over_uncompleted}%\n")

        t_overview.write(output)


# define a function writing user's overview to the file
def user_overview():
    tasks_list = task_read()
    users_list = []
    users_total = 0
    output = ""

    for i in range(len(tasks_list)):  # count users
        if tasks_list[i][0] not in users_list:
            users_list.append(tasks_list[i][0])
            users_total += 1

    tasks_total = len(tasks_list)  # create a list with the length equal to number of users
    users_tasks_list = [[] for x in range(users_total)]

    for i in range(len(tasks_list)):
        for j in range(len(users_list)):
            if tasks_list[i][0] == users_list[j]:
                users_tasks_list[j].append(tasks_list[i])  # add user's tasks to the list

    for j in range(len(users_list)):
        user_name = users_list[j]
        user_completed = 0
        user_over = 0
        user_t_num = len(users_tasks_list[j])
        output += f"Total number of tasks for user {user_name} is {user_t_num}.\n"
        output += f"User {user_name} is assigned {round((user_t_num / tasks_total * 100), 2)} % of all tasks.\n"

        for m in range(len(users_tasks_list[j])):

            if users_tasks_list[j][m][-1] == "Yes":
                user_completed += 1
                user_over = 0
                due_date = datetime.datetime.strptime(users_tasks_list[j][m][-2], "%d %b %Y")
                curr_date = datetime.datetime.today()

                if due_date < curr_date and users_tasks_list[j][m][-1] == "No":
                    user_over += 1

        user_over_uncompl_perc = user_over / user_t_num * 100
        user_perc_compl = round(user_completed / user_t_num * 100, 2)

        output += f"User {user_name} completed {user_perc_compl} % of their tasks.\n"
        output += f"{100 - user_perc_compl}% of {user_name}'s tasks must still be completed.\n"
        output += f"{user_over_uncompl_perc}% of {user_name}'s uncompleted tasks are overdue.\n" \
                  f"\n"

    with open("user_overview.txt", "w", encoding="utf-8") as u_overview:  # write user overview to the file
        u_overview.write(output)


# define a function that displays statistics of all tasks
def display_stat():
    path_user = "./user_overview.txt"
    path_task = "./task_overview.txt"

    # check if "user_overview.txt" file exists
    if os.path.isfile(path_user):
        read_user_overview()  # display user data
    else:
        user_overview()  # generate and display user data
        read_user_overview()

    # check if "task_overview.txt" file exists
    if os.path.isfile(path_task):
        read_task_overview()  # display task data
    else:
        task_overview()  # generate and display task data
        read_task_overview()


# define a function that reads user overview from file and displays it
def read_user_overview():
    with open("user_overview.txt", "r", encoding="utf-8") as u_overview:
        u_overview_read = u_overview.readlines()

        for user_line in u_overview_read:
            u_over_split_data = user_line.strip("\n").strip(".").split(",")
            for lines in u_over_split_data:
                print(lines)


# define a function that reads task overview from file and displays it
def read_task_overview():
    with open("task_overview.txt", "r", encoding="utf-8") as t_overview:
        t_overview_read = t_overview.readlines()

        for task_line in t_overview_read:
            t_over_split_data = task_line.strip("\n").split(",")
            for lines in t_over_split_data:
                print(lines)


# ===== Login Section =====

# read usernames and passwords from the user.txt file and save them as separate lists
with open("user.txt", "r", encoding="utf-8") as user_data:
    for line in user_data:
        user, psw = line.strip("\n").split(", ")
        usernames_list.append(user)
        passwords_list.append(psw)

# validate user names and passwords
print(f"{YELLOW}{BOLD}W E L C O M E   T O   T A S K   M A N A G E R !\n")
username = input(f"{WHITE}To begin, please enter your username:")  # request a username

while not username in usernames_list:  # check if username exists
    username = input("You typed incorrect username. Please enter a correct username:")

password = input("Please enter your password:")  # request a password
position = usernames_list.index(username)  # check username index

while password != passwords_list[position]:  # check if given password matches the one from the list
    password = input("You've enter incorrect password! Please try again:")
print(f"\n{YELLOW}Welcome {BOLD}{username}!")


# ===== Menu Section =====

# present the menu to the user and allow to choose an option to follow
while True:
    if username == "admin":  # present ADMIN menu
        menu = input(f'''\n{PINK}Select one of the following Options below:{WHITE}
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e  - Exit
: ''').lower()  # convert input to lowercase to avoid spelling errors
    else:  # present non-admin menu
        menu = input(f'''\n{PINK}Select one of the following Options below:{WHITE}
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()  # convert input to lowercase to avoid spelling errors

    if menu == 'r' and username == "admin":
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == "va":
        view_all()
    elif menu == "vm":
        view_mine()
    elif menu == "gr" and username == "admin":
        task_overview()
        user_overview()
    elif menu == "ds" and username == "admin":
        display_stat()
    elif menu == 'e':
        print(f'\n{YELLOW}{BOLD}Goodbye !!!')
        exit()
    else:
        print(f"\n{YELLOW}You have made a wrong choice, please Try again")
