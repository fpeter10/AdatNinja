import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json
from methods import type_print
from autofill import HeaderCompleter, FileCompleter

colorama.init()

def relativize_columns(workdir, table_file, output_file, group_col, sum_value, test_mode):

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

                try:
                    headers = table.columns.tolist()
                except Exception as e:
                    headers = []

                header_completer = HeaderCompleter(headers)
                
                # --group_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_string(table= table, table_path= table_path, value_to_check= group_col, 
                                                  parameter= "group_col", sep= sep, is_none_possible= True)
       
                # sum szám legyen
                try:
                    float(sum_value)
                except ValueError:
                    raise ValueError(f"Error {sum_value} as --sum_value is not numeric!")
                
                if group_col is None or str(group_col).lower() == "none":
                    group_col = None  # globális mód
                
                else:
                    if isinstance(group_col, str):
                        group_col = [group_col]

                    missing_cols = [col for col in group_col if col not in table.columns]
                    if missing_cols:
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Error {group_col} --group_col column not found!")

                
                    # ha szám a --group_col
                    numeric_cols = [col for col in group_col if pd.api.types.is_numeric_dtype(table[col])]
                    if numeric_cols:
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Error {group_col} --group_col should not be numeric!")

                myMethods.blue_message("table: ", table)
            
                    # Perform statistics
                df_relative = myMethods.def_relative_columns(df= table, groupby_cols= group_col, sum_value = sum_value)
                    
                    # Save merged DataFrame
                df_relative.to_csv(str(output_path), index=False, sep= "\t",  decimal = ".")

                myMethods.success_message(df_relative, "relative", output_path,  test_mode= test_mode)
                break  # Exit loop on success
            
            except ValueError as e:
                file_completer = FileCompleter(workdir)

                print(colorama.Fore.RED, f"{e}")
                print(colorama.Style.RESET_ALL)
                if '--table is not a CSV or TSV file' in str(e):  # Check if error is related to file type
                    if not myMethods.is_csv_file(str(table_path)):
                        if not myMethods.is_csv_file(str(table_path)):
                            table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                             completer= file_completer)
                            table_path = workdir / table_file
                        continue
                    
                    
                elif '--table is full empty' in str(e):  # Check if table is empty
                    table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                             completer= file_completer)
                    table_path = workdir / table_file                    
                    continue

                
                elif 'as --sum_value is not numeric!' in str(e):  
                    sum_value = myMethods.error_handling(print_message= "Enter correct --sum_value: ", 
                                             completer= header_completer)
                    continue
                    
                # --group_col hibakezelés
                elif '--group_col column not found!' in str(e):  
                    type_print(f"If you do not need --group_col type none!")
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue

                # --group_col szám hibakezelés
                elif '--group_col should not be numeric!' in str(e): 
                    type_print(f"If you do not need --group_col type none!")
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue
                
            except FileNotFoundError as e:
                file_completer = FileCompleter(workdir)
                
                print(colorama.Fore.RED, f"{e}")
                print(colorama.Style.RESET_ALL)
                if '--table file not found' in str(e):
                    if not myMethods.is_file_exists(table_path):
                        table_file = myMethods.error_handling(print_message= "Enter correct table: ", 
                                    completer= file_completer)
                        table_path = workdir / table_file  
                continue  # Only ask for file paths again
            
            except myMethods.BackToMainMenu:
                break
            
            except myMethods.ExitProgram:
                raise SystemExit(0)             

    return workdir, table_file, output_file, group_col, sum_value

def parse_stat():
    parser = argparse.ArgumentParser(description="Calculate the relative values, in a group with the sum of --sum_value",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", required=True, help= myMethods.help_workdir)
    parser.add_argument("--table", required=True, help= myMethods.help_table)
    parser.add_argument("--output", required=True, help= myMethods.help_output(default_output= "relative"))
    parser.add_argument("--group_col", help= myMethods.help_group(default_group= "group"))
    parser.add_argument("--sum_value", help="Sum of the values in one group, e.g.: 1, 100")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs kimeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_relative"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    group_col = args.group_col if args.group_col else "None"
    sum_value = args.sum_value if args.sum_value else 1

    test_mode = False

    # számítás és hiba kezelés
    while True:
        try:
            workdir_save, table_save, output_file_save, group_col_save, sum_value_save = relativize_columns(workdir, table, output, group_col, sum_value, test_mode)
            break
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = sum_value_save  = group_col_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)

    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.sum_value = sum_value_save

    if group_col not in ["none", "NONE", "None"]: 
        if isinstance(group_col_save, list) and len(group_col_save) == 1:
            args.group_col = group_col_save[0]
        else:
            args.group_col = group_col_save
    else:
        args.group_col = "none"

    # mentés json fileba
    cmd = f"python relative.py --workdir {args.workdir} --table {args.table} --output {args.output} --group_col {str(args.group_col)} --sum_value {args.sum_value}"
    save_last_command_to_json(cmd)


