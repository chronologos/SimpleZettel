import sublime, sublime_plugin
import os, string
import re


from SimpleZettel.wiki_page import *
from SimpleZettel.external_search import *
from SimpleZettel.uid import *


class ReferenceAutocompleteCommand(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # don't offer anything for multiple cursors
        if len(locations) > 1:
            return ([], 0)
        # start determines which completion to offer
        start = locations[0] - len(prefix)
        # check scope of charactor on `start
        if not view.match_selector(start, "text.html.markdown"):
            return None
        verbose = False
        if verbose:
            print("Running ReferenceAutocompleteCommand")
        if verbose:
            print(prefix)
        cur_word_glob = "*{}*".format(prefix)
        file_paths = ExternalSearch().rg_search_for_file(ZETTEL_DIRS, cur_word_glob)
        if file_paths:
            basenames = [strip_file_suffix(fp) for fp in file_paths]
            return [[x, x] for x in basenames]

        # fallback to all search
        cur_word_regex = ".*{}.*".format(prefix)
        # dictionary with filename as key, list of (linenum, line) as value.
        raw_res = ExternalSearch().rg_search_for_text(ZETTEL_DIRS, cur_word_regex)
        flattened_res = []
        for k, l in raw_res.items():
            for v in l:
                flattened_res.append((k, v[0], v[1]))
        if verbose:
            print(flattened_res)
        res = [
            [line, strip_file_suffix(filename)]
            for (filename, num, line) in flattened_res
        ]
        if verbose:
            print(res)
        return res

    def get_current_word(self):
        cur_region = self.view.sel()[0]
        cur_word_region = self.view.word(cur_region)
        cur_word = self.view.substr(cur_word_region)
        return cur_word
