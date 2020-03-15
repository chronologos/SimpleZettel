import sublime, sublime_plugin
import os, string
import re
import fileinput

from SimpleZettel.external_search import *
from SimpleZettel.uid import *

block_reference_regex = re.compile(r"\(\((\d*)_?([\w ]*)\)\)")


class WikiBlock:
    def __init__(self, view):
        self.view = view

    def identify_block_at_cursor(self):
        """ Returns (uid, title) if link is parsable, None if it doesn't. """
        for region in self.view.sel():
            text_on_cursor = None
            pos = region.begin()
            line_region = self.view.line(pos)
            if not line_region.empty():
                text_on_cursor = self.view.substr(line_region)
                matches = block_reference_regex.search(text_on_cursor)
                if not matches or matches.lastindex < 2:
                    print("no matches")
                    continue
                uid, title = matches.group(1), matches.group(2)
                print(
                    "identify_block_at_cursor: uid, title = {}, {}".format(uid, title)
                )
                return uid, title
        return None

    def select_block(self, uid, title):
        if uid:  # go by UID first
            self.block_list = self.find_blocks(uid)
        elif title:  # fall back to title
            self.block_list = self.find_blocks(title)
        if len(self.block_list) > 1:
            self.view.window().show_quick_panel(self.block_list, self.open_block)
        elif len(self.block_list) == 1:
            self.open_block(0)
        # else:
        #     self.open_new_file("{}_{}".format(uid, title))

    def find_blocks(self, name_ref):
        verbose = True
        results = []
        search = ExternalSearch()
        raw_res = search.rg_search_for_text(ZETTEL_DIRS, name_ref)
        # List of [[filename, linenum, line]]
        # Duplicated code.
        flattened_res = []
        for k, l in raw_res.items():
            for v in l:
                flattened_res.append([k, "{}".format(v[0]), v[1]])
        if verbose:
            print(flattened_res)
        return flattened_res
        # for file_path_ext in file_paths:
        #     if not file_path_ext:
        #         continue
        #     file_path, extension = os.path.splitext(file_path_ext)
        #     dirname = os.path.dirname(file_path)
        #     basename = os.path.basename(file_path)
        #     results.append([basename, file_path_ext])
        # return results

    def open_block(self, selected_index):
        if selected_index != -1:
            file, linenum, = (
                self.block_list[selected_index][0],
                self.block_list[selected_index][1],
            )
            print("Opening file '%s'" % (file))
            self.view.window().open_file(
                "{}:{}".format(file, linenum), sublime.ENCODED_POSITION
            )
