from Handle import CommandHandler
from Bookmark import BookmarkManager

if __name__ == "__main__":
    bookmark_manager = BookmarkManager()
    command_handler = CommandHandler(bookmark_manager)

    # add
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

    # delete
    command_handler.execute('delete-title "参考资料"')
    command_handler.execute('delete-bookmark "Markdown Guide"')

    # load/save
    command_handler.execute('save "../cloud.bmk"')
    # command_handler.execute('open "../cloud.bmk"')
    # bookmark_manager = BookmarkManager("../cloud.bmk")
    # command_handler = CommandHandler(bookmark_manager)
