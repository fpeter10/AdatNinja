import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json
from autofill import FileCompleter

colorama.init()

def long_format(workdir, table_file, output_file, test_mode):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")
 
    while True:
            try: 
                myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
                # sepator  decimal meghatározás automatikusan
                sep, dec = myMethods.detect_separator_and_decimal(table_path)

                # beolovasás                    
                table = pd.read_csv(str(table_path), sep= sep, decimal = dec, engine='python')

                dangerous_column = [col for col in table.columns if myMethods.has_mixed_column2(table[col])]

                if dangerous_column:
                    print(colorama.Fore.RED, f"Warning there is {dangerous_column} column with both numeric and non numeric data, please check file!")
                    break

                id_vars = table.select_dtypes(exclude='number').columns.tolist()

                if 'value' in table.columns:
                    print(colorama.Fore.RED, "Table can not contain ['value'] column. Check file!")
                    break
                
                # számolás
                else:
                    myMethods.blue_message("table: ", table)
                    df_long_format = pd.melt(table, id_vars= id_vars)

                # mentés
                df_long_format.to_csv(str(output_path), index=False, sep= "\t", decimal= dec)

                myMethods.success_message(df_long_format, "long format", output_path, test_mode= test_mode)
                break  
            
            except ValueError as e:
                file_completer = FileCompleter(workdir)

                print(colorama.Fore.RED, f"{e}")
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

    return workdir, table_file, output_file#, id_col

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Convert a wide format file into long format. It is required for AdatNinja to handle data.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output", help= myMethods.help_output(default_output= "_long_format"))

    # Parse arguments
    args = parser.parse_args()

    return args
   

if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_long_format"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""

    test_mode = False

    # számítás
    while True:
        try:
            workdir_save, table_save, output_file_save = long_format(workdir, table, output, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)

    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    
    # mentés json fileba
    cmd = f"python long_format.py --workdir {args.workdir} --table {args.table} --output {args.output}"
    save_last_command_to_json(cmd)

 
  



