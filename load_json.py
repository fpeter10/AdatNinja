import json
import os

def load_command_from_json(code_id, filename='saved_commands.json'):
    """
    Load a command and its working directory from a JSON file using the provided code_id.

    Parameters:
        code_id (int): The ID of the command to load.
        filename (str): The name of the JSON file to load the command from.

    Returns:
        dict or None: A dictionary with 'command' and 'message' if found, else None.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                commands = json.load(file)

                for command in commands:
                    if command.get('id') == code_id:
                        return command
                print(f"Command with ID {code_id} not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON file.")
    else:
        print(f"File {filename} does not exist.")
    return None

