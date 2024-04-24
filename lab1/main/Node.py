class Node:
    def __init__(self, name, parent=None, is_bookmark=False, url=None, is_read=False):
        self.name = name
        self.parent = parent
        self.children = []
        self.is_bookmark = is_bookmark
        self.url = url
        self.is_read = is_read
        self.read_count = 0

    def add_child(self, child):
        if child.is_bookmark:
            # add a bookmark at the beginning
            self.children.insert(0, child)
        else:
            self.children.append(child)

    def mark_as_read(self):
        self.is_read = True
        self.read_count += 1
