import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json
from autofill import FileCompleter

colorama.init()

def print_table(workdir, table_file):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
 
    while True:
            try: 
                # check table valid
                myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
                # serator  decimal meghatározás automatikusan
                sep, dec = myMethods.detect_separator_and_decimal(table_path)

                # beolovasás                    
                table = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')
                
                myMethods.blue_message("table: ", table)
                myMethods.list_available_columns(str(table_path), sep)

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

    return workdir, table_file

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Print the table to check content, headers", 
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", required=True, help= myMethods.help_workdir)
    parser.add_argument("--table", required=True, help= myMethods.help_table)

    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    
    # számítás
    while True:
        try:
            workdir_save, table_save, = print_table(workdir, table)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = None
            break
            
        except myMethods.ExitProgram:
            raise SystemExit(0)  

    args.workdir = workdir_save
    args.table = table_save
    
    # mentés json fileba
    cmd = f"python print_table.py --workdir {args.workdir} --table {args.table}"
    save_last_command_to_json(cmd)

 
  



