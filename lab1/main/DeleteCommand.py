from Command import Command


class DeleteCommand(Command):
    def __init__(self, manager, title):
        self.manager = manager
        self.title = title
        self.deleted_node = None
        self.parent_node = None
        self.children = []  # 用于保存删除的节点的所有子节点

    def execute(self):
        self.deleted_node = self.manager.nodes.get(self.title)
        if self.deleted_node:
            self.parent_node = self.deleted_node.parent
            self._store_children(self.deleted_node)
            self.manager.delete_title(
                self.title) if not self.deleted_node.is_bookmark else self.manager.delete_bookmark(self.title)

    def _store_children(self, node):
        # store children nodes recursively
        for child in node.children:
            self.children.append((child.name, child.is_bookmark, child.url, child.parent.name))
            self._store_children(child)

    def undo(self):
        if self.deleted_node:
            if self.deleted_node.is_bookmark:
                restored_node = self.manager.add_bookmark(self.deleted_node.name, self.deleted_node.url, self.parent_node.name)
            else:
                restored_node = self.manager.add_title(self.deleted_node.name, self.parent_node.name)
            # restore children nodes recursively
            self._restore_children(restored_node, self.children)

    def _restore_children(self, parent_node, children_info):
        for name, is_bookmark, url, parent_name in children_info:
            if parent_node.name == parent_name:
                if is_bookmark:
                    new_node = self.manager.add_bookmark(name, url, parent_name)
                else:
                    new_node = self.manager.add_title(name, parent_name)
                self._restore_children(new_node, children_info)