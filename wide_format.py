import os
import pandas as pd
import argparse
import colorama
from pathlib import Path
import methods as myMethods
from last_command import save_last_command_to_json
from methods import type_print
from prompt_toolkit import prompt
from autofill import HeaderCompleter, MultiHeaderCompleter, FileCompleter

colorama.init()

settings = myMethods.get_local_settings()
language = settings["language"]
decimal = settings["decimal"]

def wide_format(workdir, table_file, output_file, value_col, sample_col, id_col, test_mode):

    # Path
    workdir = Path(workdir)
    table_path = workdir / table_file
    output_path = workdir / (output_file if output_file.lower().endswith(".csv") else f"{output_file}.csv")
    
    # --- Normalize id_col to always be a list ---
    if isinstance(id_col, str):
        id_col_list = [c.strip() for c in id_col.split() if c.strip()]
    elif isinstance(id_col, list):
        id_col_list = [str(c).strip() for c in id_col if str(c).strip()]

    while True:
        try:
            # check table valid
            myMethods.check_table(workdir= workdir, table_file= table_file, parameter= "table")
                
            # Detect separator & decimal
            sep, dec = myMethods.detect_separator_and_decimal(table_path)

            # Read table
            table = pd.read_csv(str(table_path), sep=sep, decimal=dec, engine='python')

            try:
                headers = table.columns.tolist()
            except Exception as e:
                headers = []

            multi_header_completer = MultiHeaderCompleter(headers)
            header_completer = HeaderCompleter(headers)
            
            # Split ID columns
            id_col_list = [c.strip() for c in id_col]
            
            duplicates = [c for c in set(id_col_list) if id_col_list.count(c) > 1]
            if duplicates:
                raise ValueError(f"Error: duplicate columns in --id_col: {', '.join(duplicates)}")
            
            for col in id_col_list:
                if col not in table.columns:
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error [{col}] --id_col column not found!")
                if pd.api.types.is_numeric_dtype(table[col]):
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error [{col}] --id_col column should not be numeric!")
                
                series = table[col]
                if myMethods.has_mixed_column2(series):
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Column '{col}' has mixed data types, please use consistent columns!")
                if series.isna().any():  # check for missing
                        myMethods.list_available_columns(str(table_path), sep)
                        raise ValueError(f"Column '{col}' contains missing Nan values!")

            # --value_col minden lehetséges hiba kiszűrése
            myMethods.check_everything_number(table= table, table_path= table_path, value_to_check= value_col, 
                                                  parameter= "value_col", sep= sep)                
            
            # --sample_col minden lehetséges hiba kiszűrése
            myMethods.check_everything_string(table= table, table_path= table_path, value_to_check= sample_col, 
                                                  parameter= "sample_col", sep= sep, is_none_possible= False)
                    
            for col in id_col_list:
                if col == sample_col:
                    myMethods.list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error [{col}] id_col and sample_col can not be the same!")        
            
            
            myMethods.blue_message("table: ", table)
            
            # Pivot table
            df_wide = table.pivot_table(
                index=id_col_list,
                columns=sample_col,
                values=value_col,
                aggfunc="first"
            ).reset_index()

            # Flatten columns if needed
            if isinstance(df_wide.columns, pd.MultiIndex):
                df_wide.columns = [
                    '_'.join([str(i) for i in col if i]) for col in df_wide.columns.values
                ]

            #save to csv
            myMethods.safe_to_csv(table= df_wide, output_path= output_path, separator= "\t", decimal= decimal)

            myMethods.success_message(df_wide, "wide_format", output_path, test_mode=test_mode)
            break

        except Exception as e:
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

            # id_col léteznie kell
            elif "--id_col column not found!" in str(e):
                type_print("Enter existing id_cols: ", color = colorama.Fore.LIGHTCYAN_EX)
                id_col = prompt("", completer=multi_header_completer).strip()
                myMethods.check_exit(id_col)
                id_col = [col.strip() for col in id_col.split() if col.strip()]
                continue

            # id_col nem lehet szám
            elif "--id_col column should not be numeric!" in str(e):
                type_print("Enter existing id_cols: ", color = colorama.Fore.LIGHTCYAN_EX)
                id_col = prompt("", completer=multi_header_completer).strip()
                myMethods.check_exit(id_col)
                id_col = [col.strip() for col in id_col.split() if col.strip()]
                continue
            
            # id_col Nan -t tartalmaz
            elif "contains missing Nan values!" in str(e):
                type_print("Enter correct id_cols: ", color = colorama.Fore.LIGHTCYAN_EX)
                id_col = prompt("", completer=multi_header_completer).strip()
                myMethods.check_exit(id_col)
                id_col = [col.strip() for col in id_col.split() if col.strip()]
                continue
            
            # id_col MIX
            elif "has mixed data types, please use consistent columns!" in str(e):
                type_print("Enter correct id_cols: ", color = colorama.Fore.LIGHTCYAN_EX)
                id_col = prompt("", completer=multi_header_completer).strip()
                myMethods.check_exit(id_col)
                id_col = [col.strip() for col in id_col.split() if col.strip()]
                continue
            
            # id_col nem lehet duplikátum
            elif "duplicate columns in --id_col" in str(e):
                type_print("Enter id_cols, the same --id_cols prohibited: ", color = colorama.Fore.LIGHTCYAN_EX)
                id_col = prompt("", completer=multi_header_completer).strip()
                myMethods.check_exit(id_col)
                id_col = [col.strip() for col in id_col.split() if col.strip()]
                continue
            
            # --value nem létezik   
            elif '--value_col column not found!' in str(e):
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                            completer= header_completer)
                    continue
            
            # teljes üres adatok --value_col
            elif '--value_col is empty!' in str(e): 
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer) 
                    continue
                
            # üres értékek Nan --value_col
            elif '--value_col contains Nan values!' in str(e): 
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer) 
                    continue

            # --value nem szám   
            elif '--value_col should be numeric!' in str(e):
                    value_col = myMethods.error_handling(print_message= "Enter correct --value_col column: ", 
                                             completer= header_completer)
                    continue

             # --sample_col nem létezik   
            elif '--sample_col column not found!' in str(e):
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                        completer= header_completer)
                    continue
            
            # --sample_col üres   
            elif '--sample_col is empty!' in str(e):
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                        completer= header_completer)
                    continue
            
            # --sample_col üres   
            elif '--sample_col contains Nan values!' in str(e):
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                        completer= header_completer)
                    continue
            
            elif '--sample_col has mixed data types, please use consistent columns!' in str(e): 
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                             completer= header_completer)
                    continue

            # --sample_col nem szám   
            elif '--sample_col should not be numeric!' in str(e):
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                        completer= header_completer)
                    continue
            
            elif 'id_col and sample_col can not be the same!' in str(e):
                    type_print("Enter both id_cols and sample_col!")
                    type_print("Enter existing id_cols: ", color = colorama.Fore.LIGHTCYAN_EX)
                    id_col = prompt("", completer=multi_header_completer).strip()
                    myMethods.check_exit(id_col)
                    id_col = [col.strip() for col in id_col.split() if col.strip()]                    
                    
                    sample_col = myMethods.error_handling(print_message= "Enter correct --sample_col column: ", 
                                        completer= header_completer)
                    continue
            
        #--table hibakezelés
        except FileNotFoundError as e:
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
        
    return workdir, table_file, output_file, id_col, value_col, sample_col


# MAIN
def parse_stat():
    parser = argparse.ArgumentParser(description="Convert a long-format table into wide format.",
                                     formatter_class=myMethods.SingleLineFormatter)
    parser.add_argument("--workdir", required=True, help= myMethods.help_workdir)
    parser.add_argument("--table", required=True, help= myMethods.help_table)
    parser.add_argument("--output", required=False, help= myMethods.help_output(default_output= "wide"))
    parser.add_argument("--id_col", required=True, nargs='+', help="One or more column name used as identifiers/groups for wide format. Default: id")
    parser.add_argument("--value_col", help= myMethods.help_value(default_value= "value"))
    parser.add_argument("--sample_col", required=True, help="Column whose unique values become new column headers in the wide table. (Names of the samples)")
    # Parse arguments
    args = parser.parse_args()

    return args
   
if __name__ == "__main__":
    args = parse_stat()

    #  alapértelmezett név ha nincs bemeent
    if not args.output:
        table_base = os.path.splitext(os.path.basename(args.table))[0]
        args.output = f"{table_base}_wide"

    # alapértelmezett név
    workdir = args.workdir if args.workdir else ""
    table = args.table if args.table else ""
    output = args.output if args.output else ""
    id_col = args.id_col if args.id_col else "id"
    value_col = args.value_col if args.value_col else "value"
    sample_col = args.sample_col if args.sample_col else ""
    
    # ensure merge_cols is a list
    if isinstance(id_col, str):
        merge_cols = id_col.split()  # split string by whitespace
    
    test_mode = False

    # számítás
    while True:
        try:
            workdir_save, table_save, output_file_save, id_col_save, value_col_save, sample_col_save = wide_format(workdir, table, output, value_col, sample_col, id_col, test_mode)
            break
        
        except myMethods.BackToMainMenu:
            workdir_save = table_save = output_file_save = id_col_save = value_col_save = sample_col_save = None
            break  # loop back to menu
        
        except myMethods.ExitProgram:
            raise SystemExit(0)

    args.workdir = workdir_save
    args.table = table_save
    args.output = output_file_save
    args.value_col = value_col_save
    args.id_col = id_col_save
    args.sample_col = sample_col_save
    
    # mentés json fileba
    #id_col_str = " ".join(id_col_save)
    id_col_str = " ".join(args.id_col) if args.id_col and isinstance(args.id_col, list) else (args.id_col or "")
    cmd = f"python wide_format.py --workdir {args.workdir} --table {args.table} --output {args.output} --id_col {id_col_str} --value_col {args.value_col} --sample_col {args.sample_col}"
    save_last_command_to_json(cmd)