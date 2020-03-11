import sublime, sublime_plugin
import os, string

from SimpleZettel.wiki_page import *


class ListBackLinksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("Running ListBackLinksCommand")
        wiki_page = WikiPage(self.view)
        file_list = wiki_page.find_backlinks()
        self.select_backlink(file_list)

    def select_backlink(self, file_list):
        if file_list:
            self.file_list = file_list
            self.view.window().show_quick_panel(self.file_list, self.open_selected_file)
        else:
            msg = "No pages reference this page"
            print(msg)
            self.view.window().status_message(msg)

    def open_selected_file(self, selected_index):
        if selected_index != -1:
            _, file = self.file_list[selected_index]

            print("Opening file '%s'" % (file))
            self.view.window().open_file(file)
