import os
import sys
import shutil
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "source")
USER_PROFILE = os.environ["USERPROFILE"]
VALORANT_CONFIG_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "VALORANT", "Saved", "Config")


def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

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

def browse_destination_folder():
    folder = filedialog.askdirectory(initialdir=VALORANT_CONFIG_DIR, title="Select Destination Folder")
    if folder:
        folder_plus_windows = os.path.join(folder, 'Windows')
        destination_folder_var.set(folder_plus_windows)

def copy_file():
    destination_folder = destination_folder_var.get()

    if not destination_folder:
        messagebox.showwarning("Warning", "Please select a destination folder.")
        return

    selected_index = source_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select a resolution from the list.")
        return

    selected_file = source_listbox.get(selected_index[0])
    source_file = os.path.join(SOURCE_DIRECTORY, selected_file)

    copy_and_rename(source_file, destination_folder)





# GUI Setup
root = tk.Tk()
root.title("Valorant Stretch Resolution")

# Variables
destination_folder_var = tk.StringVar()

# Layout
tk.Label(root, text="Resolution list:").grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
source_listbox = tk.Listbox(root, height=10, width=60)
source_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5)


tk.Label(root, text="Be careful to select only the profile folder !!!!").grid(row=3, column=0, padx=10, pady=5, sticky="w")
tk.Label(root, text="Destination Folder:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=destination_folder_var, width=50).grid(row=4, column=1, padx=10, pady=5, sticky="w")
tk.Button(root, text="Browse", command=browse_destination_folder).grid(row=4, column=2, padx=10, pady=5)

tk.Button(root, text="Apply Resolution", command=copy_file).grid(row=5, column=0, columnspan=3, pady=10)

# Populate the source file list at startup
populate_source_files()



# Run the GUI loop
root.mainloop()
