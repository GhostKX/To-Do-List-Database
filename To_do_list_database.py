# To Do List Database

import sqlite3
from datetime import datetime, timedelta
import time
import threading
from plyer import notification
import subprocess

# Establish connection with SQLite database
connection = sqlite3.connect('to_do_list_database.db')
sql = connection.cursor()

# Create a table if it doesn't exist
sql.execute('''CREATE TABLE IF NOT EXISTS to_do_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            task_name TEXT NOT NULL,
            task_description TEXT NOT NULL,
            task_reminder_date DATETIME NOT NULL
            )''')

connection.commit()


# Function to set a task reminder based on user choice
def task_remind(user_name, task_name, task_description, task_reminder_choice):
    while True:
        if task_reminder_choice == '1':
            current_time = datetime.now()
            reminder_time_str = input("\nEnter reminder time in HH:MM format (e.g., 14:30): ")
            try:
                reminder_time = datetime.strptime(reminder_time_str, '%H:%M').time()
                reminder_date_time = datetime.combine(current_time.date(), reminder_time)
                if reminder_date_time > current_time:
                    reminder_date_time = reminder_date_time.isoformat()
                    sql.execute(f'''INSERT INTO to_do_tasks (user_name, task_name, task_description, task_reminder_date) 
                    VAlUES (?, ?, ?, ?)''', (user_name, task_name, task_description, reminder_date_time))
                    connection.commit()
                    print('\nTask reminder is successfully set!')
                    print('\nNew Task is successfully been created!')
                    break
                else:
                    print('\nError. Reminder time is in the past!'
                          '\nPlease try again')
            except ValueError:
                print('\nError. Invalid reminder time'
                      '\nPlease try again')
        elif task_reminder_choice == '2':
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day
            reminder_time_str = input("Enter reminder for tomorrow time in HH:MM format(e.g., 14:30): ")
            try:
                reminder_time = datetime.strptime(reminder_time_str, '%H:%M').time()
                current_date = datetime(current_year, current_month, current_day)
                tomorrow_date = current_date + timedelta(days=1)
                reminder_date_time = datetime.combine(tomorrow_date, reminder_time)
                if reminder_date_time > tomorrow_date:
                    reminder_date_time = reminder_date_time.isoformat()
                    sql.execute('''INSERT INTO to_do_tasks (user_name, task_name, task_description, task_reminder_date)
                     VAlUES (?, ?, ?, ?)''', (user_name, task_name, task_description, reminder_date_time))
                    connection.commit()
                    print('\nTask reminder is successfully set!')
                    print('\nNew Task is successfully been created!')
                    break
                else:
                    print('\nError. Reminder time is in the past'
                          '\nPlease try again')
            except ValueError:
                print('\nError. Invalid reminder time'
                      '\nPlease try again')
        elif task_reminder_choice == '3':
            current_date_time = datetime.now()
            reminder_date_str = input("Set reminder date YYYY-MM-DD format(e.g., 2024-10-15): ")
            reminder_time_str = input("Enter reminder for tomorrow time in HH:MM format(e.g., 14:30): ")
            try:
                reminder_date = datetime.strptime(reminder_date_str, '%Y-%m-%d').date()
                reminder_time = datetime.strptime(reminder_time_str, '%H:%M').time()
                reminder_date_time = datetime.combine(reminder_date, reminder_time)
                if reminder_date_time > current_date_time:
                    reminder_date_time = reminder_date_time.isoformat()
                    sql.execute('''INSERT INTO to_do_tasks (user_name, task_name, task_description, task_reminder_date)
                     VALUES (?, ?, ?, ?)''', (user_name, task_name, task_description, reminder_date_time))
                    connection.commit()
                    print('\nTask reminder is successfully set!')
                    print('\nNew Task is successfully been created!')
                    break
                else:
                    print('\nError. Reminder time is in the past'
                          '\nPlease try again')
            except ValueError:
                print('\nError. Invalid reminder time'
                      '\nPlease try again')
        else:
            print('Error. Invalid symbol!'
                  '\nPlease try again')


# Function to check if a task name already exists
def task_name_check(task_name):
    isTrue = True
    check = sql.execute('SELECT task_name from to_do_tasks where task_name = ?', (task_name,)).fetchone()
    if check:
        isTrue = True
        return check
    else:
        pass


# Function to create a new task
def create_new_task():
    while True:
        user_name = input('\n\n(Press "0" anytime to go back)'
                          '\nPlease type in your name: ')
        if user_name == '0':
            print('Back to Menu')
            break
        else:
            if user_name.isalpha():
                task_name = input('Please type in task name: ')
                if task_name == '0':
                    print('Back to Menu')
                    break
                else:
                    if task_name != '' or ' ':
                        if task_name.strip() and any(char.isalpha() for char in task_name):
                            if task_name_check(task_name):
                                print('\nError. Task with this name already exists!'
                                      '\nPlease try again')
                            else:
                                task_description = input('Please type in task description: ')
                                if task_description == '0':
                                    print('Back to Menu')
                                    break
                                else:
                                    if task_description != '' or ' ' and task_description.strip() and any(
                                            char.isalpha() for char in task_description):
                                        task_reminder_choice = input('\n   Setting reminder: '
                                                                     '\n\n   Options (type in 1, 2, or 3):'
                                                                     '\n1. Today (specific time)'
                                                                     '\n2. Tomorrow (specific time)'
                                                                     '\n3. Another'
                                                                     '\n::: ')
                                        task_remind(user_name, task_name, task_description, task_reminder_choice)
                                        break
                                    else:
                                        print('Error. Task description should have at least one letter!'
                                              '\nPlease try again')
                        else:
                            print('Error. Some characters in task name should be letters!'
                                  '\nPlease try again')
                    else:
                        print('Error. Task name can not be empty string!'
                              '\nPlease try again')
            else:
                print('Error. User name should consist of only letters!'
                      '\nPlease try again')


# Function to display all tasks for a specific user
def view_all_tasks(user_name):
    tasks = sql.execute('''SELECT * FROM to_do_tasks where user_name = ?''', (user_name,)).fetchall()
    if tasks:
        print(f"{'Task ID':<10}{'User Name':<20}{'Task Name':<40}{'Task Description':<70}{'Deadline date':<30}")
        print("-" * 200)
        for task in tasks:
            task_id, user_name, task_name, task_description, task_reminder_date = task
            print(f"{task_id:<10}{user_name:<20}{task_name:<40}{task_description:<70}{task_reminder_date:<30}")
    else:
        print('\nError. User name is not found!'
              '\nPlease try again')


# Function to edit task details
def edit_tasks(user_name, task_name):
    edit_task = sql.execute('''SELECT * FROM to_do_tasks WHERE user_name = ? and task_name = ?''',
                            (user_name, task_name)).fetchone()
    if edit_task:
        edit_type = input(f'\n1. Username: {user_name}'
                          f'\n2. Task name: {task_name}'
                          f'\n3. Task description: {edit_task[3]}'
                          f'\n4. Task reminder date: {edit_task[4]}'
                          f'\n\nType in a number what exactly you want to change: ')
        if edit_type == '1':
            new_user_name = input('Type in New Username: ')
            if new_user_name.isalpha():
                edit_name = sql.execute(
                    '''UPDATE to_do_tasks SET user_name = ? WHERE user_name = ? and task_name = ?''',
                    (new_user_name, user_name, task_name))
                connection.commit()
                if edit_name:
                    print('\n\nChanges are successfully done!')
                else:
                    print('\nError. Something went wrong!'
                          '\nPlease try again')
            else:
                print('Error. Invalid New Username!'
                      '\nPlease try again')
        elif edit_type == '2':
            new_task_name = input('Type in New Task name: ')
            if task_name_check(new_task_name):
                print('\nError. Task with this name already exists!'
                      '\nPlease try again')
            else:
                if new_task_name.isalpha() and new_task_name != '' or ' ':
                    edit_name = sql.execute(
                        '''UPDATE to_do_tasks SET task_name = ? WHERE user_name = ? and task_name = ?''',
                        (new_task_name, user_name, task_name))
                    connection.commit()
                    if edit_name:
                        print('\n\nChanges are successfully done!')
                    else:
                        print('\nError. Something went wrong!'
                              '\nPlease try again')
                else:
                    print('Error. Invalid New task name!'
                          '\nPlease try again')
        elif edit_type == '3':
            new_task_description = input('Type in New Task description: ')
            if new_task_description != '' or ' ' and new_task_description.strip() and any(
                    char.isalpha() for char in new_task_description):
                edit_task_description = sql.execute('''UPDATE to_do_tasks SET task_description = ?
                 WHERE user_name = ? and task_name = ?''', (new_task_description, user_name, task_name))
                connection.commit()
                if edit_task_description:
                    print('\n\nChanges are successfully done!')
                else:
                    print('\nError. Something went wrong!'
                          '\nPlease try again')
            else:
                print('Error. Task description should have at least one letter!'
                      '\nPlease try again')
        elif edit_type == '4':
            current_date_time = datetime.now()
            new_reminder_date_str = input("Set reminder date YYYY-MM-DD format(e.g., 2024-10-15): ")
            new_reminder_time_str = input("Enter reminder for tomorrow time in HH:MM format(e.g., 14:30): ")
            try:
                new_reminder_date = datetime.strptime(new_reminder_date_str, '%Y-%m-%d').date()
                new_reminder_time = datetime.strptime(new_reminder_time_str, '%H:%M').time()
                new_reminder_date_time = datetime.combine(new_reminder_date, new_reminder_time)
                if new_reminder_date_time > current_date_time:
                    new_reminder_date_time = new_reminder_date_time.isoformat()
                    new_date = sql.execute('''UPDATE to_do_tasks SET task_reminder_date = ?
                     WHERE user_name = ? and task_name = ?''', (new_reminder_date_time, user_name, task_name))
                    connection.commit()
                    if new_date:
                        print('\n\nChanges are successfully done!')
                    else:
                        print('\nError. Something went wrong!'
                              '\nPlease try again')
                else:
                    print('\nError. Reminder time is in the past'
                          '\nPlease try again')
            except ValueError:
                print('\nError. Invalid reminder time'
                      '\nPlease try again')
        else:
            print('Error. Invalid edit number option!'
                  '\nPlease try again')
    else:
        print('\nError. User name or task name is not found!'
              '\nPlease try again')


# Function to delete tasks
def delete_tasks(user_name, task_name):
    delete_task = sql.execute('''SELECT * FROM to_do_tasks WHERE user_name = ? and task_name = ?''',
                              (user_name, task_name)).fetchone()
    if delete_task:
        delete_task_details = input(f'\n1. Username: {user_name}'
                                    f'\n2. Task name: {task_name}'
                                    f'\n3. Task description: {delete_task[3]}'
                                    f'\n4. Task reminder date: {delete_task[4]}'
                                    f'\n\nDo you really want to delete this task (Y/N): ').upper()
        if delete_task_details == 'Y':
            delete_task_permanently = sql.execute('''DELETE FROM to_do_tasks WHERE user_name = ? and task_name = ?''',
                                                  (user_name, task_name))
            connection.commit()
            if delete_task_permanently:
                print('Task is successfully deleted!')
            else:
                print('\nError. Something went wrong!'
                      '\nPlease try again')
        elif delete_task_details == 'N':
            print('Back to Menu')
            exit(0)
        else:
            print('Error. Invalid delete option!'
                  '\nPlease try again')

    else:
        print('\nError. User name or task name is not found!'
              '\nPlease try again')


# Reminder checking function that runs in the background
# For macOS notifications

# macOS native notification using terminal-notifier
def send_mac_notification(title, message):
    # Using terminal-notifier with sound and pop-up
    subprocess.run([
        'terminal-notifier',
        '-title', title,
        '-message', message,
        '-sound', 'default',  # Play default sound
        '-timeout', '10'  # Show the notification for 10 seconds
    ])


# Reminder checking function that runs in the background
def check_for_reminders():
    # Create a new SQLite connection for this thread
    connection = sqlite3.connect('to_do_list_database.db', check_same_thread=False)
    sql = connection.cursor()

    while True:
        current_time = datetime.now().isoformat()  # Get the current time
        tasks_due = sql.execute('SELECT * FROM to_do_tasks WHERE task_reminder_date <= ?', (current_time,)).fetchall()

        if tasks_due:
            for task in tasks_due:
                task_id, user_name, task_name, task_description, task_reminder_date = task
                # Trigger a desktop notification
                # notification.notify(
                #     title=f"Reminder: {task_name}",
                #     message=f"Task for {user_name} is due! Description: {task_description}",
                #     timeout=10  # Notification will disappear after 10 seconds
                # )
                send_mac_notification(task_name, task_description)
                print(f'\nReminder: {task_name} for {user_name} is due! Description: {task_description}')

        time.sleep(60)  # Check every 60 seconds


# Start reminder checking thread
if __name__ == "__main__":
    reminder_thread = threading.Thread(target=check_for_reminders, daemon=True)
    reminder_thread.start()
    # # Main program # #
    while True:
        user_choice = input(f"\n{('*' * 75)}"
                            f"\n              {'Hi, Welcome to the To-do-mini-app!'}"
                            f"\n\n"
                            f"\n   Main Menu:"
                            f'\n1. Create new task'
                            f'\n2. View all tasks'
                            f'\n3. Edit task'
                            f'\n4. Delete task'
                            f'\n5. Exit'
                            f'\n::: ')
        if user_choice == '1':
            create_new_task()
        elif user_choice == '2':
            user_name = input('\nPlease type in user name: ')
            view_all_tasks(user_name)
        elif user_choice == '3':
            user_name = input('\nPlease type in user name: ')
            task_name = input('\nPlease type in task name: ')
            edit_tasks(user_name, task_name)
        elif user_choice == '4':
            user_name = input('\nPlease type in user name: ')
            task_name = input('\nPlease type in task name: ')
            delete_tasks(user_name, task_name)
        elif user_choice == '5':
            print('\nExiting the program!')
            break
        else:
            print('\nError. Please use numbered options!'
                  '\nPlease try again')
