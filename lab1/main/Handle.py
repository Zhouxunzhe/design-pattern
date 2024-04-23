import re


class CommandHandler:
    def __init__(self, manager):
        self.manager = manager

    def _split_string(self, command):
        new_command = re.sub(r'@|at', '', command)
        parts = re.findall(r'"[^"]*"|\S+', new_command)
        parts = [part.strip('"') for part in parts]
        return parts

    def execute(self, command):
        parts = self._split_string(command)
        action = parts[0]
        if action in ["add-title", "add-bookmark"]:
            self.handle_add_command(parts, command)
        elif action.startswith("delete"):
            self.handle_delete_command(parts)

    def handle_add_command(self, parts, command):
        action = parts[0]
        if action == "add-title":
            title = parts[1]
            if "at" in command:
                parent_title = parts[2]
                self.manager.add_title(title, parent_title)
            else:
                self.manager.add_title(title)
        elif action == "add-bookmark":
            title = parts[1]
            url = parts[2]
            if "at" in command:
                parent_title = parts[3]
                self.manager.add_bookmark(title, url, parent_title)
            else:
                self.manager.add_bookmark(title, url)

    def handle_delete_command(self, parts):
        item = parts[1]
        if parts[0] == "delete-title":
            self.manager.delete_title(item)
        elif parts[0] == "delete-bookmark":
            self.manager.delete_bookmark(item)
