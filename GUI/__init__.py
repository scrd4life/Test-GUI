import tkinter as tk
import importlib
import json
from tkinter import ttk


class GUI:
    def __init__(self, config_filename="config.json"):
        self.config_filename = config_filename
        self.config = {}
        self.load_config()

        # Configure the root window
        self.root = tk.Tk()
        self.config.update(self.config['Windows']['Main'])
        self.root.title(self.config.get("title", ""))
        self.root.geometry(
            f"{self.config.get('size', [400, 400])[0]}x{self.config.get('size', [400, 400])[1]}+{self.config.get('position', [0, 0])[0]}+{self.config.get('position', [0, 0])[1]}")

        # Create the menu and widgets for the root window
        print("Creating menu...")
        self.create_menu(self.config, self.root)

        print("Creating widgets...")
        self.create_widgets(self.config, self.root)

    def load_config(self):
        with open(self.config_filename, "r") as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_filename, "w") as f:
            json.dump(self.config, f)

    def update_config(self, new_config):
        self.config.update(new_config)
        self.save_config()

    def create_menu(self, selected_option, db_window):
        menu_options = selected_option.get("menu", [])
        menu = tk.Menu(db_window)

        for option in menu_options:
            label = option.get("label", "")
            sub_options = option.get("options", [])
            submenu = tk.Menu(menu, tearoff=0)

            for sub_option in sub_options:
                sub_label = sub_option.get("label", "")
                command = sub_option.get("command", "")

                # Dynamically create a reference to the appropriate function
                if command.startswith("self."):
                    func = getattr(self, command[5:])
                else:
                    try:
                        module_name, func_name = command.rsplit(".", 1)
                        module = importlib.import_module(module_name)
                        func = getattr(module, func_name)
                    except (ValueError, AttributeError) as e:
                        # If there is an error unpacking the command or getting the function reference, print a warning message
                        print(f"Invalid command: {command}")
                        print(f"Error: {str(e)}")
                        continue

                # Check if the function is create_new_window and add the label argument if it is
                if func == self.create_new_window:
                    func = lambda label=sub_label: self.create_new_window(label, self.root)

                # Add the menu option to the submenu
                submenu.add_command(label=sub_label, command=func)

            # Add the submenu to the menu if there are sub-options
            if sub_options:
                menu.add_cascade(label=label, menu=submenu)
            else:
                menu.add_command(label=label, command=lambda: None)

        db_window.config(menu=menu)
        return menu

    def create_new_window(self, label, root_window):
        # Find the metadata for the selected option
        selected_option = self.config['Windows'][label]
        print(f"selected_option: {selected_option}")
        if not selected_option:
            print(f"Error: Selected option '{label}' not found in configuration")
            return

        # Create a new window for the selected option
        window_title = selected_option.get("title", "")
        window_size = selected_option.get("size", [400, 400])
        window_position = selected_option.get("position", [0, 0])
        on_load_func = getattr(self, selected_option.get("on_load", ""), None)
        on_close_func = getattr(self, selected_option.get("on_close", ""), None)
        db_window = tk.Toplevel(root_window)
        db_window.title(window_title)
        db_window.geometry(f"{window_size[0]}x{window_size[1]}+{window_position[0]}+{window_position[1]}")
        db_window.protocol("WM_DELETE_WINDOW", on_close_func)

        # Create the menu for the window
        print("Creating menu...")
        self.create_menu(selected_option, db_window)

        # Create the tabs for the window
        print("Creating tabs...")
        self.create_tabs(selected_option, db_window)

        # Create the widgets for the window
        print("Creating widgets...")
        self.create_widgets(selected_option, db_window)

        # Call the on_load function, if it exists
        if on_load_func:
            print("Calling on_load function...")
            on_load_func(db_window)

    def create_tabs(self, selected_option, db_window):
        tabs = tk.ttk.Notebook(db_window)
        tabs.pack(fill='both', expand=True)

        for tab_label, tab_options in selected_option.get("tabs", {}).items():
            tab = tk.Frame(tabs)
            tabs.add(tab, text=tab_label)

            # Add widgets to the tab as desired
            for widget_config in tab_options.get('widgets', []):
                widget_type = widget_config.get('type')

                if widget_type == 'label':
                    text = widget_config.get('text', '')
                    label = tk.Label(tab, text=text)
                    label.pack()

                elif widget_type == 'entry':
                    entry = tk.Entry(tab)
                    entry.pack()

                elif widget_type == 'button':
                    text = widget_config.get('text', 'Button')
                    command = widget_config.get('command', lambda: None)
                    button = tk.Button(tab, text=text, command=command)
                    button.pack()

                # Handle other widget types here

            # Add more tabs as desired

        return tabs

    def create_widgets(self, selected_option, db_window):
        widgets = selected_option.get("widgets", [])
        for widget_config in widgets:
            widget_type = widget_config.get("type", "")
            if widget_type == "Label":
                widget_text = widget_config.get("text", "")
                label = tk.Label(db_window, text=widget_text)
                label.pack()
            elif widget_type == "Entry":
                entry = tk.Entry(db_window)
                entry.pack()
            elif widget_type == "Button":
                button_text = widget_config.get("text", "")
                command = widget_config.get("command")
                if command:
                    if command.startswith("self."):
                        command = getattr(self, command[5:])
                    else:
                        try:
                            module_name, func_name = command.rsplit(".", 1)
                            module = importlib.import_module(module_name)
                            command = getattr(module, func_name)
                        except (ValueError, AttributeError):
                            # If there is an error unpacking the command or getting the function reference, print a warning message
                            print(f"Invalid command: {command}")

    def exit_program(self):
        self.root.quit()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)
        # self.create_new_window("Main", self.root)
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
