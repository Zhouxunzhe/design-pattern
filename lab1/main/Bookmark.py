from Node import Node


class BookmarkManager:
    def __init__(self):
        self.root = Node("Root")
        self.nodes = {"Root": self.root}

    def add_title(self, title, parent_title="Root"):
        if parent_title in self.nodes:
            parent_node = self.nodes[parent_title]
            new_node = Node(title, parent=parent_node)
            parent_node.add_child(new_node)
            self.nodes[title] = new_node
        else:
            print(f"Parent title '{parent_title}' not found.")

    def add_bookmark(self, title, url, parent_title="Root"):
        if parent_title in self.nodes:
            parent_node = self.nodes[parent_title]
            new_node = Node(title, parent=parent_node, is_bookmark=True, url=url)
            parent_node.add_child(new_node)
            self.nodes[title] = new_node
        else:
            print(f"Parent title '{parent_title}' not found.")

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
