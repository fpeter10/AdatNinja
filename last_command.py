import json
import os

def save_last_command_to_json(command_str, file_path="last_commands.json"):
    """Maintain a fixed-length history of 5 commands where the newest is ID 1 and the oldest is ID 5."""
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            commands = json.load(f)
    else:
        commands = []

    # Add new command at the beginning
    commands.insert(0, {"id": 1, "command": command_str})

    # Ensure the list always has exactly 5 elements
    commands = commands[:5]  # Keep only the latest 5

    # Reassign IDs (newest should be ID 1, oldest should be ID 5)
    for i, cmd in enumerate(commands, start=1):
        cmd["id"] = i

    # Save back to JSON
    with open(file_path, "w") as f:
        json.dump(commands, f, indent=4)

    #print(f"Saved as ID 1!")
