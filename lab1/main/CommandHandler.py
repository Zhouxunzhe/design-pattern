import re
import os
from BookmarkManager import BookmarkManager
from CommandHistory import CommandHistory
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
        if action == "add-title":
            title = parts[1].strip('"')
            parent_title = parts[2] if "at" in command_str else "Root"
            command = AddTitleCommand(self.manager, title, parent_title)
        elif action == "add-bookmark":
            title = parts[1]
            url = parts[2]
            parent_title = parts[3] if "at" in command_str else "Root"
            command = AddBookmarkCommand(self.manager, title, url, parent_title)
        elif action == "delete":
            title = parts[1]
            command = DeleteCommand(self.manager, title)
        elif action == "undo":
            self.history.undo()
            return
        elif action == "redo":
            self.history.redo()
            return
        elif action == "open" or action == "bookmark" or action == "edit":
            self.manager = BookmarkManager(opened_files=self.manager.opened_files)
            self.history = CommandHistory()
            file_path = parts[1]
            self.manager.load_bookmarks(file_path)
            self.manager.open_file(file_path)
            return
        elif action == "close":
            if len(parts) > 1:
                file_path = parts[1]
                self.manager.close_file(file_path)
            else:
                self.manager.close_file()
            return
        elif action == "save":
            file_path = parts[1]
            self.manager.save_bookmarks(file_path)
            return
        if action == "show-tree":
            self.manager.show_tree()
            return
        if action == "ls-tree":
            workspace_dir = os.path.dirname(self.manager.current_file)
            self.manager.list_directory_tree(workspace_dir)
            return
        if action == "read-bookmark":
            bookmark_name = parts[1]
            self.manager.read_bookmark(bookmark_name)
            return
        self.history.execute(command)

    def _split_string(self, command):
        new_command = re.sub(r'@|at', '', command)
        parts = re.findall(r'"[^"]*"|\S+', new_command)
        parts = [part.strip('"') for part in parts]
        return parts
