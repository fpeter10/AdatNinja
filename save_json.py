import json
import os

def save_command_to_json(command_str, message, file_path="saved_commands.json"):
    """ Save the command to a JSON file """
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            commands = json.load(f)
    else:
        commands = []

    command_data = {
        "id": len(commands) + 1,
        "command": command_str,
        "message" : message
    }
    commands.append(command_data)

    with open(file_path, "w") as f:
        json.dump(commands, f, indent=4)

    print(f"Command saved as ID {command_data['id']}!")
    