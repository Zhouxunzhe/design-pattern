from CommandHandler import CommandHandler
from BookmarkManager import BookmarkManager

if __name__ == "__main__":
    bookmark_manager = BookmarkManager()
    command_handler = CommandHandler(bookmark_manager)

    # add
    command_handler.execute('add-title "个人收藏"')
    command_handler.execute('add-title "课程" at "个人收藏"')
    command_handler.execute('add-title "参考资料" at "个人收藏"')
    # command_handler.execute('undo')
    command_handler.execute('add-title "函数式" at "参考资料"')
    command_handler.execute('save "../bookmarks/cloud1.bmk"')
    command_handler.execute('undo')
    command_handler.execute('undo')
    command_handler.execute('undo')
    command_handler.execute('redo')
    command_handler.execute('redo')
    command_handler.execute('redo')
    command_handler.execute('add-title "面向对象" at "参考资料"')
    command_handler.execute('add-title "待阅读" at "个人收藏"')
    command_handler.execute('add-bookmark "elearning"@"https://elearning.fudan.edu.cn/courses" at "课程"')
    command_handler.execute('add-bookmark "Markdown Guide"@"https://www.markdownguide.org" at "参考资料"')
    command_handler.execute('save "../bookmarks/cloud2.bmk"')
    command_handler.execute(
        'add-bookmark "JFP"@"https://www.cambridge.org/core/journals/journal-of-functional-programming" at "函数式"')
    command_handler.execute(
        'add-bookmark "Category Theory"@"http://www.appliedcategorytheory.org/what-is-applied-category-theory/" at "待阅读"')
    command_handler.execute('read-bookmark "elearning"')

    # delete
    # command_handler.execute('delete-title "参考资料"')
    # command_handler.execute('undo')
    # command_handler.execute('delete-bookmark "Markdown Guide"')

    # load/save
    command_handler.execute('save "../bookmarks/cloud.bmk"')
    command_handler.execute('open "../bookmarks/cloud1.bmk"')
    command_handler.execute('open "../bookmarks/cloud2.bmk"')
    command_handler.execute('open "../bookmarks/cloud.bmk"')
    command_handler.execute('close "../bookmarks/cloud1.bmk"')
    # command_handler.execute('edit "../bookmarks/cloud.bmk"')
    # bookmark_manager = BookmarkManager("../bookmarks/cloud.bmk")
    # command_handler = CommandHandler(bookmark_manager)
    # command_handler.execute('save "../bookmarks/cloud.bmk"')

    # read bookmarks
    command_handler.execute('show-tree')
    command_handler.execute('read-bookmark "elearning"')
    command_handler.execute('show-tree')

    # show ls-tree
    command_handler.execute('ls-tree')
