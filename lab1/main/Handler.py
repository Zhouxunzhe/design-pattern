import re
from Bookmark import BookmarkManager
from History import CommandHistory
from AddTitleCommand import AddTitleCommand
from AddBookmarkCommand import AddBookmarkCommand
from DeleteCommand import DeleteCommand


class CommandHandler:
    def __init__(self, manager):
        self.manager = manager
        self.history = CommandHistory()

    def execute(self, command_str):
        parts = self._split_string(command_str)
        action = parts[0]
        if action in ["add-title"]:
            title = parts[1].strip('"')
            parent_title = parts[2] if "at" in command_str else "Root"
            command = AddTitleCommand(self.manager, title, parent_title)
        elif action == "add-bookmark":
            title = parts[1]
            url = parts[2]
            parent_title = parts[3] if "at" in command_str else "Root"
            command = AddBookmarkCommand(self.manager, title, url, parent_title)
        elif action.startswith("delete"):
            title = parts[1]
            command = DeleteCommand(self.manager, title)
        elif action == "undo":
            self.history.undo()
            return
        elif action == "redo":
            self.history.redo()
            return
        elif action == "open" or action == "bookmark" or action == "edit":
            self.manager = BookmarkManager()
            self.history = CommandHistory()
            file_path = parts[1]
            self.manager.load_bookmarks(file_path)
            return
        elif action == "save":
            file_path = parts[1]
            self.manager.save_bookmarks(file_path)
            return
        self.history.execute(command)

    def _split_string(self, command):
        new_command = re.sub(r'@|at', '', command)
        parts = re.findall(r'"[^"]*"|\S+', new_command)
        parts = [part.strip('"') for part in parts]
        return parts
