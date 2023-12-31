import os
import shutil
import customtkinter
import tkinter as tk
from tkinter import filedialog, messagebox
import logging


def find_available_filename(dest_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(dest_folder, filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename


def move_files_and_delete_subfolders(root_folder):
    successful_moves = 0
    failed_moves = 0

    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            src_path = os.path.join(foldername, filename)
            dest_path = os.path.join(root_folder, filename)
            if os.path.exists(dest_path):
                filename = find_available_filename(root_folder, filename)
            dest_path = os.path.join(root_folder, filename)
            try:
                shutil.move(src_path, dest_path)
                successful_moves += 1
                logger.info(f"Moved {filename} to {root_folder}")
            except Exception as e:
                failed_moves += 1
                logger.error(f"Failed to move {filename}: {str(e)}")

    for foldername, _, _ in os.walk(root_folder, topdown=False):
        try:
            os.rmdir(foldername)
            logger.info(f"Deleted empty subfolder: {foldername}")
        except OSError:
            pass

    result_message = f"Operation Complete\nFiles moved: {successful_moves}\nFiles failed: {failed_moves}"
    messagebox.showinfo("Result", result_message)

    label.configure(text=result_message)


def clear_log_files():
    try:
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)

        log_file = "file_mover.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info("Log file cleared.")
        label.configure(text="Log file cleared.")
    except Exception as e:
        logger.error(f"Failed to clear log file: {str(e)}")
        label.configure(text="Failed to clear log file.")


def select_root_folder():
    root_folder = filedialog.askdirectory(title="Select Root Folder")
    if root_folder:
        move_files_and_delete_subfolders(root_folder)


logger = logging.getLogger("file_mover")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("file_mover.log")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# GUI
# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("Move Files and Delete Subfolders")
app.geometry("400x220")
app.resizable(False, False)

customtkinter.CTkLabel(
    app, text="Click the button to select the root folder.").pack(pady=20)

select_button = customtkinter.CTkButton(
    app, text="Select Root Folder", command=select_root_folder)
select_button.pack()

clear_log_button = customtkinter.CTkButton(
    app, text="Clear Log", command=clear_log_files)
clear_log_button.pack()

label = customtkinter.CTkLabel(app, text="", width=500, justify="left")
label.pack(pady=20)

app.mainloop()
