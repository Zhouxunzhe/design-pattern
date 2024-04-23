class Node:
    def __init__(self, name, parent=None, is_bookmark=False, url=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.is_bookmark = is_bookmark
        self.url = url

    def add_child(self, child):
        self.children.append(child)