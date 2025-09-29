import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json

from methods import type_print
from prompt_toolkit import prompt
from autofill import MultiHeaderCompleter, FileCompleter, HeaderCompleter
from prompt_toolkit.completion import WordCompleter

colorama.init()

separator_completer = WordCompleter(["_", ";", ",", "|"], ignore_case=True)


def merge_categories(workdir, table_file, output_file, merge_cols, new_column, separator, test_mode):
    workdir = Path(workdir)

    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")

    merge_cols = myMethods.coerce_cols(merge_cols)

    while True:
        try:
            myMethods.check_table(workdir, table_file, parameter= "table")
                
            sep, dec = myMethods.detect_separator_and_decimal(table_path)
            table = pd.read_csv(table_path, sep = sep, decimal = dec, engine = 'python')

            try:
                headers = table.columns.tolist()
            except Exception as e:
                headers = []

            multi_header_completer = MultiHeaderCompleter(headers)
            header_completer = HeaderCompleter(headers)
            
            

            if not (2 <= len(merge_cols) <= 5):
                raise ValueError(f"Error: You must provide between 2 and 5 columns to merge.")


            # Validate all specified merge columns exist
            for col in merge_cols:
                if col not in table.columns:
                    raise ValueError(f"Error: Column '{col}' not found in table.")
                
            # Validate new column not exist
            for col in table.columns:
                if col == new_column:
                    raise ValueError(f"Error: Column '{col}' is already exist, can not be new column")

            
            myMethods.blue_message("table: ", table)

            # separator ellenőrzés
            if not myMethods.validate_separator_type(separator):
                    raise ValueError(f"Invalid separator type: '{separator}'. Only '_' ';' ',' '|' are allowed.")

            # Merge selected columns into one
            table[new_column] = table[merge_cols].astype(str).agg(separator.join, axis=1)

            table.to_csv(output_path, index=False, sep="\t")

            myMethods.success_message(table, "merged categories", output_path, test_mode)
            break

        except ValueError as e:
            file_completer = FileCompleter(workdir)

            print(colorama.Fore.RED, str(e))
            print(colorama.Style.RESET_ALL)

            # Not Csv hibakezelés
            if '--table is not a CSV or TSV file' in str(e):  # Check if error is related to file type
                if not myMethods.is_csv_file(str(table_path)):
                        if not myMethods.is_csv_file(str(table_path)):
                            table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                             completer= file_completer)
                            table_path = workdir / table_file
                        continue
                            
            # --table üres hibakezelés   
            elif '--table is full empty' in str(e):
                table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                             completer= file_completer)
                table_path = workdir / table_file                    
                continue

            elif "not found in table." in str(e):
                merge_cols = prompt("Enter 2–5 column names: ", completer=multi_header_completer).strip()
                myMethods.check_exit(merge_cols)
                merge_cols = [col.strip() for col in merge_cols.split() if col.strip()]
                continue
            
            elif "between 2 and 5 columns to merge." in str(e):
                merge_cols = prompt("Enter 2–5 column names: ", completer=multi_header_completer).strip()
                myMethods.check_exit(merge_cols)
                merge_cols = [col.strip() for col in merge_cols.split() if col.strip()]
                if not (2 <= len(merge_cols) <= 5):
                    type_print("Still invalid: you must provide between 2 and 5 columns.")
                    continue
                
            # new column
            elif "is already exist, can not be new column" in str(e):
                new_column = myMethods.error_handling(print_message= "Enter correct --new_column column: ", 
                                             completer= header_completer)
                continue
                
            # separator 
            elif 'Invalid separator type:' in str(e):  # Check if error is related to separator
                if not myMethods.validate_separator_type(str(separator)):
                    separator = myMethods.error_handling(print_message= "Enter correct separator : '_', ';', ',', '|'  ", 
                            completer= separator_completer)
                    continue
                
        #--table hibakezelés
        except FileNotFoundError as e:
            file_completer = FileCompleter(workdir)

            print(colorama.Fore.RED, f"{e}")
            print(colorama.Style.RESET_ALL)
            if '--table file not found' in str(e):
                if not myMethods.is_file_exists(table_path):
                        table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                             completer= file_completer)
                        table_path = workdir / table_file  
                        continue
        
        except myMethods.BackToMainMenu:
                break
            
        except myMethods.ExitProgram:
                raise SystemExit(0)
        
    return workdir, table_file, output_file, merge_cols, new_column, separator

def parse_stat():
    parser = argparse.ArgumentParser(description="Merge two category columns and aggregate their values.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output", help= myMethods.help_output("_merged_columns"))
    parser.add_argument("--merge_cols", nargs='+', help="List of columns to merge (2 to 5 columns allowed)")
    parser.add_argument("--new_column", help="The name of the new column.")
    parser.add_argument("--separator", help="Separator for splitting choose from: '_', ';', ',', '|'. Default: '_' ")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_stat()

    # default output name if not provided
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_merged_columns"

    # get arguments
    workdir = args.workdir or ""
    table = args.table or ""
    output = args.output or ""
    merge_cols = args.merge_cols or ""
    new_column = args.new_column or ""
    separator = args.separator or "_"

    # ensure merge_cols is a list
    if isinstance(merge_cols, str):
        merge_cols = merge_cols.split()  # split string by whitespace
    elif not isinstance(merge_cols, list):
        raise ValueError("merge_cols must be string or list")

    # perform merge
    test_mode = False
    while True:
        try:
            workdir_save, table_save, output_file_save, merge_cols_save, new_column_save, separator_save = merge_categories(
                workdir, table, output, merge_cols, new_column, separator, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = merge_cols_save, new_column_save, separator_save = (None,) * 2
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)
        
    # update args for internal use
    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.merge_cols = merge_cols_save  # this is a list
    args.new_column = new_column_save
    args.separator = separator_save

    # save JSON command as space-separated string
    merge_cols_str = " ".join(args.merge_cols) if args.merge_cols and isinstance(args.merge_cols, list) else (args.merge_cols or "")
    cmd = f"python merge_columns.py --workdir {args.workdir} --table {args.table} --output {args.output} --merge_cols {merge_cols_str} --new_column {args.new_column} --separator {args.separator}"
    save_last_command_to_json(cmd)