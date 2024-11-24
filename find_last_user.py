import os

USER_PROFILE = os.environ["USERPROFILE"]
VALORANT_LOG_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "VALORANT", "Saved", "Logs")
VALORANT_CONFIG_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "VALORANT", "Saved", "Config")

##
## FUNCTIONSS
##

def list_directories_in_directory(directory, exclude=[]):
    return [
        d for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d)) and d not in exclude
    ]

profiles=[]

def populate_profile_folders():
    if not os.path.isdir(VALORANT_CONFIG_DIR):
        print(f"Error: Valorant directory '{VALORANT_CONFIG_DIR}' does not exist.")
        return

    excluded_folders = ["Windows", "CrashReportClient"]
    directories = list_directories_in_directory(VALORANT_CONFIG_DIR, exclude=excluded_folders)


    if not directories:
        print("No folders found in the source directory.")
    else:
        print("Directories found:")
        for directory in directories:
            profiles.append(directory)


def find_log(directory):
    log_file = "ShooterGame.log"
    if log_file in os.listdir(directory):
        file_path = os.path.join(directory, log_file)
        if os.path.isfile(file_path):
            return file_path
    return None

def search_string_in_file(file_path, search_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if search_string in line:
                    return True
        return False
    except (FileNotFoundError, IOError) as e:
        print(f"Error opening file: {e}")
        return False




def remove_region_suffix(strings):
    suffixes = ['-eu', '-na', '-ap', 'pbe', 'kr']
    return [s.rsplit('-', 1)[0] if any(s.endswith(suffix) for suffix in suffixes) else s for s in strings]


def find_latest_active_profile(array, path):
    for profile in array:
        if search_string_in_file(path, profile):
            return profile  # Return the first profile that matches in the log file
    return None  # Return None if no match is found


###
### MAIN
###

populate_profile_folders()

log_path = find_log(VALORANT_LOG_DIR)
if log_path:
    print(f"Found: {log_path}")
else:
    print("ShooterGame.log not found.")

profile_list = remove_region_suffix(profiles)
latest_active_profile = find_latest_active_profile(profile_list, log_path)

if latest_active_profile:
    print(f"Latest active profile found: {latest_active_profile}")
else:
    print("No active profile found.")




