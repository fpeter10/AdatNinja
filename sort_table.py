import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json

from autofill import MultiHeaderCompleter, FileCompleter, WordCompleter
import autofill as autofill

colorama.init()

settings = myMethods.get_local_settings()
language = settings["language"]
decimal = settings["decimal"]

sort_mode_completer = WordCompleter(autofill.sort_mode_autofill, ignore_case=True)

def sort_table(workdir, table_file, output_file, keys, sort_mode, test_mode):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")
 
    while True:
            try: 
                # check table valid
                myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
                if not myMethods.validate_sort_mode(sort_mode= sort_mode):
                    raise ValueError(f"Error invalid sort_mode type: '{sort_mode}'. Only 'decreasing', 'increasing' are allowed.")
                
                # sepator  decimal meghatározás automatikusan
                sep, dec = myMethods.detect_separator_and_decimal(table_path)

                # beolovasás                    
                table = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')

                try:
                    headers = table.columns.tolist()
                except Exception as e:
                    headers = []

                multi_header_completer = MultiHeaderCompleter(headers)

                if isinstance(keys, str):
                    keys = keys.split()
                
                # Check if all columns exist
                missing = [k for k in keys if k not in table.columns]
                if missing:
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Column(s) not found in table: {missing}, please use just actual columns!")
                
                # Check that column types are not mixed
                for k in keys:
                    series = table[k]
                    if myMethods.has_mixed_column2(series):
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Column '{k}' has mixed data types, please use consistent columns!")
                    if series.isna().any():  # check for missing
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Column '{k}' contains missing values!")

                myMethods.blue_message("table: ", table)
                
                # számolás
                df_sorted = myMethods.def_sort_table_by_keys(table, sort_mode= sort_mode, keys= keys)

                #save to csv
                myMethods.safe_to_csv(table= df_sorted, output_path= output_path, separator= "\t", decimal= decimal)

                myMethods.success_message(df_sorted, "sorted", output_path, test_mode= test_mode)
                break  
            
            except ValueError as e:
                file_completer = FileCompleter(workdir)

                print(colorama.Fore.RED, f"{e}")
                print(colorama.Style.RESET_ALL)
                
                # Not Csv hibakezelés
                if '--table is not a CSV or TSV file' in str(e):  # Check if error is related to file type
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
                
               
                elif " Only 'decreasing', 'increasing' are allowed." in str(e):  # Check if error is related to separator
                    if not myMethods.validate_sort_mode(str(sort_mode)):
                        sort_mode = myMethods.error_handling(print_message= "Enter correct separator : 'decreasing' or 'incresing'", 
                                completer= sort_mode_completer)
                        continue
                    
                
                # --key nem létezik hibakezelés
                elif 'Column(s) not found in table:' in str(e):  
                    keys = myMethods.error_handling(print_message= "Enter correct --keys column: ", 
                                    completer= multi_header_completer)
                    continue
                
                # --key típusa nem egységes hibakezelés
                elif 'has mixed data types, please use consistent columns!' in str(e):  
                    keys = myMethods.error_handling(print_message= "Enter correct --keys column: ", 
                                    completer= multi_header_completer)
                    continue
                
                
                # --key-be NAn van hibakezelés
                elif 'contains missing values!' in str(e):  
                    keys = myMethods.error_handling(print_message= "Enter correct --keys column: ", 
                                    completer= multi_header_completer)
                    continue
                
                # --key duplázás hibakezelés
                elif 'Duplicate key(s) found:' in str(e):  
                    keys = myMethods.error_handling(print_message= "Enter correct --keys column: ", 
                                    completer= multi_header_completer)
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

    return workdir, table_file, output_file, keys, sort_mode

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Sort data in the table based on multiple keys.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output", help= myMethods.help_output(default_output= "_sorted"))
    parser.add_argument("--keys", nargs='+', help= "Give keys")
    parser.add_argument("--sort_mode", default= "decreasing", help= "Decreasing or increasing order")

    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_sorted"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    sort_mode = args.sort_mode if args.sort_mode else "decreasing"
    keys = args.keys if args.keys else ""
    
    # ensure merge_cols is a list
    if isinstance(keys, str):
        keys = keys.split()  # split string by whitespace
    elif not isinstance(keys, list):
        raise ValueError("keys must be string or list")
    
    test_mode = False

    # számítás és hiba kezelés
    while True:
        try:
            workdir_save, table_save, output_file_save, keys_save, sort_mode_save  = sort_table(workdir, table, output, keys, sort_mode, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = keys_save = sort_mode_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)
        
    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.keys = keys_save
    args.sort_mode = sort_mode_save

    # mentés json fileba
    keys_str = " ".join(args.keys) if args.keys and isinstance(args.keys, list) else (args.keys or "")
    cmd = f"python sort_table.py --workdir {args.workdir} --table {args.table} --output {args.output} --keys {keys_str} --sort_mode {args.sort_mode}"
    save_last_command_to_json(cmd)

 
  



