from ..main.Bookmark import BookmarkManager
from ..main.Handle import CommandHandler


class DeleteTest:
    def setup_method(self):
        self.bookmark_manager = BookmarkManager()
        self.command_handler = CommandHandler(self.bookmark_manager)

    def test_delete_title(self):
        self.command_handler.execute('delete-title "参考资料"')
        # check delete-title
        assert self.bookmark_manager.has_title("参考资料")

    def test_delete_bookmark(self):
        self.command_handler.execute('delete-bookmark "Markdown Guide"')
        # check delete-bookmark
        assert self.bookmark_manager.has_bookmark("Markdown Guide")
