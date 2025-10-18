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

settings = myMethods.get_local_settings()
language = settings["language"]
decimal = settings["decimal"]

def calculate_normality_test(workdir, table_file, output_file, name_col, value_col, group_col, test_mode):

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

                try:
                    headers = table.columns.tolist()
                except Exception as e:
                    headers = []

                header_completer = HeaderCompleter(headers)

                # --name_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_string(table= table, table_path= table_path, value_to_check= name_col, 
                                                  parameter= "name_col", sep= sep, is_none_possible= True)
                
                # --value_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_number(table= table, table_path= table_path, value_to_check= value_col, 
                                                  parameter= "value_col", sep= sep)                
           

                # --group_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_string(table= table, table_path= table_path, value_to_check= group_col, 
                                                  parameter= "group_col", sep= sep, is_none_possible= True)
                                
                # Nem lehet egyforma a --name és --group                
                if group_col == name_col and group_col != "none" and name_col != "none":
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error --group_col [{group_col}] and --name_col [{name_col}] are the same, please modify --name_col and --group_col")
                
                myMethods.blue_message("table: ", table)
                
                # számolás
                df_test = myMethods.calculate_shapiro(table, name_col, group_col, value_col)

                #save to csv
                myMethods.safe_to_csv(table= df_test, output_path= output_path, separator= "\t", decimal= decimal)

                myMethods.success_message(df_test, "normality_test", output_path, test_mode= test_mode)
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

                # --name_col hibakezelés
                elif 'as --name_col column not found!' in str(e):  
                    type_print(f"If you do not need --name_col type none!")
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                completer= header_completer)
                    continue
                
                # üres --name_col
                elif '--name_col is empty!' in str(e): 
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer) 
                    
                # üres értékek Nan --name_col
                elif '--name_col contains Nan values!' in str(e): 
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer) 
                    continue
                
                
                # --name_col szám hibakezelés
                elif '--name_col should not be numeric!' in str(e): 
                    type_print(f"If you do not need --name_col type none!")
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                completer= header_completer)                    
                    continue
                
                elif '--name_col has mixed data types, please use consistent columns!' in str(e): 
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer)
                    continue

                # --value_col hibakezelés
                elif 'as --value_col column not found!' in str(e):
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                completer= header_completer)
                    continue 

                # üres --value_col
                elif '--value_col is empty!' in str(e): 
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer) 
                    continue  

                # üres értékek Nan --value_col
                elif '--value_col contains Nan values!' in str(e): 
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer) 
                    continue                 
                
                # --value_col nem szám hibakezelés
                elif ' --value_col should be numeric!' in str(e):
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                completer= header_completer)
                    continue 
                                 
                # --group_col hibakezelés
                elif '--group_col column not found!' in str(e):
                    type_print(f"If you do not need --group_col type none!")
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue 
                
                # üres --group_col
                elif '--group_col is empty!' in str(e): 
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer) 
                    continue
                
                # üres adatok Nan --group_col
                elif '--group_col contains Nan values!' in str(e): 
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer) 
                    continue
                
                elif '--group_col has mixed data types, please use consistent columns!' in str(e): 
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue

                # --group_col szám hibakezelés
                elif '--group_col should not be numeric!' in str(e):
                    type_print(f"If you do not need --group_col type None!")
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue                     
                
                # ugyanaz --name_col --group_col hiba
                elif 'are the same, please modify --name_col and --group_col' in str(e):
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer)
                    
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    
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

    return workdir, table_file, output_file, name_col, value_col, group_col

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Calculate if data is normally distributed in names and groups.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", help= myMethods.help_workdir)
    parser.add_argument("--table", help= myMethods.help_table)
    parser.add_argument("--output",  help= myMethods.help_output(default_output= "_normality_test_output"))
    parser.add_argument("--name_col",  help= myMethods.help_name(default_name= "id"))
    parser.add_argument("--value_col", help= myMethods.help_value(default_value= "value"))
    parser.add_argument("--group_col", help= myMethods.help_group(default_group= "group"))

    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_normality_test_output"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    name_col = args.name_col if args.name_col else "id"
    value_col = args.value_col if args.value_col else "value"
    group_col = args.group_col if args.group_col else "group"

    test_mode = False

    # számítás
    while True:
        try:
            workdir_save, table_save, output_file_save, name_col_save, value_col_save, group_col_save = calculate_normality_test(workdir, table, output, name_col, value_col, group_col, test_mode)
            break
         
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = name_col_save = value_col_save = group_col_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)

    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.value_col = value_col_save

    if group_col not in ["none", "NONE", "None"]: 
            args.group_col = group_col_save
    else:
            args.group_col = "none"

    if name_col not in ["none", "NONE", "None"]:
            args.name_col = name_col_save
    else:
            args.name_col = "none"
    
    # mentés json fileba
    cmd = f"python normality.py --workdir {args.workdir} --table {args.table} --output {args.output} --name_col {args.name_col} --value_col {args.value_col} --group_col {args.group_col}"
    save_last_command_to_json(cmd)

 
  



