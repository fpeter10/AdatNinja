import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json

from autofill import FileCompleter, WordCompleter
import autofill as autofill

colorama.init()

separator_completer = WordCompleter(autofill.new_separator_autofill, ignore_case=True)
decimal_completer = WordCompleter(autofill.new_decimal_autofill, ignore_case=True)

def change_sep(workdir, table_file, output_file, separator, dececimal, test_mode):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")
 
    while True:
            try: 
                # check table valid
                myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
                # sepator  decimal meghatározás automatikusan
                sep, dec = myMethods.detect_separator_and_decimal(table_path)

                # beolovasás                    
                table = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')

                
                
                separator_map = {
                    "tab": "\t",
                    "semicolon": ";",
                    "colon": ",",
                    "pipe": "|"}

                decimal_map = {
                    "colon": ",",
                    "point": "."}

                # map user input to actual character
                separator = separator_map.get(separator, separator)
                dececimal = decimal_map.get(dececimal, dececimal)

                if not myMethods.validate_sep(separator):
                    raise ValueError(f"Invalid separator {separator}, choose from: tab, semicolon, colon, pipe")
                
                if not myMethods.validate_dec(dececimal):
                    raise ValueError(f"Invalid decimal separator {dececimal}, choose from: colon, point")

                # mentés
                table.to_csv(str(output_path), index=False, sep= separator, decimal= dececimal)

                myMethods.success_message(table, "changed sep", output_path, test_mode= test_mode)
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
                

                
                # separator
                elif "Invalid separator" in str(e):  # Check if error is related to join type
                    if not myMethods.validate_sep(str(separator)):
                        separator = myMethods.error_handling(print_message= "Enter correct separator: ", 
                            completer= separator_completer)
                        continue
                    
                # decimal
                elif "Invalid decimal separator" in str(e):  # Check if error is related to join type
                    if not myMethods.validate_dec(str(dececimal)):
                        dececimal = myMethods.error_handling(print_message= "Enter correct separator: ", 
                            completer= decimal_completer)
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

    return workdir, table_file, output_file, separator, dececimal

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Change the separator and decimal in a table!",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output", help= myMethods.help_output(default_output= "_sep_changed"))
    parser.add_argument("--sep", default="\t", help="Separator, choose from tab, semicolon, colon. Default: tab")
    parser.add_argument("--dec", default=".", help="Decimal, choose from colon and point. Default: point")

    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_sep_changed"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    separator = args.sep if args.sep else "\t"
    dececimal = args.dec if args.dec else "."
    
    test_mode = False

    # számítás és hiba kezelés
    while True:
        try:
            workdir_save, table_save, output_file_save, sep_save, dec_save = change_sep(workdir, table, output, separator, dececimal, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = sep_save = dec_save  = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)
        
    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.separator = sep_save
    args.dececimal = dec_save

    # mentés json fileba
    cmd = f"python change_sep.py --workdir {args.workdir} --table {args.table} --output {args.output} --sep {args.separator} --dec {args.dececimal}"
    save_last_command_to_json(cmd)

 
  



