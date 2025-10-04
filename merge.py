import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
import autofill as autofill
from last_command import save_last_command_to_json
from autofill import HeaderCompleter, FileCompleter, WordCompleter

colorama.init()

join_type_completer = WordCompleter(autofill.merge_mode_autofill, ignore_case=True)

def mergeAny(workdir, table1, table2, output_file, tab_id1, tab_id2, mode, test_mode):

    # Path
    workdir = Path(workdir)
    table1_path = workdir / table1
    table2_path = workdir / table2
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")

    table1_file = table1
    table2_file = table2

    while True:
            try: 
                myMethods.check_table(workdir= workdir, table_file= table1_file, parameter= "table1")
                myMethods.check_table(workdir= workdir, table_file= table2_file, parameter= "table2")

                if not myMethods.validate_join_type(mode):
                    raise ValueError(f"Error invalid join type: '{mode}'. Only 'inner', 'outer', 'left', 'right' are allowed.")

                # serator  decimal meghatározás automatikusan
                sep1, dec1 = myMethods.detect_separator_and_decimal(table1_path)
                sep2, dec2 = myMethods.detect_separator_and_decimal(table2_path)

                if not myMethods.has_column(table1_path, sep1):
                    raise ValueError(f"Error --table1 has only one column, I need at least 2 column to merge")
            
                if not myMethods.has_column(table2_path, sep2):
                    raise ValueError(f"Error --table2 has only one column, I need at least 2 column to merge")

                # beolovasás                    
                table1 = pd.read_csv(str(table1_path), sep= sep1, decimal = dec1, engine='python')
                table2 = pd.read_csv(str(table2_path), sep= sep2, decimal = dec2, engine='python')

                try:
                    headers1 = table1.columns.tolist()
                    headers2 = table2.columns.tolist()
                except Exception as e:
                    headers1 = []
                    headers2 = []

                header_completer1 = HeaderCompleter(headers1)
                header_completer2 = HeaderCompleter(headers2)

                # --id1_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_string(table= table1 , table_path= table1_path, value_to_check= tab_id1, 
                                                  parameter= "tab_id1", sep= sep1, is_none_possible= False) 

                # --id2_col minden lehetséges hiba kiszűrése
                myMethods.check_everything_string(table= table2, table_path= table2_path, value_to_check= tab_id2, 
                                                  parameter= "tab_id2", sep= sep2, is_none_possible= False)               

                myMethods.blue_message("table1: ", table1)
                myMethods.blue_message("table2: ", table2)

                try:
                    if tab_id1 == tab_id2:
                    # Columns have the same name
                        df_merge = pd.merge(
                            table1, table2,
                            how=mode,
                            on=tab_id1
                        )
                    else:
                        table1.rename(columns={tab_id1: tab_id2}, inplace=True)

                        # Columns have different names
                        df_merge = pd.merge(
                            table1, table2,
                            how=mode,
                            on=tab_id2
                        )
                    if df_merge.shape[0] == 0:
                        raise ValueError(f"--table1 and --table2 IDs did not match!")

                except Exception as e:                    
                    print(colorama.Fore.RED + f"{e}")
                    print(colorama.Style.RESET_ALL)

                    if '--table1 and --table2 IDs did not match!' in str(e):  
                        #if not myMethods.is_csv_file(str(table1_path)):
                        tab_id1 = myMethods.error_handling(print_message= "Enter correct --tab_id1 column: ", 
                            completer= header_completer1)                    
                    
                        #if not myMethods.is_csv_file(str(table1_path)):
                        tab_id2 = myMethods.error_handling(print_message= "Enter correct --tab_id2 column: ", 
                            completer= header_completer2)                    
                        continue

                # mentés
                df_merge.to_csv(str(output_path), index=False, sep= "\t", decimal= ".")

                myMethods.success_message(df_merge, "merge", output_path, test_mode= test_mode)
                break  
            
            except ValueError as e:
                file_completer = FileCompleter(workdir)

                print(colorama.Fore.RED, f"{e}")
                print(colorama.Style.RESET_ALL)
                
                # Not Csv --table1 hibakezelés
                if '--table1 is not a CSV or TSV file!' in str(e):  # Check if error is related to file type
                    if not myMethods.is_csv_file(str(table1_path)):
                        table1_file = myMethods.error_handling(print_message= "Enter correct --table1: ", 
                            completer= file_completer)
                        table1_path = workdir / table1_file  
                    continue

                # Not Csv --table2 hibakezelés
                if '--table2 is not a CSV or TSV file!' in str(e):  # Check if error is related to file type
                    if not myMethods.is_csv_file(str(table2_path)):
                        table2_file = myMethods.error_handling(print_message= "Enter correct --table2: ", 
                            completer= file_completer)
                        table2_path = workdir / table2_file  
                    continue
                            
                # --table1 üres hibakezelés   
                elif '--table1 is full empty' in str(e):
                        table1_file = myMethods.error_handling(print_message= "Enter correct --table1: ", 
                            completer= file_completer)
                        table1_path = workdir / table1_file                      
                        continue

                # --table2 üres hibakezelés   
                elif '--table2 is full empty' in str(e):
                        table2_file = myMethods.error_handling(print_message= "Enter correct --table2: ", 
                            completer= file_completer)
                        table2_path = workdir / table2_file                      
                        continue
                
                # --tab_id1 hibakezelés
                elif 'as --tab_id1 column not found!' in str(e):  
                    tab_id1 = myMethods.error_handling(print_message= "Enter correct --tab_id1 column: ", 
                            completer= header_completer1)
                    continue
                
                # üres --tab_id1
                elif '--tab_id1 is empty!' in str(e): 
                    tab_id1 = myMethods.error_handling(print_message= "Enter correct --tab_id1 column: ", 
                                             completer= header_completer1) 
                    
                # --tab_id1 szám hibakezelés
                elif '--tab_id1 should not be numeric!' in str(e): 
                    tab_id1 = myMethods.error_handling(print_message= "Enter correct --tab_id1 column: ", 
                            completer= header_completer1)
                    continue
                
                # --tab_id2 hibakezelés
                elif 'as --tab_id2 column not found!' in str(e):  
                    tab_id2 = myMethods.error_handling(print_message= "Enter correct --tab_id2 column: ", 
                            completer= header_completer2)
                    continue
                
                # üres --tab_id2
                elif '--tab_id2 is empty!' in str(e): 
                    tab_id2 = myMethods.error_handling(print_message= "Enter correct --tab_id2 column: ", 
                                             completer= header_completer2) 
                    
                # --tab_id2 szám hibakezelés
                elif '--tab_id2 should not be numeric!' in str(e): 
                    tab_id2 = myMethods.error_handling(print_message= "Enter correct --tab_id2 column: ", 
                            completer= header_completer2)
                    continue

                # --table1 nem csak 1 oszlop
                elif 'Error --table1 has only one column, I need at least 2 column to merge' in str(e):
                        table_file = myMethods.error_handling(print_message= "Enter correct --table1: ", 
                            completer= file_completer)
                        table1_path = workdir / table_file                      
                        continue

                # --table2 nem csak 1 oszlop
                elif 'Error --table2 has only one column, I need at least 2 column to merge' in str(e):
                        table_file = myMethods.error_handling(print_message= "Enter correct --table2: ", 
                            completer= file_completer)
                        table2_path = workdir / table_file                      
                        continue

                # Mode inner outer, left right
                elif 'Error invalid join type' in str(e):  # Check if error is related to join type
                    if not myMethods.validate_join_type(str(mode)):
                        mode = myMethods.error_handling(print_message= "Enter correct mode 'inner', 'outer', 'left', 'right': ", 
                            completer= join_type_completer)
                        continue
                
            #--table hibakezelés
            except FileNotFoundError as e:
                file_completer = FileCompleter(workdir)

                print(colorama.Fore.RED, f"{e}")
                print(colorama.Style.RESET_ALL)
                if '--table1 file not found' in str(e):
                    if not myMethods.is_file_exists(table1_path):
                        table1_file = myMethods.error_handling(print_message= "Enter correct --table1: ", 
                                             completer= file_completer)
                        table1_path = workdir / table1_file 
                    continue  

                elif '--table2 file not found' in str(e):
                    if not myMethods.is_file_exists(table2_path):
                        table2_file = myMethods.error_handling(print_message= "Enter correct --table2: ", 
                                             completer= file_completer)
                        table2_path = workdir / table2_file 
                continue  
            
            except myMethods.BackToMainMenu:
                break
            
            except myMethods.ExitProgram:
                raise SystemExit(0) 

    return workdir, table1_file, table2_file, output_file, tab_id1, tab_id2, mode

# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Merge two tables into a single output table based on one common IDs."
                                     "This is useful for combining datasets where rows share the same identifiers.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", required=True, help= myMethods.help_workdir)
    parser.add_argument("--table1", required=True, help= myMethods.help_table)
    parser.add_argument("--table2", required=True, help= myMethods.help_table)
    parser.add_argument("--output", required=False, help= myMethods.help_output(default_output= "merged"))
    parser.add_argument("--tab_id1", required=False, default="id", help="Column ID table1 for merging. Default: id")
    parser.add_argument("--tab_id2", required=False, default="id", help="Column ID table2 for merging. Default: id")
    parser.add_argument("--mode", default="inner", help="Merge mode: inner, outer, left, right. Default: inner")

    # Parse arguments
    args = parser.parse_args()

    return args
   

if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table1_base = os.path.splitext(os.path.basename(args.table1))[0]
        table2_base = os.path.splitext(os.path.basename(args.table2))[0]
        args.output = f"{table1_base}_{table2_base}_merged"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table1 = args.table1 if args.table1 else ""
    table2 = args.table2 if args.table2 else ""
    output = args.output if args.output else ""
    tab_id1 = args.tab_id1 if args.tab_id1 else "id"
    tab_id2 = args.tab_id2 if args.tab_id2 else "id"
    mode = args.mode if args.mode else "inner"

    test_mode = False

    # számítás
    while True:
        try:
            workdir_save, table1_save, table2_save, output_file_save, tab_id1_save, tab_id2_save, mode_save = mergeAny(workdir, table1, table2, output, tab_id1, tab_id2, mode, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table1_save = table2_save = output_file_save , tab_id1_save, tab_id2_save, mode_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)
                                                                                               
    args.workdir = workdir_save
    args.table1 = table1_save
    args.table2 = table2_save
    args.output = output_file_save
    args.tab_id1 = tab_id1_save
    args.tab_id2 = tab_id2_save
    args.mode = mode_save
    
    # mentés json fileba
    cmd = f"python merge.py --workdir {args.workdir} --table1 {args.table1} --table2 {args.table2} --output {args.output} --tab_id1 {args.tab_id1} --tab_id2 {args.tab_id2} --mode {args.mode}"
    save_last_command_to_json(cmd)

 
  



