import importlib.util
import subprocess
import sys
import os
from datetime import datetime, timedelta

#TODO Minden csomag

# === CONFIG ===
required_libraries = ['numpy', 'pandas', 'requests', 'scipy', 
'colorama', 'prompt_toolkit']  
status_file = 'library_check_status.txt'
check_interval_days = 7

# === FUNCTION TO CHECK LIBRARIES ===
def check_libraries(libs):
    missing = []
    for lib in libs:
        if importlib.util.find_spec(lib) is None:
            missing.append(lib)
    return missing

# === FUNCTION TO INSTALL MISSING LIBRARIES ===
def install_libraries(libs):
    for lib in libs:
        print(f"Installing missing library: {lib}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# === FUNCTION TO CHECK FOR OUTDATED LIBRARIES ===
def check_outdated_libraries(libs):
    print("Checking for outdated libraries...")
    result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated", "--format=freeze"],
                            capture_output=True, text=True)
    outdated_lines = result.stdout.strip().splitlines()

    outdated = []
    for line in outdated_lines:
        package = line.split('==')[0].lower()
        if package in libs:
            outdated.append(package)
    return outdated

# === FUNCTION TO UPDATE LIBRARIES ===
def update_libraries(libs):
    for lib in libs:
        print(f"Updating library: {lib}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", lib])

# === FUNCTION TO READ LAST CHECK DATE ===
def read_last_check():
    if not os.path.exists(status_file):
        return None
    with open(status_file, 'r') as f:
        line = f.readline().strip()
        try:
            return datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

# === FUNCTION TO SAVE STATUS ===
def save_status(status):
    with open(status_file, 'w') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(status + "\n")

# === MAIN FUNCTION TO CALL ===
def check_and_update_libraries(libs=None, check_interval_days_override=None):
    libs = libs or required_libraries
    interval = check_interval_days_override or check_interval_days

    last_check = read_last_check()
    now = datetime.now()

    if not last_check or now - last_check > timedelta(days=interval):
        print("Checking libraries...")
        missing = check_libraries(libs)

        if missing:
            install_libraries(missing)

        still_missing = check_libraries(libs)

        if still_missing:
            status_message = "Missing libraries after attempted install: " + ", ".join(still_missing)
        else:
            outdated = check_outdated_libraries(libs)
            if outdated:
                update_libraries(outdated)
                status_message = "Libraries updated: " + ", ".join(outdated)
            else:
                pass
                status_message = "\n"

        print(status_message)
        save_status(status_message)
    else:
        pass
        #print("Check not needed. Last check was within the past interval.")

# === OPTIONAL: STANDALONE USAGE ===
if __name__ == "__main__":
    check_and_update_libraries()

