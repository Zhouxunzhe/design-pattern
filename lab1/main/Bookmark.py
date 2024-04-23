from Node import Node
from Handle import CommandHandler


class BookmarkManager:
    def __init__(self):
        self.root = Node("Root")  # 根节点，不显示，用于内部管理
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
        else:
            print(f"Parent title '{parent_title}' not found.")


if __name__ == "__main__":
    bookmark_manager = BookmarkManager()
    command_handler = CommandHandler(bookmark_manager)
    command_handler.execute('add-title "课程"')
    command_handler.execute('add-title "参考资料"')
    command_handler.execute('add-title "函数式" at "参考资料"')
    command_handler.execute('add-title "面向对象" at "参考资料"')
    command_handler.execute('add-title "待阅读"')
    command_handler.execute('add-bookmark "elearning"@"https://elearning.fudan.edu.cn/courses" at "课程"')
    command_handler.execute('add-bookmark "Markdown Guide"@"https://www.markdownguide.org" at "参考资料"')
    command_handler.execute(
        'add-bookmark "JFP"@"https://www.cambridge.org/core/journals/journal-of-functional-programming" at "函数式"')
    command_handler.execute(
        'add-bookmark "Category Theory"@"http://www.appliedcategorytheory.org/what-is-applied-category-theory/" at "待阅读"')
