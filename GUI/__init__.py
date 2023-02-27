import tkinter as tk
import importlib
import json
from tkinter import ttk


class GUI:
    def __init__(self, config_filename="config.json"):
        self.config_filename = config_filename
        with open(config_filename, "r") as f:
            self.config = json.load(f)

        # Configure the root window
        self.root = tk.Tk()
        self.config.update(self.config['Windows']['Main'])
        self.root.title(self.config.get("title", ""))
        self.root.geometry(
            f"{self.config.get('size', [400, 400])[0]}x{self.config.get('size', [400, 400])[1]}+{self.config.get('position', [0, 0])[0]}+{self.config.get('position', [0, 0])[1]}")

        # Create the menu, tabs, and widgets for the root window
        print("Creating menu...")
        self.create_menu(self.config, self.root)

        print("Creating tabs...")
        self.create_tabs(self.config, self.root)

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
                        func = lambda: None

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

    def create_widgets(self, config, parent):
        # Create a notebook for each window in the configuration
        for window_name, window_config in config['Windows'].items():
            db_window = ttk.Frame(parent)
            db_window.grid(column=0, row=0, sticky='nsew')

            # Create tabs for each tab in the window configuration
            tabs = ttk.Notebook(db_window)
            tabs.grid(column=0, row=0, sticky='nsew')
            print(f"tabs: {tabs}")

            for tab_name, tab_config in window_config['tabs'][0].items():
                tab_frame = ttk.Frame(tabs)
                tabs.add(tab_frame, text=tab_name)

                # Create widgets for each widget in the tab configuration
                for widget_config in tab_config['widgets']:
                    widget_type = widget_config['type']
                    if widget_type == 'Label':
                        text = widget_config['text']
                        label = ttk.Label(tab_frame, text=text)
                        label.grid(column=0, row=0)
                    elif widget_type == 'Combobox':
                        options = widget_config['options']
                        combobox = ttk.Combobox(tab_frame, values=options)
                        combobox.grid(column=0, row=1)
                    elif widget_type == 'Button':
                        text = widget_config['text']
                        command = widget_config['command']
                        button = ttk.Button(tab_frame, text=text, command=command)
                        button.grid(column=0, row=2)
                    elif widget_type == 'Entry':
                        text = widget_config['text']
                        variable = widget_config['variable']
                        show = widget_config.get('show', '')
                        entry = ttk.Entry(tab_frame, textvariable=variable, show=show)
                        entry.grid(column=0, row=3)

            print(f"tabs children: {tabs.winfo_children()}")

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

    def create_tabs(self, selected_option, db_window):
        tabs = tk.Frame(db_window)
        tabs.grid(row=0, column=0, sticky='nsew')

        tab_frames = {}
        for tab_options in selected_option.get("tabs", []):
            for tab_label, tab_content in tab_options.items():
                tab_frame = tk.Frame(tabs)
                tab_frames[tab_label] = tab_frame
                tk.Label(tab_frame, text=tab_label).grid(row=0, column=0)

                for i, widget_config in enumerate(tab_content.get('widgets', [])):
                    widget_type = widget_config.get('type')
                    if widget_type == "Label":
                        widget_text = widget_config.get("text", "")
                        label = tk.Label(tab_frame, text=widget_text)
                        label.grid(row=i + 1, column=0, sticky='w', padx=5, pady=5)
                    elif widget_type == "Entry":
                        entry = tk.Entry(tab_frame)
                        entry.grid(row=i + 1, column=0, sticky='w', padx=5, pady=5)
                    elif widget_type == "Button":
                        button_text = widget_config.get("text", "")
                        command = widget_config.get("command")
                        if command:
                            if command.startswith("self."):
                                func = getattr(self, command[5:], lambda: None)
                            else:
                                try:
                                    module_name, func_name = command.rsplit(".", 1)
                                    module = importlib.import_module(module_name)
                                    func = getattr(module, func_name, lambda: None)
                                except (ValueError, AttributeError):
                                    # If there is an error unpacking the command or getting the function reference, print a warning message
                                    print(f"Invalid command: {command}")
                                    func = lambda: None
                                button = tk.Button(tab_frame, text=button_text, command=func)
                                button.grid(row=i + 1, column=0, sticky='w', padx=5, pady=5)

                tab_frame.grid(row=1, column=0, sticky='nsew')
                tab_frame.grid_remove()

        def show_tab(tab_name):
            for name, frame in tab_frames.items():
                if name == tab_name:
                    frame.grid()
                else:
                    frame.grid_remove()

        tab_names = [list(tab_options.keys())[0] for tab_options in selected_option.get("tabs", [])]
        tabs_menu = tk.OptionMenu(db_window, tk.StringVar(value=tab_names[0]), *tab_names, command=show_tab)
        tabs_menu.grid(row=0, column=0, sticky='n')

        show_tab(tab_names[0])

    def exit_program(self):
        self.root.quit()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)
        # self.create_new_window("Main", self.root)
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
