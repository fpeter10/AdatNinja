import os
from pathlib import Path
import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from autofill import HeaderCompleter, MultiHeaderCompleter, FileCompleter, DirectoryCompleter
import methods as myMethods
from methods import check_exit

def modify_parameters(command):
    # Tokenize the command string
    tokens = command.split()

    modifiable_params = [
        "--workdir", "--table", "--table1", "--table2", "--output",
        "--name_col", "--group_col", "--new_column", "--value_col", "--tab_id1", "--tab_id2",
        "--mode", "--summary_mode", "--id_col", "--sample_col", "--sum_value", "--merge_cols",
        "--column_to_split", "--sep", "--dec", "--separator", "--new_columns"
    ]

    working_dir = ""
    headers = []

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok not in modifiable_params:
            i += 1
            continue

        # Find the span of values for this parameter
        j = i + 1
        while j < len(tokens) and not tokens[j].startswith("--"):
            j += 1
        current_values = tokens[i+1:j]

        # ---- Handle --workdir ----
        if tok == "--workdir":
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Enter new value or press Enter to keep: ",
                completer=DirectoryCompleter()
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            working_dir = new_value
            tokens[i+1:j] = [new_value]
            i += 2  # parameter + single value

        # ---- Handle table files ----
        elif tok in ["--table", "--table1", "--table2"]:
            file_compl = FileCompleter(working_dir)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Enter new value or press Enter to keep: ",
                completer=file_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            # Try reading headers
            table_path = os.path.join(working_dir, new_value)
            try:
                sep, dec = myMethods.detect_separator_and_decimal(Path(table_path))
                df = pd.read_csv(str(table_path), sep=sep, decimal=dec, engine="python")
                headers = df.columns.tolist()
            except Exception:
                headers = []
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- Handle --output ----
        elif tok == "--output":
            file_compl = FileCompleter(working_dir)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Enter new value or press Enter to keep: ",
                completer=file_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- Single-column headers ----
        elif tok in ["--name_col", "--group_col", "--value_col", "--tab_id1", "--tab_id2", "--sample_col", "--column_to_split", "--new_column"]:
            header_compl = HeaderCompleter(headers)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Enter new value or press Enter to keep: ",
                completer=header_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        elif tok == "--merge_cols":
            current_cols = current_values
            header_compl = MultiHeaderCompleter(headers)
            while True:
                user_in = prompt(
                    f"Current value for {tok} is '{' '.join(current_cols)}'. "
                    "Enter new value (2–5 cols) or press Enter to keep: ",
                    completer=header_compl
                ).strip()
                check_exit(user_in)

                if not user_in:
                    new_cols = current_cols
                else:
                    new_cols = [c for c in user_in.split() if c]

                # calculate new index safely
                next_idx = i + 1 + len(new_cols)

                # replace tokens in place
                tokens[i+1:j] = new_cols

                # move pointer correctly
                i = next_idx
                break

        elif tok in ["--id_col", "--new_columns"]:
            current_cols = current_values
            header_compl = MultiHeaderCompleter(headers)
            while True:
                user_in = prompt(
                    f"Current value for {tok} is '{' '.join(current_cols)}'. Enter new values or press Enter to keep: ",
                    completer=header_compl
                ).strip()
                check_exit(user_in)
                if not user_in:
                    new_cols = current_cols
                else:
                    new_cols = [c for c in user_in.split() if c]

                tokens[i+1:j] = new_cols
                i += 1 + len(new_cols)   # advance correctly
                break
            

        # ---- Mode selection ----
        elif tok == "--mode":
            mode_options = ["inner", "outer", "left", "right"]
            mode_compl = WordCompleter(mode_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Choose mode ({', '.join(mode_options)}): ",
                completer=mode_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- Summary mode selection ----
        elif tok == "--summary_mode":
            mode_options = ["mean", "median", "sum", "min", "max"]
            mode_compl = WordCompleter(mode_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Choose mode ({', '.join(mode_options)}): ",
                completer=mode_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- Sum value ----
        elif tok == "--sum_value":
            sum_options = ["1", "10", "100", "1000"]
            sum_compl = WordCompleter(sum_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. Recommend: 1, 10, 100, 1000 or or press Enter to keep: ",
                completer=sum_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- separator value ----
        elif tok == "--separator":
            sum_options = ["_", ";", ",", "|"]
            sum_compl = WordCompleter(sum_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. choose from: '_', ';', ',', '|' or press Enter to keep: ",
                completer=sum_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        # ---- separator value ----
        elif tok == "--sep":
            sum_options = ["tab", "semicolom", "colon", "pipe"]
            sum_compl = WordCompleter(sum_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. choose from: [tab], [semicolom], [colon], [pipe] or press Enter to keep: ",
                completer=sum_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

        elif tok == "--dec":
            sum_options = ["colon", "point"]
            sum_compl = WordCompleter(sum_options, ignore_case=True)
            new_value = prompt(
                f"Current value for {tok} is '{' '.join(current_values)}'. choose from: [colon], [point] or press Enter to keep: ",
                completer=sum_compl
            ).strip()
            check_exit(new_value)
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2    

        # ---- Fallback for other params ----
        else:
            new_value = input(
                f"Current value for {tok} is '{' '.join(current_values)}'. Enter new value or press Enter to keep: "
            ).strip()
            if not new_value:
                new_value = current_values[0] if current_values else ""
            tokens[i+1:j] = [new_value]
            i += 2

    return " ".join(tokens)

