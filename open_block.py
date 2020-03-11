import sublime, sublime_plugin
import os, string
import re

from SimpleZettel.wiki_block import *


class OpenBlockCommand(sublime_plugin.TextCommand):
    def is_visible(self):
        """Return True if cursor is on a wiki page reference."""
        return True
        # for sel in self.view.sel():
        #     scopes = self.view.scope_name(sel.b).split(" ")
        #     if "meta.link.wiki.markdown" in scopes:
        #         return True
        # return False

    def run(self, edit):
        wiki_block = WikiBlock(self.view)
        uid_title = wiki_block.identify_block_at_cursor()
        if uid_title:
            uid, title = uid_title
            wiki_block.select_block(uid, title)
