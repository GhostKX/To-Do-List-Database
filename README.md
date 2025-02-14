# To-Do List Application

A **Python-based command-line application** for managing daily tasks using **SQLite**. This system allows users to **add, edit, delete, and mark tasks as completed**, providing an efficient way to track daily activities.

## Features

### **Task Management**
- **Add a new task** with a title and optional description.
- **Edit task details** including title and description.
- **Delete tasks** permanently to remove completed or unnecessary tasks.
- **Mark tasks as completed**, updating their status.
- **View all tasks** with filters for pending and completed tasks.

### **Database Integration**
- Uses **SQLite** for persistent data storage, ensuring tasks are saved across sessions.
- **Data validation** to prevent duplicate or empty task entries.
- **Secure and reliable operations** to maintain data integrity.

### **User-Friendly Interface**
- Interactive **command-line menu** for easy navigation.
- **Input validation** ensures correct data entry.

## Requirements

- **Python 3.x** or higher  
- **SQLite** (built-in with Python)  
- No external libraries required  

## How to Run

1. Clone or download this repository.
2. Open a terminal or command prompt.
3. Navigate to the project directory.
4. Run the script using:

```bash
python To_do_list_database.py
```

## Usage

The system provides the following options:

- **Add Task**: Create a new task with a title and optional description.  
- **Edit Task**: Modify an existing task's title or description.  
- **Delete Task**: Remove a task permanently from the list.  
- **Mark as Completed**: Update the status of a task to "Completed."  
- **View Tasks**: Display all tasks, with filtering options for pending and completed tasks.  
- **Exit**: Close the application.  


## Example Usage Scenario
```
**********************************************
Welcome to the To-Do List Application!

Choose an option:
1 - Add a task
2 - Edit a task
3 - Delete a task
4 - Mark task as completed
5 - View all tasks
6 - Exit
::: 1

Enter Task Title: Complete Python project  
Enter Task Description: Finish implementing and testing features  

Task successfully added!
--------------------------------
Title: Complete Python project
Status: Pending
--------------------------------
```

## Code Structure

### Database Schema

The system manages tasks in an SQLite database table named `tasks`, which stores:

- **id** (Primary Key) – Auto-incremented task ID.  
- **title** – Task title (must be unique).  
- **description** – Additional task details (optional).  
- **status** – Task status (`Pending` or `Completed`).  
- **created_at** – Timestamp indicating when the task was added.  

### Core Functions

The system consists of well-structured functions for task management:

- **`add_task(title, description)`** – Creates and stores a new task.  
- **`edit_task(task_id, new_title, new_description)`** – Updates an existing task's title or description.  
- **`delete_task(task_id)`** – Removes a task permanently from the database.  
- **`mark_task_completed(task_id)`** – Changes the status of a task to "Completed."  
- **`view_tasks(status_filter)`** – Retrieves and displays tasks based on their status (`Pending`, `Completed`, or `All`).  

### Security & Validation

- **Title uniqueness check** prevents duplicate task names.  
- **Valid input handling** ensures correct and formatted data entry.  
- **Database integrity checks** maintain accurate and consistent task records.  


## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/To-Do-List-Database**)
