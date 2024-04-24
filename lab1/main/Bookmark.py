from Node import Node
import os


class BookmarkManager:
    def __init__(self, file_path=None):
        self.root = Node("Root")
        self.nodes = {"Root": self.root}
        self.file_path = file_path
        if file_path and os.path.exists(file_path):
            self.load_bookmarks(file_path)

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
