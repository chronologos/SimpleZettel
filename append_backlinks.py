import sublime_plugin
import urllib.parse

from SimpleZettel.wiki_page import *


class AppendBacklinksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("Running AppendBacklinksCommand")
        wiki_page = WikiPage(self.view)
        file_list = wiki_page.find_backlinks()
        self.insert_backlinks(edit, file_list)

    def insert_backlinks(self, edit, file_list):
        if file_list:
            self.file_list = file_list
            self.view.insert(edit, self.view.size(), self.format_backlinks(file_list))
        else:
            msg = "No pages reference this page"
            print(msg)
            self.view.window().status_message(msg)

    def format_backlinks(self, file_list):
        res = "# Backlinks\n"
        for f in file_list:
            res += "- [[{}]]\n".format(f[0])
        return res
