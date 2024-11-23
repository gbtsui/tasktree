import os

# Define the database file name
database_file = "database.txt"

def load_database():
    """Load the database into a dictionary."""
    if not os.path.exists(database_file) or os.path.getsize(database_file) == 0:
        return {}
    
    database = {}
    with open(database_file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",", 5)
                
                # Ensure there are exactly 6 parts, if not, skip this line
                if len(parts) != 6:
                    print(f"Skipping invalid line: {line}")
                    continue
                
                try:
                    task_id = parts[0]
                    name = parts[1]
                    description = parts[2]
                    priority = int(parts[3]) if parts[3].isdigit() else None
                    dependencies = list(map(int, parts[4].split(";"))) if parts[4] != "-1" else []
                    completed = parts[5].lower() == "true"

                    # Add the task to the database
                    database[name] = {
                        "id": task_id,
                        "description": description,
                        "priority": priority,
                        "dependencies": dependencies,
                        "completed": completed,
                    }
                except ValueError as e:
                    print(f"Error parsing line: {line}. Error: {e}")
                    continue
    return database

def save_database(database):
    """Save the database back to the file."""
    with open(database_file, "w") as file:
        for name, data in database.items():
            dependencies = ";".join(map(str, data["dependencies"])) if data["dependencies"] else "-1"
            file.write(f"{data['id']},{name},{data['description']},{data['priority']},{dependencies},{data['completed']}\n")

def display_task_list(database):
    """Display all tasks with their IDs and names."""
    print("\nCurrent Task List:")
    print("-------------------")
    for name, data in database.items():
        print(f"ID: {data['id']} - Name: {name}")
    print("-------------------\n")

def main():
    # Load the database
    database = load_database()

    # Check if the database is empty (no tasks loaded)
    if not database:
        print("There are no tasks in the database.")
        print("What is our goal?")
        goal_description = input("Goal description: ").strip()  # Now, use the user-provided name
        database["Goal"] = {
            "id": "1",
            "description": goal_description,
            "priority": 0,
            "dependencies": [-2],  # Set dependency of goal task to -2
            "completed": False,
        }
        print(f"Goal task created with ID 1: '{goal_description}'.")
    else:
        # Check if goal task exists (ID 1). If not, create it.
        if "Goal" not in database:
            print("What is our goal?")
            goal_description = input("Goal description: ").strip()  # Now, use the user-provided name
            database["Goal"] = {
                "id": "1",
                "description": goal_description,
                "priority": 1,
                "dependencies": [-2],  # Set dependency of goal task to -2
                "completed": False,
            }
            print(f"Goal task created with ID 1: '{goal_description}'.")
        else:
            # Ask if the user wants to change the goal
            change_goal = input("Do you want to change your goal? (yes/no): ").strip().lower()
            if change_goal == "yes":
                # Prompt user to enter a new goal description
                new_goal_description = input("Enter the new goal description: ").strip()  # Use new goal name here
                database["Goal"]["description"] = new_goal_description
                print(f"Goal task updated to: '{new_goal_description}'.")

    # Ask the user if they want to add tasks in a loop
    while True:
        # Ask if the user wants to add a new task
        add_task = input("Do you want to add a new task? (yes/no): ").strip().lower()

        if add_task == "yes":
            # Proceed to configure the new task
            name = input("What is the name of the task? ").strip()
            description = input("What is the description of the task? ").strip()
            
            # If the task already exists, update its description
            if name in database:
                database[name]["description"] = description
                print(f"Task '{name}' updated with new description.")
            else:
                # Otherwise, create a new task with a unique ID
                new_id = len(database) + 1
                database[name] = {
                    "id": str(new_id),
                    "description": description,
                    "priority": None,
                    "dependencies": [],
                    "completed": False,
                }
                print(f"Task '{name}' added with ID {new_id}.")
            
            # Display task list before configuration
            display_task_list(database)

        elif add_task == "no":
            break  # Exit the loop if the user doesn't want to add more tasks
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

    # Now, go through all tasks and configure the others only after adding tasks
    print("\nConfiguring all tasks...\n")
    display_task_list(database)

    # Configure remaining tasks
    for name, data in database.items():
        if data["id"] == "1":
            # Skip configuring the goal task (ID 1)
            continue
        
        print(f"Configuring task '{name}' (ID {data['id']}):")
        
        # Get priority as a number between 1 and 5
        while True:
            try:
                priority = int(input("Enter the priority for this task (1-5, where 1 is highest): ").strip())
                if 1 <= priority <= 5:
                    break
                else:
                    print("Priority must be a number between 1 and 5. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
        
        # Get dependencies
        dependencies = input(
            "Enter the IDs of tasks this task depends on (separate by commas, or type 'none' if there are no dependencies): "
        ).strip()
        if dependencies.lower() == "none":
            dependencies_list = []
        else:
            try:
                dependencies_list = list(map(int, dependencies.split(",")))
            except ValueError:
                print("Invalid dependencies input. Defaulting to no dependencies.")
                dependencies_list = []

        # Update the task's priority and dependencies
        data["priority"] = priority
        data["dependencies"] = dependencies_list

    # Save the updated database
    save_database(database)
    print("All tasks saved successfully.")

if __name__ == "__main__":
    main()
