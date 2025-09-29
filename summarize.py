import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json

from autofill import HeaderCompleter, FileCompleter, WordCompleter

colorama.init()

summary_mode_completer = WordCompleter(["sum", "mean", "median", "min", "max", "main", "exit"], ignore_case=True)

def calculate_summary(workdir, table_file, output_file, name_col, value_col, group_col, summary_mode, test_mode):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")
 
    while True:
            try: 
                # check table valid
                myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
                if not myMethods.validate_summary_type(join_type = summary_mode):
                    raise ValueError(f"Error invalid summary_mode type: '{summary_mode}'. Only 'mean', 'median', 'sum', 'min', 'max' are allowed.")
                
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
                if group_col == name_col:
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error --group_col [{group_col}] and --name_col [{name_col}] are the same, please modify --name_col and --group_col")
                
                myMethods.blue_message("table: ", table)
                
                # számolás
                df_summary = myMethods.def_calculate_summarize(table, name_col, group_col, value_col, summarize_mode= summary_mode)

                # mentés
                df_summary.to_csv(str(output_path), index=False, sep= "\t", decimal= ".")

                myMethods.success_message(df_summary, "summary", output_path, test_mode= test_mode)
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
                

                # --name_col hibakezelés
                elif 'as --name_col column not found!' in str(e):  
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer)
                    continue

                # üres --name_col
                elif '--name_col is empty!' in str(e): 
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer) 
                    
                # --name_col szám hibakezelés
                elif '--name_col should not be numeric!' in str(e): 
                    name_col = myMethods.error_handling(print_message= "Enter correct --name_col column: ", 
                                             completer= header_completer)
                    continue
                
                # --value_col hibakezelés
                if '--value_col column not found!' in str(e):
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer)
                    continue
                
                # üres --value_col
                elif '--value_col is empty!' in str(e): 
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer) 
                    continue
                
                 # --value_col nem szám hibakezelés
                elif '--value_col should be numeric!' in str(e):
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer)
                    continue

                 # --group_col hibakezelés
                elif '--group_col column not found!' in str(e):
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer)
                    continue
                
                # üres --group_col
                elif '--group_col is empty!' in str(e): 
                    group_col = myMethods.error_handling(print_message= "Enter correct --group_col column: ", 
                                             completer= header_completer) 
                    continue
                
                 # --group_col number hibakezelés
                elif '--group_col should not be numeric!' in str(e):
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
                
                # summary mode mean, median sum min max
                elif 'Error invalid summary_mode type: ' in str(e):  # Check if error is related to join type
                    if not myMethods.validate_summary_type(str(summary_mode)):
                        summary_mode = myMethods.error_handling(print_message= "Enter correct summary_mode type:  'mean', 'median', 'sum', 'min', 'max: ", 
                            completer= summary_mode_completer)
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

    return workdir, table_file, output_file, name_col, value_col, group_col, summary_mode

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Calculate the summary (mean, median, sum, min, max), for any names in any groups!",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", required=True, help= myMethods.help_workdir)
    parser.add_argument("--table", required=True, help= myMethods.help_table)
    parser.add_argument("--output", required=False, help= myMethods.help_output(default_output= "stat_output"))
    parser.add_argument("--name_col", required=False, default="id", help= myMethods.help_name(default_name= "id"))
    parser.add_argument("--value_col", required=False, default="value", help= myMethods.help_value(default_value= "value"))
    parser.add_argument("--group_col", required=False, default="group", help= myMethods.help_group(default_group= "group"))
    parser.add_argument("--summary_mode", required=False, default="sum", help="Summary mode (mean, median, sum, min, max)")

    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_summary"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    name_col = args.name_col if args.name_col else "id"
    value_col = args.value_col if args.value_col else "value"
    group_col = args.group_col if args.group_col else "group"
    summary_mode = args.summary_mode if args.summary_mode else "sum"

    test_mode = False

    # számítás és hiba kezelés
    while True:
        try:
            workdir_save, table_save, output_file_save, name_col_save, value_col_save, group_col_save, summary_mode_save = calculate_summary(workdir, table, output, name_col, value_col, group_col, summary_mode, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = name_col_save = value_col_save = group_col_save = summary_mode_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)
        
    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.value_col = value_col_save
    args.summary_mode = summary_mode_save

    if group_col not in ["none", "NONE", "None"]: 
            args.group_col = group_col_save
    else:
            args.group_col = "none"

    if name_col not in ["none", "NONE", "None"]:
            args.name_col = name_col_save
    else:
            args.name_col = "none"
    
    # mentés json fileba
    cmd = f"python summarize.py --workdir {args.workdir} --table {args.table} --output {args.output} --name_col {args.name_col} --value_col {args.value_col} --group_col {args.group_col} --summary_mode {args.summary_mode}"
    save_last_command_to_json(cmd)

 
  



