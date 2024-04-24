class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def run_plugins(self, node):
        for plugin in self.plugins:
            plugin.modify_node(node)


class SamplePlugin:
    def modify_node(self, node):
        if node.is_bookmark:
            node.extra_info = f"[{node.read_count}]" if node.is_read else ''
