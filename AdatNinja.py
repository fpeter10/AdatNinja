from check_package import check_and_update_libraries
check_and_update_libraries()

import subprocess
import json
import os
import sys
import colorama
import methods as myMethods
import pandas as pd

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from save_json import save_command_to_json
from load_json import load_command_from_json
from modify_code2 import modify_parameters
from information import ProgramTracker
from methods import welcome
from methods import type_print
from methods import check_exit

from autofill import HeaderCompleter, SchemaCompleter, DirectoryCompleter, MultiHeaderCompleter, FileCompleter, HelpCompleter
import autofill as autofill

colorama.init(autoreset=True)

def print_help():
    """Interactive help: ask the user which program to show help for."""
    type_print("Available programs:" , color= colorama.Fore.YELLOW)
    for key, prog in programs.items():
        type_print(f"  {key:10} {prog['description']}", base_speed= 0.001, color=  colorama.Fore.CYAN)

    while True:
        type_print("Enter program name to see help: ")
        choice = prompt('', completer=HelpCompleter(autofill.program_help)).strip().lower()
        check_exit(choice)

        if choice in programs:
            prog = programs[choice]["code"]
            try:
                result = subprocess.run(
                    [sys.executable, prog, "--help"],
                    text=True,
                    capture_output=True,
                    check=False
                )
                if result.stdout:
                    type_print(result.stdout , base_speed= 0.001)
                    #print(colorama.Fore.YELLOW +  + colorama.Style.RESET_ALL)
                if result.stderr:
                    type_print(result.stderr , base_speed= 0.001)
                    #print(colorama.Fore.RED + result.stderr + colorama.Style.RESET_ALL)
            except FileNotFoundError:
                print(colorama.Fore.RED + f"Program file not found: {prog}" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + f"Unknown program: {choice}" + colorama.Style.RESET_ALL)



def load_last_command(file_path="last_commands.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            commands = json.load(f)
            if commands:
                return commands[-1]["command"]  # Return last saved command
    return None  # No previous command found

chat_prog = {
    "list": {
        "name" : "list",
        "description": "List functions."
    },

    "programs": {
        "name" : "programs",
        "description" : "List programs"
    },

    "help": {
        "name" : "help",
        "description" : "Print program help"
    },
        
    "load code xx check": {
        "description": "Check loaded code, xx = ID"
    },

    "load code xx run": {
        "description": "Run loaded code, xx = ID"
    },

    "load code xx modify": {
        "description": "You can modify loaded code easily, xx = ID"
    },

    "load last_code xx check": {
        "description": "Check last code, xx = ID"
    },

    "load last_code xx run": {
        "description": "Run last code, xx = ID"
    },

    "load last_code xx modify": {
        "description": "You can modify last code easily, xx = ID"
    },

    "load last_code xx save": {
        "description": "You can save last code, xx = ID"
    },

    "change wd": {
        "description": "Change working directory"
    },

    "wd": {
        "description": "Print working directory"
    },

    "info": {
        "description": "Print program usage stat"
    },

    "language": {
        "description": "Change language settings that effects decimal separator"
    },

    "exit": {
        "description": "Exit the program"
    },

    "": {
        "description": ""
    }
}

programs = {
    "stat": {
        "code": "stat.py",
        "name": "stat",
        "description" : "Calcualte statistics",
        "params": ["--table", "--output", "--name_col", "--value_col", "--group_col"]
    },

    "wilcoxon": {
        "code": "wilcoxon.py",
        "name": "wilcoxon",
        "description" : "Calcualte Wilcoxon test",
        "params": ["--table", "--output", "--name_col", "--value_col", "--group_col"]
    },

    "ttest": {
        "code": "ttest.py",
        "name": "ttest",
        "description" : "Calculate T test",
        "params": ["--table", "--output", "--name_col", "--value_col", "--group_col"]
    },

    "normality": {
        "code": "normality_test.py",
        "name": "normality",
        "description" : "Calculate normality test",
        "params": ["--table", "--output", "--name_col", "--value_col", "--group_col"]
    },

    "summarize": {
        "code": "summarize.py",
        "name": "summarize",
        "description" : "Calcualte summarize (sum, mean, median, min, max) of the data in a group",
        "params": ["--table", "--output", "--name_col", "--value_col", "--group_col", "--summary_mode"]
    },

    "print table":{
       "code": "print_table.py",
       "name": "print table",
       "description" : "Print table",
       "params": ["--table"]
    },
    "long format":{
        "code": "long_format.py",
        "name": "long format",
        "description" : "Transpose to long format",
        "params": ["--table", "--output"]
    },
    "wide format":{
        "code": "wide_format.py",
        "name": "wide format",
        "description": "Transpose to wide format",
        "params": ["--table", "--output", "--id_col", "--value_col", "--sample_col"]
    },
    "merge":{
        "code": "merge.py",
        "name": "merge",
        "description": "Merge 2 table",
        "params": ["--table1", "--table2", "--output", "--tab_id1", "--tab_id2", "--mode"]
    },
    "relative":{
        "code": "relative.py",
        "name": "relative",
        "description": "Calculate relative values",
        "params": ["--table", "--output", "--group_col", "--sum_value"]
    },
    "merge columns":{
        "code": "merge_columns.py",
        "name": "merge columns",
        "description": "Merge 2-5 columns into one",
        "params": ["--table", "--output", "--merge_cols", "--new_column", "--separator"]
    },
    "split columns":{
        "code": "split_column.py",
        "name": "split columns",
        "description": "Split a complex column into single ones",
        "params": ["--table", "--output", "--column_to_split", "--separator", "--new_columns"]
    },

    "change sep":{
        "code": "change_sep.py",
        "name": "change sep",
        "description": "Change the separator and decimal",
        "params": ["--table", "--output", "--sep", "--dec"]
    }, 

    "sort table": {
        "code": "sort_table.py",
        "name": "sort table",
        "description": "Sort table data according to multiple column in order",
        "params": ["--table", "--output", "--keys", "--sort_mode"]
    }

}



def list_chat_available():
    print(colorama.Fore.CYAN + "\nAvailable:")
    for key, value in chat_prog.items():
        type_print(f"{key} - {value['description']}", color= colorama.Fore.YELLOW, base_speed= 0.001)
    print()

def list_programs():
    print(colorama.Fore.CYAN + "\nAvailable programs:")
    for key, value in programs.items():
        type_print(f"{key} - {value['description']}", color = colorama.Fore.YELLOW, base_speed= 0.001)
    print()


def get_working_directory():
    """Ask the user for the working directory and validate it."""
    while True:
        directory = prompt("Enter the working directory: ", completer=DirectoryCompleter()).strip()
        check_exit(directory)
        if os.path.isdir(directory):
            type_print(f"Directory set to: {directory}")
            return directory
        type_print(f"Invalid directory. Please enter a valid path.", color = colorama.Fore.RED)


def build_command(program_key, working_dir):
    """Builds the command dynamically, including the working directory."""
    program = programs.get(program_key)
    if not program:
        type_print("Invalid selection.", color= colorama.Fore.RED)
        return None

    cmd = ["python", program["code"], "--workdir", working_dir]

    file_completer = FileCompleter(working_dir)

    table_path = ""
    headers = ""
    headers1 = ""
    headers2 = ""

    for param in program["params"]:
        type_print(f"Enter value for {param}: ")

        if param in ["--table"]:
        #Prompt for file path with file completion
            value = prompt("", completer=file_completer).strip()
            check_exit(value)

            table_path = os.path.join(working_dir, value)
            try:
                sep, dec = myMethods.detect_separator_and_decimal(table_path)
                df = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')
                
                headers = df.columns.tolist()
            except Exception as e:
                headers = []
            cmd.extend([param, value])

        if param in ["--table1"]:
        #Prompt for file path with file completion
            value = prompt("", completer=file_completer).strip()
            check_exit(value)

            table_path = os.path.join(working_dir, value)
            try:
                sep, dec = myMethods.detect_separator_and_decimal(table_path)
                df1 = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')
                
                headers1 = df1.columns.tolist()
            except Exception as e:
                headers1 = []
            cmd.extend([param, value])


        if param in ["--table2"]:
        #Prompt for file path with file completion
            value = prompt("", completer=file_completer).strip()
            check_exit(value)

            table_path = os.path.join(working_dir, value)
            try:
                sep, dec = myMethods.detect_separator_and_decimal(table_path)
                df2 = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')
                
                headers2 = df2.columns.tolist()
            except Exception as e:
                headers2 = []
            cmd.extend([param, value])

        if param in ["--output"]:
        #Prompt for file path with file completion
            value = prompt("", completer=file_completer).strip()
            check_exit(value)
            cmd.extend([param, value])
        
        join_type_completer = WordCompleter(autofill.merge_mode_autofill, ignore_case=True)

        if param in ["--mode"]:
            value = prompt("", completer=join_type_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        summary_mode_completer = WordCompleter(autofill.summary_mode_autofill, ignore_case=True)

        if param in ["--summary_mode"]:
            value = prompt("", completer=summary_mode_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--sep"]:
            new_separator_completer = WordCompleter(autofill.new_separator_autofill, ignore_case=True)
            value = prompt("", completer= new_separator_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--dec"]:
            new_decimal_completer = WordCompleter(autofill.new_decimal_autofill, ignore_case=True)
            value = prompt("", completer= new_decimal_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--tab_id1"]:             
            header_completer1 = HeaderCompleter(headers1)
            value = prompt("", completer=header_completer1).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--tab_id2"]:             
            header_completer2 = HeaderCompleter(headers2)
            value = prompt("", completer=header_completer2).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--name_col", "--group_col", "--value_col", "--sample_col", "--column_to_split", "--new_column"]:             
            header_completer = HeaderCompleter(headers)
            value = prompt("", completer=header_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--merge_cols", "--id_col", "--new_columns", "--keys"]:            
            multi_header_completer = MultiHeaderCompleter(headers)
            value = prompt("", completer=multi_header_completer).strip()
            check_exit(value)
            value2 = [v for v in value.split() if v]
            cmd.append(param)
            cmd.extend(value2)

        if param in ["--sum_value"]:
            sum_value_completer = WordCompleter(autofill.relative_summary_autofill, ignore_case=True)
            value = prompt("", completer=sum_value_completer).strip()
            check_exit(value)
            cmd.extend([param, value])

        if param in ["--separator"]:
            separator_completer = WordCompleter(autofill.separator_autofill, ignore_case=True)
            value = prompt("", completer=separator_completer).strip()
            check_exit(value)

        if param in ["--sort_mode"]:
            sort_mode_completer = WordCompleter(autofill.sort_mode_autofill, ignore_case=True)
            value = prompt("", completer=sort_mode_completer).strip()
            check_exit(value)
            
            cmd.extend([param, value])

        
            
  
        if param not in ["--name_col", "--group_col", "--value_col", "--output", "--table",
                         "--tab_id1", "--tab_id2", "--table1", "--table2", "--mode", "--summary_mode",
                         "--id_col", "--sample_col", "--sum_value", "--merge_cols", "--keys", "--sort_mode",
                         "--column_to_split", "--new_columns", "--new_column", "--separator", "--sep", "--dec"]:
            value = input(f"").strip()
            cmd.extend([param, value])

    return cmd

with open('saved_commands.json', 'r') as file:
    commands = json.load(file)

def main():

    welcome()

    myMethods.save_language(force= False)

    tracker = ProgramTracker()
    
    workdirectory = get_working_directory()

    type_print("Type 'list' to see available functions, 'program' to see available programs 'exit' to quit")

    while True:
        try:
            command = prompt('Enter a command: ', completer=SchemaCompleter()).strip().lower()

            check_exit(command)
            
            if not command:
                type_print("Waiting for command. use [list] to to check available functions!")


            if command == "program" or command == "programs":
                list_programs()

            if command == "list":
                list_chat_available()

            if command == "help":
                print_help()

            if command == "change wd":
                workdirectory = get_working_directory()
                type_print("Changed")

            if command == "wd":
                type_print(f"Working directory: {workdirectory}")

            if command == "info":
                tracker.get_program_info()

            if command == "language":
                myMethods.save_language(force= True)
    
            if command.startswith("load code"):
                try:    
                    parts = command.split()
                    code_id = int(parts[2])
                    loaded_command = load_command_from_json(code_id, 'saved_commands.json')

                    if loaded_command and len(parts) > 3 and parts[3] in {'run', 'modify', 'check'}:

                        
                        if loaded_command and parts[3] == "check":
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                        elif loaded_command and parts[3] == "run":
                            
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                            subprocess.run(loaded_command['command'], check=True)
                            tracker.run_program(loaded_command['command']) # megszámolás


                        elif loaded_command and len(parts) > 3 and parts[3] == "modify":
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(colorama.Fore.CYAN + f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                            loaded_command['command'] = modify_parameters(loaded_command['command'])
                            type_print(f"Modified command:\n", color= colorama.Back.BLUE)
                            type_print(colorama.Fore.CYAN + f"{loaded_command['command']}", color= colorama.Fore.CYAN)
                            
                            subprocess.run(loaded_command['command'])
                            tracker.run_program(loaded_command['command'])

                    else:
                        type_print("Invalid command format. Use 'load codeX check' to check code or 'load codeX run' to run current code or 'load codeX modify' to modify code where X is the command ID.", color= colorama.Fore.RED)
                except (ValueError, IndexError):
                        type_print("Invalid command format. Use 'load codeX check' to check code or 'load codeX run' to run current code or 'load codeX modify' to modify code where X is the command ID.", color= colorama.Fore.RED)


            if command.startswith("load last_code"):
                try:    
                    parts = command.split()
                    code_id = int(parts[2])
                    loaded_command = load_command_from_json(code_id, 'last_commands.json')

                    if loaded_command and len(parts) > 3 and parts[3] in {'run', 'modify', 'check', 'save'}:

                        
                        if loaded_command and parts[3] == "check":
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                        elif loaded_command and parts[3] == "run":
                            
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                            subprocess.run(loaded_command['command'], check=True)
                            tracker.run_program(loaded_command['command']) # megszámolás

                        elif loaded_command and parts[3] == "save":
                            
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                            message = input("Enter a message: ")
                            save_command_to_json(loaded_command['command'], message)


                        elif loaded_command and len(parts) > 3 and parts[3] == "modify":
                            type_print(f"Loaded command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)

                            loaded_command['command'] = modify_parameters(loaded_command['command'])
                            type_print(f"Modified command:\n", color= colorama.Back.BLUE)
                            type_print(f"{loaded_command['command']}", color= colorama.Fore.CYAN)
                            
                            subprocess.run(loaded_command['command'])
                            tracker.run_program(loaded_command['command'])

                    else:
                        type_print("Invalid command format. Use 'load codeX check' to check code or 'load codeX run' to run current code or 'load codeX modify' to modify code where X is the command ID.", color= colorama.Fore.RED)
                except (ValueError, IndexError):
                        type_print("Invalid command format. Use 'load codeX check' to check code or 'load codeX run' to run current code or 'load codeX modify' to modify code where X is the command ID.", color= colorama.Fore.RED)


            if command in programs:
                    type_print(f"Running {programs[command]['code']}... ", color= colorama.Fore.GREEN)
                    
                    cmd = build_command(command, working_dir= workdirectory)
                    if cmd:
                        subprocess.run(cmd)
                        tracker.run_program(cmd)                        
                    else:
                        print(" ")
                    # Stop spinner after task done
            
            if command.endswith("check") or command.endswith("run") or command.endswith("modify") and command.startswith("load code") and len(command) > 9:
                continue
            
            elif command not in programs and command not in chat_prog:
                print("Typo use [list] to check available functions!")

        except myMethods.BackToMainMenu:
            continue
        
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nOperation cancelled. Type 'exit' to quit.")


if __name__ == "__main__":
    main()
