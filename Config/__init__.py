import json


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.config = self.load_config()

    def load_config(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(self.filename, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_menu_options(self):
        return self.config.get("menu_options", [])

    def get_database_config(self):
        return self.config.get("Database", {})

    def update_database_config(self, new_config):
        self.config["Database"] = new_config
        self.save_config()
