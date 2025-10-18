from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter

import json
import os

class HeaderCompleter(Completer):
    def __init__(self, headers):
        self.headers = headers

    def get_completions(self, document, complete_event):
        text = document.text
        options = self.headers + ["none"] + ["exit"] + ["main"]
        for option in options:
            if option.startswith(text):
                yield Completion(option, start_position=-len(text))


#Keywords that should autocomplete
fixed_keywords = ['list','programs', 'help', 'load', 'stat', 'wilcoxon',
                'ttest', 'summarize', 'normality', 'print table', 'long format', 
                'wide format', 'merge', 'relative', 'merge columns', 
                'split columns', 'sort table', 'change sep', 'wd', 'change wd', 'language', 'info', 'exit']

program_help = ['stat', 'wilcoxon','ttest', 'summarize', 'normality', 'print table', 'long format', 
                'wide format', 'merge', 'relative', 'merge columns', 
                'split columns', 'sort table', 'change sep', 'main', 'exit']

CODE_FILE = "saved_commands.json"

def get_saved_code_count():
    if os.path.exists(CODE_FILE):
        with open(CODE_FILE, "r") as f:
            data = json.load(f)
            return len(data)
    return 0

class SchemaCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()
        last_word = document.get_word_before_cursor()

        if not words:
            for kw in fixed_keywords:
                if kw.startswith(last_word):
                    yield Completion(kw, start_position=-len(last_word))

        elif len(words) == 1:
            if words[0] == 'load':
                for option in ['code', 'last_code']:
                    if option.startswith(last_word):
                        yield Completion(option, start_position=-len(last_word))
            else:
                for kw in fixed_keywords:
                    if kw.startswith(last_word):
                        yield Completion(kw, start_position=-len(last_word))

        elif len(words) == 2 and words[0] == 'load':
            if words[1] == 'last_code':
                for num in map(str, range(1, 6)):
                    if num.startswith(last_word):
                        yield Completion(num, start_position=-len(last_word))
            elif words[1] == 'code':
                count = get_saved_code_count()
                for num in map(str, range(1, count + 1)):
                    if num.startswith(last_word):
                        yield Completion(num, start_position=-len(last_word))

        elif len(words) == 3 and words[0] == 'load' and words[1] in ['code', 'last_code']:
            valid_nums = list(map(str, range(1, 6))) if words[1] == 'last_code' else list(map(str, range(1, get_saved_code_count() + 1)))
            if words[2] in valid_nums:
                for action in ['run', 'check', 'modify', 'save']:
                    if action.startswith(last_word):
                        yield Completion(action, start_position=-len(last_word))

        else:
            for kw in fixed_keywords:
                if kw.startswith(last_word):
                    yield Completion(kw, start_position=-len(last_word))

class HelpCompleter(Completer):
    def __init__(self, program_help):
        self.program_help = program_help

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()
        last_word = document.get_word_before_cursor()

        # Ha nincs semmi beírva, minden kulcsszót ajánl
        if not words:
            for kw in self.program_help:
                if kw.startswith(last_word):
                    yield Completion(kw, start_position=0)

        # first word only → suggest help keywords
        elif len(words) == 1:
            for kw in self.program_help:
                if kw.startswith(last_word):
                    yield Completion(kw, start_position=-len(last_word))

        else:
            # Csak azokat, amelyek illeszkednek az aktuális szó elejére
            for kw in self.program_help:
                if kw.startswith(last_word):
                    yield Completion(kw, start_position=-len(last_word))


allowed_exts = ('.csv', '.tsv', '.txt')

def file_filter(path):
    return os.path.isfile(path) and path.endswith(allowed_exts)

class FileCompleter(Completer):
    """
    Completer that suggests only allowed files plus extra static options (e.g., 'exit').
    """
    def __init__(self, working_dir, only_directories=False, expanduser=True, extra_options=None):
        self.path_completer = PathCompleter(
            file_filter=file_filter,
            get_paths=lambda: [working_dir],
            only_directories=only_directories,
            expanduser=expanduser,
        )
        self.extra_options = extra_options or ["exit", "main"]

    def get_completions(self, document, complete_event):
        # 1) Yield file completions
        yield from self.path_completer.get_completions(document, complete_event)

        # 2) Yield static command completions
        text = document.text_before_cursor.strip()
        for option in self.extra_options:
            if option.startswith(text):
                yield Completion(option, start_position=-len(text))
    
class DirectoryCompleter(Completer):
    def __init__(self, only_directories=True, expanduser=True):
        self.path_completer = PathCompleter(only_directories=only_directories, expanduser=expanduser)
        self.extra_options = ["exit"]

    def get_completions(self, document, complete_event):
        # First yield completions from PathCompleter
        yield from self.path_completer.get_completions(document, complete_event)

        # Then yield static options like "exit"
        text = document.text
        for option in self.extra_options:
            if option.startswith(text):
                yield Completion(option, start_position=-len(text))


class MultiHeaderCompleter(Completer):
    def __init__(self, headers):
        self.headers = headers
        self.extra_options = ["exit", "main"]

    def get_completions(self, document, complete_event):
        # split the already typed words
        typed = document.text_before_cursor.split()
        
        # offer headers that haven't been typed yet
        remaining = [h for h in self.headers if h not in typed]
        options = remaining + self.extra_options
        # complete only the current word (last one)
        word = typed[-1] if typed else ""
        for opt in options:
            if opt.startswith(word):
                yield Completion(opt, start_position=-len(word))


merge_mode_autofill = ["inner", "outer", "left", "right", "main", "exit"]
separator_autofill = ["_", ";", ",", "|", "main", "exit"]
new_separator_autofill = ["tab", "semicolon", "colon", "pipe", "main", "exit"]
new_decimal_autofill = ["colon", "point", "main", "exit"]
summary_mode_autofill = ["sum", "mean", "median", "min", "max", "main", "exit"]
relative_summary_autofill = ["1", "10", "100", "1000", "main", "exit"]
sort_mode_autofill = ["decreasing", "increasing","main", "exit"]
exit_autofill = ["main", "exit"]
language_autofill = ["Magyar", "English", "main", "exit"]