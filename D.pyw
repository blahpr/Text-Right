import sys
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, END, ttk, Toplevel
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import logging
import json
import webbrowser

# Get the directory of the current script or executable
script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.keep_json_var = tk.BooleanVar(value=False)  # Initialize the variable
        self.export_json_var = tk.BooleanVar(value=False)  # Initialize the variable
        self.data_folder = ""  # Initialize data_folder attribute
        self.original_names = {}
        self.new_names = {}
        self.data_folder = os.path.join(os.path.dirname(__file__), 'data')
        self.root.title("Text Right v1.0")
        self.root.geometry("1100x600")  # main window size
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        # Get the directory of the current script or executable
        script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

        # Construct the path to the icon files
        icon_path = os.path.join(script_dir, 'images', 'D.ico')
        about_icon_path = os.path.join(script_dir, 'images', 'B_64x64.png')
        about_image_path = os.path.join(script_dir, 'images', 'B_64x64.png')

        # Set the application icon
        self.root.iconbitmap(default=icon_path)

        self.menubar = Menu(self.root)

        self.create_menu(about_icon_path, about_image_path)
        self.create_widgets()

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        self.selected_folder = ""
        self.original_names = {}
        self.new_names = {}
        self.last_selected_dir = ""

        # File to store the data
        script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

        # Load data from JSON file
        self.load_data()

        # Export JSON to Desktop variable
        self.export_json_var = tk.BooleanVar(value=False)

    def export(self):
        # Save the JSON data to the desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        data_folder_base = 'data'
        data_folder_path = os.path.join(desktop_path, data_folder_base)
        data_folder_path = os.path.join(desktop_path, 'data')
        json_file_path = os.path.join(data_folder_path, 'data.json')

        # Find the next available data folder name
        count = 1
        while os.path.exists(data_folder_path):
            data_folder_path = os.path.join(desktop_path, f"{data_folder_base} {count}")
            count += 1

        os.makedirs(data_folder_path, exist_ok=True)  # Create the data folder on the desktop if it doesn't exist

        # Inside the data folder, create the 'data.json' file
        json_file_path = os.path.join(data_folder_path, 'data.json')

        data = []
        for original_name, new_name in self.original_names.items():
            file_data = {
                "original_name": original_name,
                "new_name": new_name
            }
            data.append(file_data)
            
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Exported", "To: (data) Folder on Desktop.")

    def create_menu(self, about_icon_path, about_image_path):
        menubar = Menu(self.root)
        
        # File menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Browse", command=self.browse_folder)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Options
        #optionsmenu = Menu(menubar, tearoff=0)
        #optionsmenu.add_command(label="Export JSON to Desktop", command=self.export)
        #menubar.add_cascade(label="Options", menu=optionsmenu)
        
        # About menu
        aboutmenu = Menu(menubar, tearoff=0)
        about_icon = ImageTk.PhotoImage(Image.open(about_icon_path))
        aboutmenu.add_command(label="Text Right v1.0", compound="left", command=lambda: self.show_about_dialog(about_image_path))
        menubar.add_cascade(label="About", menu=aboutmenu)
        
        # Store the icon reference to prevent garbage collection
        self.about_icon = about_icon

        # Set the menu
        self.root.config(menu=menubar)

        # Create a label with a large width to center the text
        label_width = 210  # Adjust the width as needed
        centered_text = "Drag N Drop (\"DND\") Folder Anywhere or File, Browse, and Select Folder".center(label_width)
        menubar.add_command(label=centered_text, state="disabled")

    def show_about_dialog(self, about_image_path):
        about_window = Toplevel(self.root)
        about_window.title("About Text Right v1.0")

        # Load the about image
        about_image = ImageTk.PhotoImage(Image.open(about_image_path))

        # Display the image
        image_label = tk.Label(about_window, image=about_image)
        image_label.image = about_image  # Keep a reference to prevent garbage collection
        image_label.pack(pady=10)

        # Display additional text
        about_text = (
            "VERSION v1.0\n\n"
            "A Simple Text Correction Tool When Downloading Files And The Text Has Unneeded Characters And/Or Symbols\n"
            "And You Just Want Or Need Simple Names Or Text.\n\n"
            "By: BLAHPR 2024"
        )
        text_label = tk.Label(about_window, text=about_text, justify="left")
        text_label.pack(pady=10)

        # Add a GitHub button that opens the GitHub URL
        github_button = tk.Button(about_window, text="My Github\nhttps://github.com/blahpr/Text-Right", command=self.open_github)
        github_button.pack(pady=0)

    def open_github(self):
        webbrowser.open("https://github.com/BLAHPR/Text-Right/releases/latest")

         # Directory for storing JSON file
        self.data_folder = os.path.join(script_dir, 'data')

        # Delete the data folder when closing
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)

        self.listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        self.select_all_button = tk.Button(button_frame, text="Select All", command=self.select_all)
        self.select_all_button.pack(side=tk.LEFT, padx=5)

        self.preview_button = tk.Button(button_frame, text="Preview Changes", command=self.preview_changes)
        self.preview_button.pack(side=tk.LEFT, padx=5)

        self.rename_button = tk.Button(button_frame, text="Correct Text\nNormalize Text", command=self.rename_files, state=tk.DISABLED)
        self.rename_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undo_organization, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.clear_window_button = tk.Button(button_frame, text="Clear Window", command=self.clear_window)
        self.clear_window_button.pack(side=tk.RIGHT, padx=5)

        self.clear_selection_button = tk.Button(button_frame, text="Clear Selections", command=self.clear_selection)
        self.clear_selection_button.pack(side=tk.RIGHT, padx=5)

        self.progress_label = tk.Label(main_frame, text="")
        self.progress_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.preview_tree = ttk.Treeview(main_frame, columns=("new_name",), show='tree headings')
        self.preview_tree.heading('#0', text='Original Name')
        self.preview_tree.heading('#1', text='New Name')
        self.preview_tree.column('#0', stretch=tk.YES, width=400)
        self.preview_tree.column('#1', stretch=tk.YES, width=400)
        self.preview_tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

        options_frame = tk.Frame(self.root)
        options_frame.grid(row=0, column=1, sticky="nsew")

        self.remove_special_var = tk.BooleanVar(value=True)
        self.replace_underscore_var = tk.BooleanVar(value=True)
        self.replace_dot_var = tk.BooleanVar(value=True)
        self.remove_double_spaces_var = tk.BooleanVar(value=True)
        self.remove_hyphen_var = tk.BooleanVar(value=True)

        remove_special_check = tk.Checkbutton(options_frame, text="Remove Special Characters", variable=self.remove_special_var, offvalue=False, onvalue=True)
        remove_special_check.grid(row=0, column=0, sticky="w")

        replace_underscore_check = tk.Checkbutton(options_frame, text="Replace Underscores with Spaces", variable=self.replace_underscore_var, offvalue=False, onvalue=True)
        replace_underscore_check.grid(row=1, column=0, sticky="w")

        replace_dot_check = tk.Checkbutton(options_frame, text="Replace Dots with Spaces", variable=self.replace_dot_var, offvalue=False, onvalue=True)
        replace_dot_check.grid(row=2, column=0, sticky="w")

        remove_double_spaces_check = tk.Checkbutton(options_frame, text="Remove Double Spaces", variable=self.remove_double_spaces_var, offvalue=False, onvalue=True)
        remove_double_spaces_check.grid(row=3, column=0, sticky="w")

        self.remove_hyphen_var = tk.BooleanVar(value=False)  # Not selected by default
        remove_hyphen_check = tk.Checkbutton(options_frame, text="Replace Hyphens with Single Space", variable=self.remove_hyphen_var, offvalue=False, onvalue=True)
        remove_hyphen_check.grid(row=4, column=0, sticky="w")

        self.add_space_before_uppercase_var = tk.BooleanVar(value=False)
        add_space_before_uppercase_check = tk.Checkbutton(options_frame, text="Add Space Before Uppercase Letters\nAfter Lowercase Letters", variable=self.add_space_before_uppercase_var, offvalue=False, onvalue=True)
        add_space_before_uppercase_check.grid(row=5, column=0, sticky="w")

        options_frame.grid_rowconfigure(6, weight=1)
        options_frame.grid_columnconfigure(0, weight=1)

    def browse_folder(self):
            initial_dir = self.last_selected_dir if self.last_selected_dir else os.path.expanduser(r"~\Downloads")
            self.selected_folder = filedialog.askdirectory(initialdir=initial_dir, title="Select Folder")

            self.root.title(f"Text Right v1.0 - {self.selected_folder}")  # Update the window title
            self.progress_label.config(text="")  # Clear the progress label text
            self.progress['value'] = 0  # Reset the progress bar value
            if os.path.isdir(self.selected_folder):
                self.last_selected_dir = self.selected_folder  # Update the last selected directory
                self.populate_listbox()

    def on_drop(self, event):
            self.selected_folder = event.data.strip('{}')
            self.populate_listbox()
            self.root.title(f"Text Right v1.0 - {self.selected_folder}")

    def populate_listbox(self):
        # Clear the listbox and Treeview
        self.listbox.delete(0, END)
        self.preview_tree.delete(*self.preview_tree.get_children())
        self.rename_button.config(state=tk.DISABLED)

        # Set a monospaced font for consistent character width in the top Listbox
        self.listbox.config(font=('Courier', 13, 'bold'), foreground='green', background='lightgrey')
        for filename in os.listdir(self.selected_folder):
            self.listbox.insert(END, filename)

    def select_all(self):
        self.listbox.select_set(0, END)

    def preview_changes(self):
        selected_files = [self.listbox.get(i) for i in self.listbox.curselection()]

        if not selected_files:
            messagebox.showinfo("Info", "No files selected for preview.")
            return

        self.preview_tree.delete(*self.preview_tree.get_children())
        options = {
            'remove_special': self.remove_special_var.get(),
            'replace_underscore': self.replace_underscore_var.get(),
            'replace_dot': self.replace_dot_var.get(),
            'remove_hyphen': self.remove_hyphen_var.get(),
            'remove_double_spaces': self.remove_double_spaces_var.get(),
        }

        # Create a Style and configure font for Treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Courier', 10, 'bold'), foreground='blue', background='lightgrey')

        # Insert the filenames and their new names into the Treeview
        for filename in selected_files:
            new_name = self.simplify_name(filename, options)
            self.preview_tree.insert("", "end", text=filename, values=(new_name,))

        self.rename_button.config(state=tk.NORMAL)
        self.undo_button.config(state=tk.NORMAL)

    def rename_files(self):
        total_files = len(self.new_names)
        self.progress["value"] = 0
        self.progress["maximum"] = total_files
       
        for original, new in self.new_names.items():
            original_path = os.path.join(self.selected_folder, original)
            new_path = os.path.join(self.selected_folder, new)

        # Update the JSON file with the renamed files
        json_file_path = os.path.join(self.data_folder, 'data.json')

        selected_files = [self.listbox.get(i) for i in self.listbox.curselection()]

        if not selected_files:
            messagebox.showinfo("Info", "No files selected for renaming.")
            return

        if not messagebox.askokcancel("Correct \\ Make Changes", "Are you sure?"):
            return

        options = {
            'remove_special': self.remove_special_var.get(),
            'replace_underscore': self.replace_underscore_var.get(),
            'replace_dot': self.replace_dot_var.get(),
            'remove_double_spaces': self.remove_double_spaces_var.get(),
            'remove_hyphen': self.remove_hyphen_var.get(),
        }
        self.progress["maximum"] = len(selected_files)
        self.progress["value"] = 0
        self.progress_label.config(text="Renaming files...")

        for filename in selected_files:
            old_path = os.path.join(self.selected_folder, filename)
            new_name = self.simplify_name(filename, options)
            new_path = os.path.join(self.selected_folder, new_name)
            try:
                os.rename(old_path, new_path)
                self.original_names[filename] = new_name
                self.new_names[filename] = old_path
            except Exception as e:
                print(f"File '{old_path}' not found.")
                continue  # Skip the rest of the loop for this file

            self.progress["value"] += 1
            self.progress.update_idletasks()

        self.save_data()  # Save data to JSON file
        self.progress_label.config(text="Files have been renamed.")
        messagebox.showinfo("Success", "Files have been renamed.")

        # Enable the undo button after renaming is completed
        self.undo_button.config(state=tk.NORMAL)

    def undo_organization(self):
        if not self.original_names:
            messagebox.showinfo("Info", "No files have been renamed yet.")
            return

        if not messagebox.askokcancel("Undo Text Correct", "Are you sure?"):
            return

        for filename, new_name in self.original_names.items():
            try:
                old_path = os.path.join(self.selected_folder, filename)
                new_path = os.path.join(self.selected_folder, new_name)
                os.rename(new_path, old_path)
            except Exception as e:
                logging.error(f"Error renaming file {new_name} back to its original name {filename}: {e}")

        self.original_names.clear()
        self.new_names.clear()
        self.populate_listbox()
        self.preview_tree.delete(*self.preview_tree.get_children())
        self.rename_button.config(state=tk.DISABLED)
        self.undo_button.config(state=tk.DISABLED)
        self.progress_label.config(text="Undo completed.")
        messagebox.showinfo("Done", "Renaming Undone.")

    def clear_selection(self):
        self.listbox.selection_clear(0, END)
        self.preview_tree.delete(*self.preview_tree.get_children())

    def clear_window(self):
        self.listbox.delete(0, END)
        self.preview_tree.delete(*self.preview_tree.get_children())
        self.progress['value'] = 0
        self.progress_label.config(text="")
        self.selected_folder = ""
        self.original_names = {}
        self.new_names = {}
        self.rename_button.config(state=tk.DISABLED)
        self.undo_button.config(state=tk.DISABLED)

    def simplify_name(self, filename, options):
        name, ext = os.path.splitext(filename)
        
        # Remove special characters if the option is enabled
        if options['remove_special']:
            name = re.sub(r'[^\w\s.-]', '', name)
        
        # Replace underscores with spaces if the option is enabled
        if options['replace_underscore']:
            name = name.replace('_', ' ')
        
        # Replace dots, but preserve dots within numbers (e.g., version numbers)
        if options['replace_dot']:
            # Replace dots between words, but keep dots within numbers (e.g., "v1.0")
            # Also remove dots after letters and before numbers or other letters (e.g., "Plus.26" -> "Plus 26")
            name = re.sub(r'(?<=[a-zA-Z])\.(?=\d)', ' ', name)  # Handles "Plus.26" -> "Plus 26"
            name = re.sub(r'(?<=\d)\.(?=[a-zA-Z])', ' ', name)  # Handles dots between numbers and letters
            name = re.sub(r'(?<!\d)\.(?!\d)', ' ', name)  # Replace other dots with spaces except between numbers
        
        # Remove extra spaces if the option is enabled
        if options['remove_double_spaces']:
            name = re.sub(r'\s+', ' ', name)
        
        # Replace hyphens with spaces if the option is enabled
        if options['remove_hyphen']:
            name = name.replace('-', ' ')
        
        # Add a space before uppercase letters that follow lowercase letters, if the option is enabled
        if self.add_space_before_uppercase_var.get():
            name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)
        
        # Add a space between numbers and letters if the option is enabled
        if options['remove_double_spaces']:
            name = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', name)
        
        # Optional: Add space after periods if followed by letters (e.g., "360.Utility" -> "360 Utility")
        if options['replace_dot']:
            name = re.sub(r'\.(?=[A-Za-z])', ' ', name)
        
        # Replace hyphens and other separators with spaces
        if options['remove_hyphen']:
            name = re.sub(r'[^\w\s\.]', ' ', name)
        
        # Remove extra spaces (redundant, but ensures clean output)
        if options['remove_double_spaces']:
            name = re.sub(r'\s+', ' ', name)
        
        # Return the modified name along with the original file extension
        return f"{name.strip()}{ext}"

    def load_data(self):
        try:
            data_folder = os.path.join(os.path.dirname(__file__), 'data')
            json_file_path = os.path.join(data_folder, 'data.json')
            with open(os.path.join(script_dir, 'data.json'), 'r') as file:
                data = json.load(file)
                self.selected_folder = data.get('selected_folder', '')
                self.original_names = data.get('original_names', {})
                self.new_names = data.get('new_names', {})
        except FileNotFoundError:
            pass  # Data file not found, start with default settings
        except Exception as e:
            pass  # Handle other exceptions if needed

    def save_data(self):
        data_folder = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_folder, exist_ok=True)  # Create the "data" folder if it doesn't exist

        data = []
        for original_name, new_name in self.original_names.items():
            file_data = {
                "original_name": original_name,
                "new_name": new_name
            }
            data.append(file_data)

        data_folder = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_folder, exist_ok=True)  # Create the "data" folder if it doesn't exist

        data_file_path = os.path.join(data_folder, "data.json")

        with open(os.path.join(data_folder, "data.json"), "w") as file:
            json.dump(data, file, indent=4)

    def on_closing(self):
        if self.export_json_var.get():
            # Save the JSON data to the desktop
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            data_folder_path = os.path.join(desktop_path, 'data')
            json_file_path = os.path.join(data_folder_path, 'data.json')

            os.makedirs(data_folder_path, exist_ok=True)  # Create the data folder on the desktop if it doesn't exist

            data = {
                'original_names': self.original_names,
                'new_names': self.new_names
            }

            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            # Delete the data folder if it exists
            if os.path.exists(self.data_folder):
                shutil.rmtree(self.data_folder)

        # Close the application
        self.root.destroy()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileOrganizerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
