from Node import Node
import os
from Plugin import PluginManager, SamplePlugin


class BookmarkManager:
    def __init__(self, file_path=None, opened_files=None):
        self.root = Node("Root")
        self.nodes = {"Root": self.root}
        if file_path is not None:
            file_path = file_path.replace('\\', '/')
        self.file_path = file_path
        if file_path and os.path.exists(file_path):
            self.load_bookmarks(file_path)
        if opened_files is not None:
            self.opened_files = opened_files
        else:
            self.opened_files = set()
        self.current_file = None
        self.plugin_manager = PluginManager()
        self.plugin_manager.register_plugin(SamplePlugin())

    def add_title(self, title, parent_title="Root"):
        if parent_title in self.nodes:
            parent_node = self.nodes[parent_title]
            new_node = Node(title, parent=parent_node)
            parent_node.add_child(new_node)
            self.nodes[title] = new_node
            return new_node
        else:
            print(f"Parent title '{parent_title}' not found.")
            return None

    def add_bookmark(self, title, url, parent_title="Root"):
        if parent_title in self.nodes:
            parent_node = self.nodes[parent_title]
            new_node = Node(title, parent=parent_node, is_bookmark=True, url=url)
            parent_node.add_child(new_node)
            self.nodes[title] = new_node
            return new_node
        else:
            print(f"Parent title '{parent_title}' not found.")
            return None

    def delete_title(self, title):
        if title in self.nodes:
            node_to_delete = self.nodes[title]
            self._delete_node(node_to_delete)
            del self.nodes[title]
        else:
            print(f"Title '{title}' not found.")

    def delete_bookmark(self, title):
        if title in self.nodes:
            node_to_delete = self.nodes[title]
            if node_to_delete.is_bookmark:
                self._delete_node(node_to_delete)
                del self.nodes[title]
            else:
                print(f"'{title}' is not a bookmark.")
        else:
            print(f"Bookmark '{title}' not found.")

    def _delete_node(self, node):
        for child in list(node.children):
            self._delete_node(child)
            if child.name in self.nodes:
                del self.nodes[child.name]
        node.parent.children.remove(node)

    def load_bookmarks(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            current_node = self.root
            for line in file:
                line = line.strip()
                if line.startswith('#'):
                    # Determine the level of the heading
                    level = line.count('#')
                    title = line.strip('# ').strip()
                    # Navigate up to the correct parent level
                    while level <= self._get_level(current_node):
                        current_node = current_node.parent
                    # Add new node
                    new_node = Node(title, parent=current_node)
                    current_node.add_child(new_node)
                    current_node = new_node
                    self.nodes[title] = current_node
                elif line.startswith('['):
                    # Parse bookmark
                    title_end = line.index(']')
                    title = line[1:title_end]
                    url = line[title_end + 2:-1]
                    new_node = Node(title, parent=current_node, is_bookmark=True, url=url)
                    current_node.add_child(new_node)
                    current_node = new_node
                    self.nodes[title] = current_node

    def save_bookmarks(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.truncate(0)
            self._write_node(self.root, file, 0)

    def _write_node(self, node, file, depth):
        if node != self.root:
            if node.is_bookmark:
                file.write(f'[{node.name}]({node.url})\n')
            else:
                file.write(f'{"#" * depth} {node.name}\n')
        for child in node.children:
            self._write_node(child, file, depth + 1)

    def _get_level(self, node):
        level = 0
        while node.parent:
            node = node.parent
            level += 1
        return level

    def show_tree(self, node=None, indent=0, last_nodes=None):
        if node is None:
            node = self.root
        if last_nodes is None:
            last_nodes = []
        if node.name != "Root":
            prefix = ''
            for is_last in last_nodes[:-1]:
                prefix += '    ' if is_last else '|   '
            prefix += '└── ' if last_nodes and last_nodes[-1] else '├── '
            read_marker = '*' if node.is_read else ''
            extra_info = getattr(node, 'extra_info', '')
            if node.is_bookmark:
                print(prefix + f"{read_marker}[{node.name}]{extra_info}")
            else:
                print(prefix + read_marker + f"{node.name}")
        child_last_nodes = last_nodes + [False]
        num_children = len(node.children)
        for index, child in enumerate(node.children):
            child_last_nodes[-1] = index == num_children - 1
            self.show_tree(child, indent + 1, child_last_nodes)

    def read_bookmark(self, bookmark_name):
        if bookmark_name in self.nodes:
            node = self.nodes[bookmark_name]
            if node.is_bookmark:
                node.mark_as_read()
                # print(f"Bookmark '{bookmark_name}' has been marked as read. Total reads: {node.read_count}")
            else:
                print(f"'{bookmark_name}' is not a bookmark.")
        else:
            print(f"Bookmark '{bookmark_name}' not found.")

    def open_file(self, file_path):
        file_path = file_path.replace('\\', '/')
        self.current_file = file_path
        self.opened_files.add(file_path)
        # print(f"Opened file: {file_path}")

    def close_file(self, file_path=None):
        if file_path:
            file_path = file_path.replace('\\', '/')
            if file_path in self.opened_files:
                if file_path == self.current_file:
                    self.current_file = None
                self.opened_files.remove(file_path)
                # print(f"Closed specified file: {file_path}")
            else:
                print(f"File {file_path} was not open.")
        else:
            if self.current_file:
                # print(f"Closing current file: {self.current_file}")
                self.opened_files.remove(self.current_file)
                self.current_file = None
            else:
                print("No file is currently open.")

    def list_directory_tree(self, path, prefix='', is_root=True):
        if is_root:
            print(f"└── {os.path.basename(path)}/")
            prefix = "    "
        items = os.listdir(path)
        items.sort()
        last_index = len(items) - 1

        for index, item in enumerate(items):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if index == last_index:
                    print(f"{prefix}└── {item}/")
                    new_prefix = prefix + "    "
                else:
                    print(f"{prefix}├── {item}/")
                    new_prefix = prefix + "|   "
                self.list_directory_tree(full_path, new_prefix, is_root=False)
            else:
                if index == last_index:
                    print(f"{prefix}└── {item}")
                else:
                    print(f"{prefix}├── {item}")
