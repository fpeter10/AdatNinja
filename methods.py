import os
import sys
import re
from datetime import datetime
import time
import random
import colorama
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations
from prompt_toolkit import prompt
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind
from scipy.stats import shapiro
from prompt_toolkit.completion import WordCompleter
import autofill as autofill

def type_print(text, test_mode = False, color=colorama.Fore.WHITE, base_speed=0.01):
    if test_mode == True:
        print(text)  # Standard print for test capture
        
    for line in text.splitlines():
        for char in line:
            sys.stdout.write(f"{color}{char}{colorama.Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(base_speed + random.uniform(0, base_speed * 5))
        print()

def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 9:
        return "Good morning"
    elif 9 <= current_hour < 18:
        return "Have a nice day"
    elif 18 <= current_hour < 23:
        return "Good evening"
    else:
        return "It is late, better to sleep!"

def get_user_name(filename="user.txt"):
    try:
        with open(filename, "r") as file:
            name = file.read().strip()
            if name:
                return name
    except FileNotFoundError:
        pass
    
    text = f"Hello, thank you for downloading me, I am AdatNinja to handle your data like a true Ninja. Please enter your name: "
    type_print(text)
    name = input("Name: ").strip()
    with open(filename, "w") as file:
        file.write(name)
    return name

language_autofill = WordCompleter(autofill.language_autofill, ignore_case=True)

def save_language(filename="language.txt", force = False):
    valid_languages = {"English", "Magyar"}

    if not force:
        # Try reading existing language file
        try:
            with open(filename, "r", encoding="utf-8") as file:
                language = file.read().strip().capitalize()
                if language in valid_languages.values():
                    return language
        except FileNotFoundError:
            pass  # No file yet, proceed to prompt user
        
    type_print(f"Choose between English or Magyar settings. "\
                   "This will affect formatting options: decimal separator (comma vs. point).", color= colorama.Fore.CYAN)
        
    while True:
        language_input = prompt("Language: ", completer=language_autofill).strip()
        check_exit(language_input)

        if language_input in valid_languages:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(language_input)
            type_print(f"Language set to: {language_input}")
            return language_input
        else:
            type_print("Invalid input. Please type 'English' or 'Magyar'.", color= colorama.Fore.RED)
            print(colorama.Style.RESET_ALL)


def list_functions():
    functions = ["mergeAny"]
    return "\n".join(f"{i}. {func}" for i, func in enumerate(functions, start=1))
    

def welcome():
    name = get_user_name()
    greeting = get_greeting()
    current_time = datetime.now().strftime("%H:%M:%S")
    current_day = datetime.now().strftime("%A, %B %d, %Y")
    
    text = f"I am AdatNinja, here to assist you with data like a true Ninja. {greeting}, {name}! Today is: {current_day}. The time is: {current_time}."
    type_print(text, color= colorama.Fore.WHITE)


def success_message(table, method, output_path, test_mode):
      """
      Print succes for user with green\n
      Parameter: name of table\n
      """
      type_print(f"Success! {method} file saved as {output_path}", color = colorama.Fore.GREEN, test_mode= test_mode)
      type_print(str(table.head(5)), color = colorama.Fore.GREEN, base_speed = 0.001)

      print("-----------")

def blue_message(message, table):
      """
      Print table for user with nice blue\n
      Parameter1: message\n
      Parameter2: name of table\n
      """
      type_print(message, color= colorama.Back.BLUE)
      type_print(str(table.head(3)), color= colorama.Fore.BLUE, base_speed = 0.001)

      print("-----------")

class BackToMainMenu(Exception):
    pass
class ExitProgram(Exception):
    pass

def check_exit (variable: str, in_error_handling: bool = False):
    if variable.lower() == "main":
        type_print("Back to main menu...", color = colorama.Fore.YELLOW)
        raise BackToMainMenu()
    
    elif variable.lower() == "exit":
        if in_error_handling:
            type_print("Exit program to main, type again exit", color = colorama.Fore.YELLOW)
            raise BackToMainMenu()
        
        else:
            type_print("Exit program...", color = colorama.Fore.YELLOW)
            raise SystemExit(0)


def is_csv_file(file_path):
    """Check if the file is a CSV or TSV."""
    _, file_extension = os.path.splitext(file_path.lower())
    return file_extension in [".csv", ".tsv"]


def detect_separator_and_decimal(file_path, n_lines=5):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = []
        for i, line in enumerate(f):
            if i >= n_lines + 1:  # +1 to ensure we get at least 1 row of actual data (skip header)
                break
            lines.append(line.strip())

    if len(lines) <= 1:
        raise ValueError("File doesn't contain enough data rows.")

    header = lines[0]
    data_lines = lines[1:]  # skip header

    # Step 1: Guess the separator
    candidate_separators = [',', ';', '\t']
    sep_counts = {
        sep: sum(len(line.split(sep)) for line in data_lines) / len(data_lines)
        for sep in candidate_separators
    }
    separator = max(sep_counts, key=sep_counts.get)

    # Step 2: Guess the decimal mark
    decimal = '.'
    for line in data_lines:
        fields = line.split(separator)
        for field in fields:
            field = field.strip()
            if re.match(r'^\d{1,3}(,\d{3})*(\.\d+)?$', field):  # e.g., 1,000.00
                decimal = '.'
                break
            elif re.match(r'^\d{1,3}(\.\d{3})*(,\d+)?$', field):  # e.g., 1.000,00
                decimal = ','
                break
            elif re.match(r'^\d+,\d+$', field):  # fallback
                decimal = ','
                break
        if decimal != '.':
            break

    return separator, decimal


def detect_decimal_issue(separator, decimal):
    if separator in [",", ";", "\t", "tab"]:
        
        if decimal in [",", "."]:
            if separator == ";" and decimal != ",":
                return False
        else:
            print(f"Invalid decimal '{decimal}'. Only ',' (comma) or '.' (point) are accepted.")
            return True
        return False




def is_real_separator(separator):

    if separator in [",", ";", "\t", "tab"]:
        return True
    else:
        print(f"Invalid separator '{separator}'. Only ',' (comma), ';' (semicolon), and 'tab' (tabulator) are accepted.")
        return False


def detect_separator_issue(file_path, expected_separator):
    
    if expected_separator == "tab":
            expected_separator = "\t"
            
    try:
        
        if not is_real_separator(expected_separator):
            return True  # Invalid separator
        
        df = pd.read_csv(file_path, sep=expected_separator, engine='python')

        # If only 1 column, likely wrong separator
        if len(df.columns) <= 1 and expected_separator != "tab":
            return True
        return False
    except Exception:
        return True  # Assume issue if file can't be read


def table_has_data(table_file):
    if not os.path.exists(table_file) or os.path.getsize(table_file) <= 3:
        return False

    with open(table_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # More than 1 line = header + at least one data row
    return len(lines) > 1

    

def is_file_exists(file_path):
    """Check if the file exists."""
    return os.path.exists(file_path)


def check_numeric_columns(table_file, separator, name_col, group_col, value_col, dec):
    """Returns True if the value_col exists and contains only numeric data, False otherwise."""
    df = pd.read_csv(table_file, sep=separator, decimal= dec, engine='python')
    
    
    # Get numeric columns excluding name and category columns
    string_column = [name_col, group_col]
    numeric_columns = df.columns.difference(string_column)

    if value_col not in numeric_columns:
        print(colorama.Fore.RED + f"Only value column does not exist, please check!")
        print(colorama.Style.RESET_ALL)       
        #os._exit(0)
        
    
    # Check if the given value_col exists in the DataFrame
    if value_col not in df.columns:
        return False
        
    # Check if the value_col is numeric and if all values are numeric
    if value_col in numeric_columns:
        # Try to convert the value column to numeric, using 'coerce' to turn invalid values to NaN
        numeric_df = pd.to_numeric(df[value_col], errors='coerce')
        
        # If any NaN values are present, return False (non-numeric data exists)
        if numeric_df.isna().any():
            return False
        else:
            return True
    else:
        return False
    

def has_mixed_column(series):
    numeric_converted = pd.to_numeric(series, errors='coerce')
    has_numeric = numeric_converted.notna().any()
    has_strings = numeric_converted.isna().any()
    return has_numeric and has_strings


def has_mixed_column2(series):
    """
    Returns True if a column contains both numeric and non-numeric values.
    Ignores missing values (NaN, None).
    """
    s = series.dropna()  # ignore missing
    numeric_mask = pd.to_numeric(s, errors='coerce').notna()
    non_numeric_mask = ~numeric_mask

    return numeric_mask.any() and non_numeric_mask.any()


def has_nan_values(series):
    """
    Returns True if the column contains missing values.
    Missing values include: NaN, None, empty strings, or whitespace-only strings.
    """
    s = series.copy()
    
    # Treat empty strings or whitespace as missing
    s = s.replace(r'^\s*$', pd.NA, regex=True)
    
    # Check if any missing values exist
    return s.isna().any()


def def_calculate_statistics(df, name_col, group_col, value_col):
    grouped = df.groupby([name_col, group_col])[value_col]
    
    stats = grouped.agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('sum', 'sum'),
        ('min', 'min'),
        ('max', 'max'),
    ]).reset_index()
    
    # Calculate sum SD using sqrt(sum of variances)
    stats['mean_std'] = stats['std'] * np.sqrt(stats['count'])
    
    

    # Ensure median is displayed without `.0` if it's a whole number
    stats['median'] = stats['median'].apply(lambda x: f"{int(x)}" if x.is_integer() else f"{x}")

    return stats[[name_col, group_col, 'count', 'mean', 'mean_std', 'median', 'sum', 'min', 'max']]

def def_calculate_summarize(df, name_col, group_col, value_col, summarize_mode):
    grouped = df.groupby([name_col, group_col])[value_col]
    
    if summarize_mode == "mean":
        stats = grouped.mean().reset_index(name= value_col)
    elif summarize_mode == "median":
        stats = grouped.median().reset_index(name= value_col)
        # format median as integer if whole number
        stats[value_col] = stats[value_col].apply(
            lambda x: f"{int(x)}" if float(x).is_integer() else f"{x}"
        )

    elif summarize_mode == "sum":
        stats = grouped.sum().reset_index(name= value_col)

    elif summarize_mode == "min":
        stats = grouped.min().reset_index(name= value_col)

    elif summarize_mode == "max":
        stats = grouped.max().reset_index(name= value_col)
    
    return stats

def significance_label(p_value):
    if p_value < 0.001:
        return "***"
    elif p_value < 0.01:
        return "**"
    elif p_value < 0.05:
        return "*"
    else:
        return "NS"  # Not Significant
    
def def_calculate_wilcox(df, name_col, group_col, value_col):
    # Get unique taxa (categories in `name_col`)
    name_groups = df[name_col].unique()

    # List to store results
    results_list = []

    # Perform Wilcoxon rank-sum tests for each unique taxa
    for name in name_groups:
        name_data = df[df[name_col] == name]  # Filter rows by taxa
        groups = name_data[group_col].unique()  # Get unique groups

        # Perform pairwise tests between all groups
        for (group1, group2) in combinations(groups, 2):
            # Extract values for each group
            group1_values = name_data[name_data[group_col] == group1][value_col]
            group2_values = name_data[name_data[group_col] == group2][value_col]

            # Perform Wilcoxon rank-sum test (Mann-Whitney U test)
            if len(group1_values) > 0 and len(group2_values) > 0:
                stat, p_value = mannwhitneyu(group1_values, group2_values, alternative='two-sided')

                # Append results to the list
                results_list.append({
                    'name': name,
                    'comparison': f"{group1} vs {group2}",
                    'statistic': stat,
                    'p_value': p_value,
                    'significance': significance_label(p_value)
                })

    # Convert list to DataFrame
    return pd.DataFrame(results_list)



def calculate_shapiro(df, name_col, group_col, value_col):
    results_list = []

    for name in df[name_col].unique():
        name_data = df[df[name_col] == name]

        for group in name_data[group_col].unique():
            group_values = name_data[name_data[group_col] == group][value_col]

            if len(group_values) >= 3:
                stat, p_value = shapiro(group_values)
                normality = "normal" if p_value > 0.05 else "not normal"
            else:
                stat, p_value, normality = None, None, "NA"

            results_list.append({
                'name': name,
                'group': group,
                'p_value': p_value,
                'normality': normality
            })

    return pd.DataFrame(results_list)


def def_calculate_t_test(df, name_col, group_col, value_col):
    # Get unique taxa (categories in `name_col`)
    name_groups = df[name_col].unique()

    # List to store results
    results_list = []

    # Perform Wilcoxon rank-sum tests for each unique taxa
    for name in name_groups:
        name_data = df[df[name_col] == name]  # Filter rows by taxa
        groups = name_data[group_col].unique()  # Get unique groups

        # Perform pairwise tests between all groups
        for (group1, group2) in combinations(groups, 2):
            # Extract values for each group
            group1_values = name_data[name_data[group_col] == group1][value_col]
            group2_values = name_data[name_data[group_col] == group2][value_col]

            # Perform Wilcoxon rank-sum test (Mann-Whitney U test)
            if len(group1_values) > 0 and len(group2_values) > 0:
                stat, p_value = ttest_ind(group1_values, group2_values, alternative='two-sided')

                # Append results to the list
                results_list.append({
                    'name': name,
                    'comparison': f"{group1} vs {group2}",
                    'statistic': stat,
                    'p_value': p_value,
                    'significance': significance_label(p_value)
                })

    # Convert list to DataFrame
    return pd.DataFrame(results_list)


def def_sort_table_by_keys(table, sort_mode, keys=None):
    """
    Sort a pandas DataFrame by one or more columns.
    """

    # Normalize sort_mode
    if isinstance(sort_mode, str):
        sort_mode = sort_mode.strip().lower()
        if sort_mode in ["decreasing"]:
            sort_mode = True
        elif sort_mode in ["increasing"]:
            sort_mode = False
        

    # Ensure keys is a list
    if isinstance(keys, str):
        keys = [keys]
    elif not isinstance(keys, list):
        raise ValueError("keys must be a string or list of column names.")

    ordered = table.sort_values(by=keys, ascending=not sort_mode)

    return ordered




# def def_relative_columns(df, sum_value, table_path, sep, groupby_cols=None):
    
#     # Ha string és 'none', akkor None-ra alakítjuk
#     if isinstance(groupby_cols, str) and groupby_cols.lower() == "none":
#         groupby_cols = None

#     # Ha string, de nem "none", akkor listává alakítjuk
#     if isinstance(groupby_cols, str) and groupby_cols.lower() != "none":
#         groupby_cols = [groupby_cols]

#     # Identify numeric columns
#     numeric_columns = df.select_dtypes(include=[np.number]).columns

#     check_everything_number(table= df, table_path= table_path, value_to_check= numeric_columns, 
#                                                   parameter= "numeric_col", sep= sep)

#     # Globális normalizáció
#     if groupby_cols is None:
#         normalized_df = df.copy()
#         for column in numeric_columns:
#             total = df[column].sum()
#             normalized_df[column] = (df[column] / total) * float(sum_value) if total != 0 else df[column]
#         return normalized_df


#     # Csoportosított normalizáció
#     def normalize_group(group):
#         for column in numeric_columns:
#             total = group[column].sum()
#             group[column] = (group[column] / total) * float(sum_value) if total != 0 else group[column]
#         return group

#     normalized_df = df.groupby(groupby_cols, group_keys=False).apply(normalize_group)
#     return normalized_df

def def_relative_columns(df, sum_value, table_path, sep, value_col, groupby_cols=None):
    """
    Normalize (make relative) only the selected numeric column (`value_col`).
    Other numeric columns remain unchanged.
    """

    # Handle groupby_cols
    if isinstance(groupby_cols, str):
        if groupby_cols.lower() == "none":
            groupby_cols = None
        else:
            groupby_cols = [groupby_cols]
    

    # Check numeric columns in general (optional full-table check)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    check_everything_number(
        table=df, 
        table_path=table_path, 
        value_to_check= value_col,  # check only the selected column
        parameter="value_col", 
        sep=sep
    )

    # --- Normalization logic ---
    normalized_df = df.copy()

    def normalize_group(group):
        total = group[value_col].sum()
        group[value_col] = (group[value_col] / total) * float(sum_value) if total != 0 else group[value_col]
        return group

    if groupby_cols is None:
        normalized_df = normalize_group(normalized_df)
    else:
        normalized_df = normalized_df.groupby(groupby_cols, group_keys=False).apply(normalize_group)

    return normalized_df



def coerce_cols(merge_cols):
    """
    Always return a flat List[str] of column names (split by whitespace).
    Accepts: None, str, List[str], or List[str-with-spaces].
    """
    if merge_cols is None:
        return []
    # If it's already a list, flatten and split items that contain spaces
    if isinstance(merge_cols, list):
        out = []
        for item in merge_cols:
            if isinstance(item, str):
                out.extend([t for t in item.split() if t])
        return out
    # If it's a string, split on any whitespace
    if isinstance(merge_cols, str):
        return [t for t in merge_cols.split() if t]
    # Otherwise it's unexpected
    raise TypeError(f"These cols has unexpected type: {type(merge_cols)}")


def list_tsv_csv_files(dir):

    files = [f for f in os.listdir(dir) if f.endswith(('.csv', '.tsv'))]

    print(colorama.Fore.RED, f"Please choose a CSV/TSV file. Avalilable file(s) in '{dir}':")
    for file in files:
        print(colorama.Fore.CYAN, f"{file}")
    print(colorama.Style.RESET_ALL)


def list_available_columns(table, separator):
    df = pd.read_csv(table, sep=separator, engine='python')

    type_print(f"Available column(s) in {table}:", color= colorama.Fore.YELLOW)

    for col in df.columns:
        series = df[col].copy()
        n_missing = series.isna().sum() + (series.astype(str).str.strip() == '').sum()

        # Determine column type
        series_non_missing = series.dropna()
        numeric = pd.to_numeric(series_non_missing, errors='coerce')
        has_numeric = numeric.notna().any()
        has_non_numeric = numeric.isna().any()

        if has_numeric and has_non_numeric:
            col_type = "MIXED"
            color = colorama.Fore.RED
        elif has_numeric:
            col_type = "numeric"
            color = colorama.Fore.CYAN
            if n_missing > 0:
                col_type = "MIXED"
                color = colorama.Fore.RED 
        elif has_non_numeric:
            col_type = "text"
            color = colorama.Fore.CYAN
            if n_missing > 0:
                col_type = "MIXED"
                color = colorama.Fore.RED
        else:
            col_type = "unknown"
            color = colorama.Fore.WHITE

        # Append missing info
        if n_missing > 0:
            col_type += f" with {n_missing} Nan value"
            if col_type != "MIXED":
                color = colorama.Fore.YELLOW

        type_print(f"- {col} ({col_type})", color= color, base_speed= 0.007)

    print(colorama.Style.RESET_ALL)





def validate_separator_type(separator):
    return separator in {"_", ";", ",", "|"}

def validate_sep(separator):
    return separator in {"\t", ";", ",", "|"}

def validate_dec(separator):
    return separator in {",", "."}

def validate_sort_mode(sort_mode):
    return sort_mode in {"decreasing", "increasing"}

def check_table(workdir, table_file, parameter):
    workdir = Path(workdir)
    table_path = workdir / table_file
    
    if not os.path.exists(workdir):
        type_print(f"Workdir: {workdir} does not exist!", color= colorama.Fore.RED)
        sys.exit(1)
                
    # valid CSV or TSV file
    if not is_csv_file(str(table_path)):
        list_tsv_csv_files(workdir)
        raise ValueError(f"Error [{table_file}] --{parameter} is not a CSV or TSV file!")
                    
    # létezik e
    if not is_file_exists(table_path):
        list_tsv_csv_files(workdir)
        raise FileNotFoundError(f"Error [{table_file}] --{parameter} file not found!")
                
    # üres e
    if not table_has_data(table_file= table_path):
        raise ValueError(f"Error [{table_file}] --{parameter} is full empty, please check!")
    
def col_in_table(table, value_to_check, parameter, table_path, sep):
    if value_to_check not in table.columns:
            list_available_columns(str(table_path), sep)
            raise ValueError(f"Error [{value_to_check}] as --{parameter} column not found!")
    
def is_not_numeric_column(table, value_to_check, parameter, table_path, sep):
    if has_nan_values(table[value_to_check]):
        list_available_columns(str(table_path), sep)
        raise ValueError(f"Error [{value_to_check}] --{parameter} contains Nan values!")
    
    if pd.api.types.is_numeric_dtype(table[value_to_check]):
                    list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error [{value_to_check}] --{parameter} should not be numeric!")
    
def is_numeric_column(table, value_to_check, parameter, table_path, sep):
    if has_nan_values(table[value_to_check]):
        list_available_columns(str(table_path), sep)
        raise ValueError(f"Error [{value_to_check}] --{parameter} contains Nan values!")
    
    if not pd.api.types.is_numeric_dtype(table[value_to_check]):
                    list_available_columns(str(table_path), sep)
                    raise ValueError(f"Error [{value_to_check}] --{parameter} should be numeric!")
    
# def has_mixed_column_check(table, parameter, table_path, sep):
#     for col in table.columns:               
#             series = table[col]
#             if has_mixed_column2(series):
#                 list_available_columns(str(table_path), sep)
#                 raise ValueError(f"Column {col} --{parameter} has mixed data types, please use consistent columns!")
            

def has_mixed_column3(series, coerce_numeric=True, treat_empty_str_as_na=True):
    
    if not isinstance(series, pd.Series):
        raise ValueError("has_mixed_column expects a pandas Series (pass table[col])")

    s = series.copy()

    # Normalize "missing" textual forms so they don't pollute type detection
    if treat_empty_str_as_na:
        s = s.replace(r'^\s*$', pd.NA, regex=True)        # empty or whitespace -> NA
        s = s.replace(["NaN", "None"], pd.NA)             # literal strings -> NA

    # Consider only non-missing values for type/mix detection
    non_na = s.dropna()
    if non_na.empty:
        return False  # no non-missing values -> not mixed

    if coerce_numeric:
        # Convert values that look numeric to numbers; others become NaN
        numeric_conv = pd.to_numeric(non_na, errors='coerce')
        has_numeric = numeric_conv.notna().any()
        has_non_numeric = numeric_conv.isna().any()
        return has_numeric and has_non_numeric
    else:
        # Strict Python-type check (int/float/str/etc.)
        return non_na.map(type).nunique() > 1
    
def has_mixed_column_check(table, table_path, column_to_check, parameter, sep):
        series = table[column_to_check]
        if has_mixed_column2(series):
            list_available_columns(str(table_path), sep)   # show helpful info
            raise ValueError(f"Column {column_to_check} --{parameter} has mixed data types, please use consistent columns!")   



def error_handling(print_message, completer):
    type_print(print_message, color = colorama.Fore.LIGHTCYAN_EX)
    column = prompt("", completer=completer).strip()
    check_exit(column, in_error_handling=True)
    return column

      
def none_parameter(table, value_to_check):
    if value_to_check not in table.columns and value_to_check == "none" or value_to_check == "None" or value_to_check == "NONE":
                    table[value_to_check] = "NA"
                    value_to_check = value_to_check

def empty_column(table, value_to_check, parameter):
    col = table[value_to_check]

    if col.isnull().all():
        raise ValueError(f"Column [{value_to_check}] --{parameter} is empty!")

    # ha string típus, akkor trim + üres ellenőrzés
    if pd.api.types.is_string_dtype(col):
        col_str = col.fillna("").astype(str)
        if (col_str.str.strip() == "").any():
            raise ValueError(f"Column [{value_to_check}] --{parameter} is empty!")
    return False


def check_everything_string(table, table_path, value_to_check, parameter, sep, is_none_possible):
    # ha none vagyis nem kell csoport
    if is_none_possible:
        none_parameter(table= table, value_to_check= value_to_check)

    # ha nincs --paraméter
    col_in_table(table= table, value_to_check= value_to_check, parameter= parameter, table_path= table_path, sep= sep)
    
    # ha üres --paraméter
    empty_column(table= table, value_to_check= value_to_check, parameter= parameter)
    
    # ha szám a --paraméter
    is_not_numeric_column(table= table, value_to_check= value_to_check, parameter= parameter, table_path= table_path, sep= sep)

    has_mixed_column_check(table= table, table_path= table_path, sep= sep, parameter= parameter, column_to_check= value_to_check)

    
   

def check_everything_number(table, table_path, value_to_check, parameter, sep):
    # nincs --value_col
    col_in_table(table= table, value_to_check = value_to_check, parameter= parameter, table_path = table_path, sep = sep)
             
    # ha üres --paraméter
    empty_column(table= table, value_to_check= value_to_check, parameter= parameter)
    
    # --value_col csak szám lehet
    is_numeric_column(table= table, value_to_check = value_to_check, parameter= parameter, table_path = table_path, sep = sep)

                

def validate_join_type(join_type):
    return join_type in {"inner", "outer", "left", "right"}

def validate_summary_type(join_type):
    return join_type in {"mean", "median", "sum", "min", "max"}

def validate_open_file(join_type):
    return join_type in {"exit", "main"}

def has_column(table_file, separator):   
    df = pd.read_csv(table_file, sep=separator, engine='python')
    
    if df.shape[1] <= 1:
        return False
    else:
        return True
                    

# help kinyomtatás javításshoz
class SingleLineFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        # make the help text start closer to the option flags
        kwargs['max_help_position'] = 200  # adjust as needed
        super().__init__(*args, **kwargs)


help_workdir = "Path to the working directory containing the input file."
help_table = "Input table file (CSV or TSV)."
def help_output(default_output):
    return(f"Output file name. If not provided, a default will be generated. table_file_name{str(default_output)}.csv")
def help_name(default_name):
    return(f"The column containing the names of the samples, That are the names on which you want to perform calculations. Default: {str(default_name)}")
def help_value(default_value):
    return(f"The column containing the values. Default: {str(default_value)}")
def help_group(default_group):
    return(f"The column containing the groups on which the statistics will be calculated. Default: {str(default_group)}")


exit_autofill = WordCompleter(autofill.exit_autofill, ignore_case=True)

def safe_to_csv(table, output_path, separator, decimal):
    printed_warning = False
    user_input = None

    while True:
        try:
            table.to_csv(output_path, index=False, sep=separator, decimal=decimal)
            return  # success → stop trying

        except PermissionError:
            if not printed_warning:
                type_print(
                    f"Output file '{output_path}' is open. Waiting until it is closed..." ,color=colorama.Fore.RED)
                print(colorama.Style.RESET_ALL)
                
                printed_warning = True

            user_input = prompt("Close the file and press Enter, or type 'exit' or 'main': ",completer=exit_autofill).strip()

                # If user types something (not empty)
            if user_input in {"exit", "main"}:
                    check_exit(user_input)
                    return 

                       
    
def get_language(config_path="language.txt"):
    path = Path(config_path)

    with open(path, encoding="utf-8") as f:
        lang = f.read().strip().capitalize()

    return lang


def get_local_settings():
    language = get_language()

    if language == "Magyar":
        decimal = ","

    else:
        decimal = "."

    return {"language": language, "decimal": decimal}
