import sublime
import sublime_plugin
import webbrowser
import ast

settings = sublime.load_settings('Alto.sublime-settings')

class AltoOpenCommand(sublime_plugin.TextCommand):
    def get_view_name(self):
        point = self.view.sel()[0].a
        row, col = self.view.rowcol(point)
        lineno = row + 1 # row is 0-based, so add 1 to compare with ast nodes.

        content = ''
        filename = self.view.file_name()
        with open(filename, 'r') as fh:
            content = fh.read()

        tree = ast.parse(content, filename=filename)
        for node in reversed(list(ast.iter_child_nodes(tree))):
            if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                if node.lineno <= lineno:
                    return node.name

    def run(self, edit):
        url = settings.get('url', 'http://127.0.0.1:8000/_alto/')
        view_name = self.get_view_name()
        if view_name:
            url += '?q={0}'.format(view_name)
        webbrowser.open(url)
