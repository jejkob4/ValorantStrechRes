import os
import shutil
import tkinter as tk
from tkinter import messagebox


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "source")
USER_PROFILE = os.environ["USERPROFILE"]
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





# GUI Setup
root = tk.Tk()
root.title("Valorant Stretch Resolution")

# Layout
# Resolution List
tk.Label(root, text="Resolution List:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
source_listbox = tk.Listbox(root, height=10, width=50, selectmode=tk.SINGLE, exportselection=False)
source_listbox.grid(row=1, column=0, padx=10, pady=5)

# Profile List
tk.Label(root, text="Profile List:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
profile_listbox = tk.Listbox(root, height=10, width=50, selectmode=tk.SINGLE, exportselection=False)
profile_listbox.grid(row=1, column=1, padx=10, pady=5)

# Apply Button
tk.Button(root, text="Apply Resolution", command=copy_file).grid(row=2, column=0, columnspan=2, pady=5)
tk.Label(root, text="Made by Džakub with help from ChatGPT").grid(row=3, column=0, columnspan=2, pady=5)

# Populate Lists on Startup
populate_source_files()
populate_profile_folders()

# Run the GUI loop
root.mainloop()