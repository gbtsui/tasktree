def clear_database(file_name):
    """
    Clears all content from the specified file.

    Args:
        file_name (str): The name of the file to be cleared.
    """
    try:
        # Open the file in write mode to overwrite its content
        with open(file_name, 'w') as file:
            # Writing an empty string clears the file
            file.write('')
        print(f"All content in '{file_name}' has been cleared.")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
clear_database('database.txt')
