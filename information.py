import os
import json
import methods as myMethods

class ProgramTracker:
    def __init__(self, data_file='program_usage.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """Load program usage data from the file, if it exists."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.data = data.get('programs', {})
                self.total_runs = data.get('total_runs', 0)
        else:
            self.data = {}
            self.total_runs = 0

    def save_data(self):
        """Save the current program usage data to the file."""
        data = {
            'programs': self.data,
            'total_runs': self.total_runs
        }
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    def run_program(self, command):
        """
        Increment the count for the base script extracted from the command
        and update the total runs.
        """
        # Ensure command is a string
        if isinstance(command, list):
            command = ' '.join(command)

        # Normalize the command by removing 'python' and extracting the script name
        parts = command.strip().split()
        if parts[0].lower() == 'python':
            script_name = parts[1]
        else:
            script_name = parts[0]

        # Update counts
        script_name = os.path.basename(script_name)
        if script_name in self.data:
            self.data[script_name] += 1
        else:
            self.data[script_name] = 1
        self.total_runs += 1

        # Save updated data
        self.save_data()

    def get_program_info(self):
        """Display program usage statistics."""
        myMethods.type_print("Program usage statistics:")
        for program, count in self.data.items():
            program = os.path.splitext(program)[0]
            myMethods.type_print(f"{program}: {count} times", base_speed= 0.001)
        myMethods.type_print(f"Total runs: {self.total_runs}")





