import sublime, sublime_plugin
import os, string
import re

from SimpleZettel.wiki_page import *


class OpenPageCommand(sublime_plugin.TextCommand):
    def is_visible(self):
        """Return True if cursor is on a wiki page reference."""
        return True
        # for sel in self.view.sel():
        #     scopes = self.view.scope_name(sel.b).split(" ")
        #     if "meta.link.wiki.markdown" in scopes:
        #         return True
        # return False

    def run(self, edit):
        wiki_page = WikiPage(self.view)
        uid_title = wiki_page.identify_page_at_cursor()
        if uid_title:
            uid, title = uid_title
            wiki_page.select_page(uid, title)
