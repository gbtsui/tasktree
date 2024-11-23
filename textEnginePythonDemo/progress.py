import os

# Define the database and completed files
database_file = "database.txt"
completed_file = "completed.txt"

def clear_database():
    """
    Clears all content from the specified file.
    """
    try:
        print(f"Attempting to clear {database_file}...")
        # Open the file in write mode to overwrite its content
        with open(database_file, 'w') as file:
            # Writing an empty string clears the file
            file.write('')
        print(f"All content in '{database_file}' has been cleared.")
    except FileNotFoundError:
        print(f"Error: The file '{database_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_database():
    """Load the database into a dictionary."""
    if not os.path.exists(database_file):
        return {}
    
    database = {}
    with open(database_file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",", 6)
                if len(parts) < 6:
                    continue

                task_id = parts[0]
                name = parts[1]
                description = parts[2]
                priority = int(parts[3]) if parts[3].isdigit() else None
                dependencies = list(map(int, parts[4].split(";"))) if parts[4] != "-1" else []
                completed = parts[5].lower() == "true"

                database[name] = {
                    "id": task_id,
                    "description": description,
                    "priority": priority,
                    "dependencies": dependencies,
                    "completed": completed,
                }
    return database

def save_database(database):
    """Save the current state of the database to the file."""
    with open(database_file, "w") as file:
        for name, task in database.items():
            if name.lower() == "goal":
                task_line = f"{task['id']},goal,{task['description']},0,-2,{str(task['completed']).lower()}"
            else:
                task_line = (
                    f"{task['id']},{name},{task['description']}," 
                    f"{task.get('priority', '')},{';'.join(map(str, task['dependencies'])) if task['dependencies'] else '-1'}," 
                    f"{str(task['completed']).lower()}"
                )
            file.write(task_line + "\n")

def save_to_completed_file(database):
    """Save all data to completed.txt and clear the database."""
    with open(completed_file, "w") as file:
        goal = next((task for name, task in database.items() if name.lower() == "goal"), None)
        if goal:
            file.write(f"Main goal:\n{goal['description']}\n\n")
        file.write("Sub tasks:\n")
        for name, task in database.items():
            if name.lower() != "goal":
                file.write(f"{name} - {task['description']}\n")
    
    # Debugging
    print("Calling clear_database...")
    clear_database()  # Ensures `database.txt` is cleared
    print("Database has been cleared after saving to completed.txt.")

def display_task_list(database):
    """Display all tasks with their IDs and names."""
    print("\nCurrent Task List:")
    print("-------------------")
    for name, data in database.items():
        print(f"ID: {data['id']} - Name: {name}")
    print("-------------------\n")

def evaluate_timeline(database):
    """Evaluate the timeline of tasks and ask for completion status."""
    tasks = [task for task in database.values() if task["id"] != "1" and not task["completed"]]
    tasks.sort(key=lambda x: x["priority"])
    
    previous_task = None
    for i, current_task in enumerate(tasks):
        print(f"Previous task: {previous_task['description']} (COMPLETED)" if previous_task else "Previous task: none")
        print(f"Current task: {current_task['description']}")
        next_task = tasks[i + 1] if i + 1 < len(tasks) else None
        print(f"Next task: {next_task['description'] if next_task else 'none'}")
        
        completed = input("Is current task completed? (yes/no): ").strip().lower()
        if completed == "yes":
            current_task["completed"] = True
            print(f"Task '{current_task['description']}' marked as completed.\n")
        else:
            skip = input("Would you like to go to your next task without completing it? (yes/no): ").strip().lower()
            if skip == "yes":
                print(f"Skipping '{current_task['description']}' without completing it.\n")
        
        previous_task = current_task
        
        if all(task["completed"] for task in database.values() if task["id"] != "1"):
            print("Congrats, you completed all tasks! Now marking the goal as completed.")
            goal_task = database.get("Goal", None)
            if goal_task:
                goal_task["completed"] = True
                save_to_completed_file(database)  # Save completed tasks and clear database
            break

def main():
    print(f"Database file path: {os.path.abspath(database_file)}")  # Debug: print full path
    database = load_database()
    if "Goal" not in database:
        print("Goal task is missing. Please make sure to define a goal task in your database first.")
        return

    evaluate_timeline(database)

if __name__ == "__main__":
    main()
