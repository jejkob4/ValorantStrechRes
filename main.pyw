import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "source")
USER_PROFILE = os.environ["USERPROFILE"]
VALORANT_LOG_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "VALORANT", "Saved", "Logs")
VALORANT_CONFIG_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "VALORANT", "Saved", "Config")


def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def list_directories_in_directory(directory, exclude=[]):
    return [
        d for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d)) and d not in exclude
    ]

def copy_and_rename(source_file, destination_directory):
    destination_file = os.path.join(destination_directory, "GameUserSettings.ini")

    try:
        shutil.copy2(source_file, destination_file)
        messagebox.showinfo("Success", f"File has been copied successfully, but be careful to APPLY THE RESOLUTION YOU WANT IN WINDOWS before starting the game.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def populate_source_files():
    if not os.path.isdir(SOURCE_DIRECTORY):
        messagebox.showerror("Error", f"Source directory '{SOURCE_DIRECTORY}' does not exist.")
        return

    files = list_files_in_directory(SOURCE_DIRECTORY)
    source_listbox.delete(0, tk.END)

    if not files:
        source_listbox.insert(tk.END, "No files found in the source directory.")
    else:
        for file in files:
            source_listbox.insert(tk.END, file)


profiles=[]

def populate_profile_folders():
    if not os.path.isdir(VALORANT_CONFIG_DIR):
        messagebox.showerror("Error", f"Valorant directory '{VALORANT_CONFIG_DIR}' does not exist.")
        return


    excluded_folders = ["Windows", "CrashReportClient"]
    directories = list_directories_in_directory(VALORANT_CONFIG_DIR, exclude=excluded_folders)
    profile_listbox.delete(0, tk.END)

    if not directories:
        profile_listbox.insert(tk.END, "No folders found in the source directory.")
    else:
        for directory in directories:
            profile_listbox.insert(tk.END, directory)
            profiles.append(directory)



def copy_file():
    # Get selected resolution
    selected_resolution_index = source_listbox.curselection()
    if not selected_resolution_index:
        messagebox.showwarning("Warning", "Please select a resolution from the list.")
        return

    selected_resolution = source_listbox.get(selected_resolution_index[0])

    # Get selected profile
    selected_profile_index = profile_listbox.curselection()
    if not selected_profile_index:
        messagebox.showwarning("Warning", "Please select a profile from the list.")
        return

    selected_profile = profile_listbox.get(selected_profile_index[0])

    # Construct source file and destination folder paths
    source_file = os.path.join(SOURCE_DIRECTORY, selected_resolution)
    destination_folder = os.path.join(VALORANT_CONFIG_DIR, selected_profile, "Windows")

    if not os.path.exists(destination_folder):
        messagebox.showerror("Error", f"This is not a valid profile.")
        return

    copy_and_rename(source_file, destination_folder)




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






root = tk.Tk()
root.title("Valorant Stretch Resolution")
root.geometry("650x400")
root.configure(bg="#1E1E1E")  # Dark background for modern style

# Styling
style = ttk.Style()
style.theme_use("clam")  # Use a clean, modern theme
style.configure(
    "TLabel",
    background="#1E1E1E",  # Match background
    foreground="#E1E1E1",  # Light text
    font=("Segoe UI", 10),
)
style.configure(
    "TButton",
    background="#2A2A2A",
    foreground="#E1E1E1",
    font=("Segoe UI", 10, "bold"),
    padding=6,
)
style.map(
    "TButton",
    background=[("active", "#444444")],  # Change color on hover
    foreground=[("active", "#FFFFFF")],
)

# Transparent effect for the main window
root.attributes("-alpha", 0.99)  # Slight transparency

# Header
header_label = ttk.Label(
    root, text="Valorant Stretch Resolution", font=("Segoe UI", 16, "bold"), anchor="center"
)
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Resolution List
ttk.Label(root, text="Resolution List:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
source_listbox = tk.Listbox(
    root, height=10, width=50, selectmode=tk.SINGLE, exportselection=False, bg="#2A2A2A", fg="#E1E1E1"
)
source_listbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# Profile List
ttk.Label(root, text="Profile List:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
profile_listbox = tk.Listbox(
    root, height=10, width=50, selectmode=tk.SINGLE, exportselection=False, bg="#2A2A2A", fg="#E1E1E1"
)
profile_listbox.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

# Apply Button
apply_button = ttk.Button(root, text="Apply Resolution", command=copy_file)
apply_button.grid(row=4, column=0, columnspan=2, pady=10)

# Footer
footer_label = ttk.Label(root, text="Made by Džakub with help from ChatGPT", font=("Segoe UI", 8, "italic"))
footer_label.grid(row=5, column=0, columnspan=2, pady=5)


# Populate Lists on Startup


populate_source_files()
populate_profile_folders()

profile_list = remove_region_suffix(profiles)
log_path = find_log(VALORANT_LOG_DIR)
latest_active_profile = find_latest_active_profile(profile_list, log_path)

combined_text = f"{"Latest active profile: "} {latest_active_profile}"
ttk.Label(root, text=combined_text, font=("Segoe UI", 10, "italic")).grid(row=3, column=1, columnspan=2, pady=5)


if log_path:
    print(f"Found: {log_path}")
else:
    print("ShooterGame.log not found.")

if latest_active_profile:
    print(f"Latest active profile found: {latest_active_profile}")
else:
    print("No active profile found.")



# Run the GUI loop
root.mainloop()
