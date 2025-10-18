import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json
from methods import type_print
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from autofill import HeaderCompleter, MultiHeaderCompleter, FileCompleter
import autofill as autofill

colorama.init()

settings = myMethods.get_local_settings()
language = settings["language"]
decimal = settings["decimal"]

separator_completer = WordCompleter(autofill.separator_autofill, ignore_case=True)

def split_column_names(workdir, table_file, output_file, column_to_split, separator, new_columns, test_mode):
    
    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")

    new_columns = myMethods.coerce_cols(new_columns)

    while True:
        try:
            # check table valid
            myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
              
            # sepator  decimal meghatározás automatikusan
            sep, dec = myMethods.detect_separator_and_decimal(table_path)

            # beolovasás                    
            table = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')

            try:
                headers = table.columns.tolist()
            except Exception as e:
                headers = []

            header_completer = HeaderCompleter(headers)
            multi_header_completer = MultiHeaderCompleter(headers)

            # separator ellenőrzés
            if not myMethods.validate_separator_type(separator):
                    raise ValueError(f"Invalid separator type: '{separator}'. Only '_' ';' ',' '|' are allowed.")
            
            if sep == separator:
                raise ValueError(f"Separator type: '{separator} is the same as separator of the table.")
            
            # --column_to_split minden lehetséges hiba kiszűrése
            myMethods.check_everything_string(table= table, table_path= table_path, value_to_check= column_to_split, 
                                                  parameter= "column_to_split", sep= sep, is_none_possible= False)
            
            # check none of the new column names exist already
            conflicts = [c for c in new_columns if c in headers]
            if conflicts:
                raise ValueError(f"--new_columns contains names already existing in table: {', '.join(conflicts)}")

            # Split the column into multiple parts
            split_cols = table[column_to_split].astype(str).str.split(separator, expand=True)

            if split_cols.shape[1] == 1:
                myMethods.list_available_columns(str(table_path), sep)
                raise ValueError(f"Column '{column_to_split}' can not split!")
            
            # Ensure new_columns is a list of column names (split by whitespace if given as string)
            if isinstance(new_columns, str):
                new_columns = [c for c in new_columns.strip().split() if c]
            
            # how many splits are actually in the data (assume all rows consistent)
            n_actual = table[column_to_split].astype(str).str.split(separator).str.len().unique()


            if len(n_actual) != 1:
                myMethods.list_available_columns(str(table_path), sep)
                raise ValueError(
                    f"Column '{column_to_split}' does not split into a consistent number of parts. "
                    f"Found: {n_actual}"
                )
            
            n_actual = n_actual[0]
            n_expected = len(new_columns)

            if n_actual != n_expected:
                raise ValueError(
                    f"Mismatch: column '{column_to_split}' can be splited into {n_actual} parts, "
                    f"but you provided {n_expected} new column names: {new_columns}"
                )
            
            myMethods.blue_message("table: ", table)
            type_print(f"\nLoaded file with {table.shape[0]} rows and {table.shape[1]} columns.\n")

            # Assign the new columns
            split_cols.columns = new_columns
            table_split = pd.concat([table, split_cols], axis=1)

            table_split.to_csv(str(output_path), index=False, sep= "\t", decimal= dec)

            #save to csv
            myMethods.safe_to_csv(table= table_split, output_path= output_path, separator= "\t", decimal= decimal)


            myMethods.success_message(table_split, "split", output_path, test_mode= test_mode)
            break  

        except ValueError as e:
            file_completer = FileCompleter(workdir)

            print(colorama.Fore.RED, f"{e}")
            print(colorama.Style.RESET_ALL)

            # Not Csv hibakezelés
            if '--table is not a CSV or TSV file' in str(e):  # Check if error is related to file type
                if not myMethods.is_csv_file(str(table_path)):
                    type_print("Enter correct table: ", color = colorama.Fore.RED)
                    table_file = prompt("", completer=file_completer).strip()
                    myMethods.check_exit(table_file)
                    update_table = table_file
                    table_path = workdir / update_table  # Update the path
                    continue
                            
            # --table üres hibakezelés   
            elif '--table is full empty' in str(e):
                table_file = prompt("Enter correct table: ", completer=file_completer).strip()
                myMethods.check_exit(table_file)
                update_table = table_file
                table_path = workdir / update_table
                continue
            
            # --column_to_split hibakezelés
            elif 'as --column_to_split column not found!' in str(e):  
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                                completer= header_completer)
                continue
                
            # üres --column_to_split
            elif '--column_to_split is empty!' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                                completer= header_completer) 
                
            # üres értékek Nan --column_to_split
            elif '--column_to_split contains Nan values!' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --ncolumn_to_splitame_col column: ", 
                                             completer= header_completer) 
                continue
                    

            # --column_to_split szám hibakezelés
            elif '--column_to_split should not be numeric!' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                            completer= header_completer)                    
                continue
            
            elif '--column_to_split has mixed data types, please use consistent columns!' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                                        completer= header_completer)
                continue
            
            elif 'can not split!' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                            completer= header_completer) 

                separator = myMethods.error_handling(print_message= "Enter correct separator : '_', ';', ',', '|'  ", 
                            completer= separator_completer)                   
                continue

            # separator 
            elif 'Invalid separator type:' in str(e):  # Check if error is related to separator
                if not myMethods.validate_separator_type(str(separator)):
                    separator = myMethods.error_handling(print_message= "Enter correct separator : '_', ';', ',', '|'  ", 
                            completer= separator_completer)
                    continue
                
            # separator ugyanaz mint table separator
            elif 'is the same as separator of the table.' in str(e):  # Check if error is related to separator
                separator = myMethods.error_handling(print_message= "Enter correct separator : '_', ';', ',', '|'  ", 
                        completer= separator_completer)
                continue
            
            elif '--new_columns contains names already existing in table' in str(e): 
                new_columns = myMethods.error_handling(print_message= "Enter correct --new_columns column: ", 
                            completer= multi_header_completer)
                continue
             
            elif 'can be splited into' in str(e): 
                new_columns = myMethods.error_handling(print_message= "Enter correct --new_columns column: ", 
                            completer= multi_header_completer)
                continue
            
            elif 'does not split into a consistent number of parts' in str(e): 
                column_to_split = myMethods.error_handling(print_message= "Enter correct --column_to_split column: ", 
                            completer= header_completer)
                continue
            
        #--table hibakezelés
        except FileNotFoundError as e:
            file_completer = FileCompleter(workdir)

            print(colorama.Fore.RED, f"{e}")
            print(colorama.Style.RESET_ALL)

            if '--table file not found' in str(e):
                if not myMethods.is_file_exists(table_path):
                    table_file = prompt("Enter correct table: ", completer=file_completer).strip()
                    myMethods.check_exit(table_file)
                    update_table = table_file
                    table_path = workdir / table_file  
            continue 
        
        except myMethods.BackToMainMenu:
                break
            
        except myMethods.ExitProgram:
                raise SystemExit(0)

    return workdir, table_file, output_file, column_to_split, separator, new_columns

    
def main():
    parser = argparse.ArgumentParser(description="Split one complex mapping column names into multiple columns. " 
    "Useful when one column contains multiple pieces of information "
    "separated by a character (e.g., 'A_B_C').",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output", help= myMethods.help_output(default_output= "_split_column"))
    parser.add_argument("--column_to_split", help="Name of the column to split.")
    parser.add_argument("--separator", help="Separator character used to split the column, choose from: '_', ';', ',', '|'. Default: '_'")
    parser.add_argument("--new_columns", nargs='+', help="Names of the new columns to create after splitting.")
    
    # Parse arguments
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = main()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_split_column"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    column_to_split = args.column_to_split if args.column_to_split else ""
    separator = args.separator if args.separator else "_"
    new_columns = args.new_columns if args.new_columns else ""
    
    # ensure merge_cols is a list
    if isinstance(new_columns, str):
        new_columns = new_columns.split()  # split string by whitespace
    elif not isinstance(new_columns, list):
        raise ValueError("new_columns must be string or list")
    
    test_mode = False

    # számítás
    while True:
        try:
            workdir_save, table_save, output_file_save, column_to_split_save, separator_save, new_columns_save = split_column_names(workdir, table, output, column_to_split, separator, new_columns, test_mode)
            break
    
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = column_to_split_save, separator_save, new_columns_save = (None,) * 3
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)

    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.column_to_split = column_to_split_save
    args.separator = separator_save
    args.new_columns = new_columns_save

    # mentés json fileba
    #new_columns_str = " ".join(args.new_columns)
    new_columns_str = " ".join(args.new_columns) if args.new_columns and isinstance(args.new_columns, list) else (args.new_columns or "")
    cmd = f"python split_column.py --workdir {args.workdir} --table {args.table} --output {args.output} --column_to_split {args.column_to_split} --separator {args.separator} --new_columns {new_columns_str}"
    save_last_command_to_json(cmd)