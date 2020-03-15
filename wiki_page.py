import os
import re
import fileinput

from SimpleZettel.external_search import *
from SimpleZettel.uid import *

# group 1 and 4 will be brackets.
# group 2 will be uid, group 3 title.
uid_title_regex = re.compile(r"(\[\[)(\d*)_?([\w -]*)(\]\])")
DEFAULT_MARKDOWN_EXTENSION = ".md"


class WikiPage:
    def __init__(self, view):
        self.view = view

    def identify_page_at_cursor(self):
        """ Returns (uid, title) if link is parsable, None if it doesn't. """
        for region in self.view.sel():
            text_on_cursor = None
            pos = region.begin()
            _, col = self.view.rowcol(pos)
            line_region = self.view.line(pos)
            if not line_region.empty():
                text_on_cursor = self.view.substr(line_region)
                print(text_on_cursor)
                matches = uid_title_regex.finditer(text_on_cursor)
                for match in matches:
                    uid, title = match.group(2), match.group(3)
                    start_pos, end_pos = match.start(1), match.end(4)
                    # print("identify_page_at_cursor: uid, title = {}, {}".format(uid, title))
                    # print("cw {} uid {} title {}".format(cur_word,uid,title))
                    # print("sp {} ep {} cp {}".format(start_pos,end_pos,col))
                    if col >= start_pos and col <= end_pos:
                        return uid, title
        print("no match")
        return None

    def select_page(self, uid, title):
        if uid:  # go by UID first
            self.file_list = self.find_filenames(uid)
        elif title:  # fall back to title
            self.file_list = self.find_filenames(title)
        if len(self.file_list) > 1:
            self.view.window().show_quick_panel(self.file_list, self.open_selected_file)
        elif len(self.file_list) == 1:
            self.open_selected_file(0)
        else:
            self.open_new_file("{}_{}".format(uid, title), title)

    def find_filenames(self, name_ref):
        results = []
        search = ExternalSearch()
        file_paths = search.rg_search_for_file(ZETTEL_DIRS, "*{}*".format(name_ref))
        for file_path_ext in file_paths:
            if not file_path_ext:
                continue
            file_path, extension = os.path.splitext(file_path_ext)
            dirname = os.path.dirname(file_path)
            basename = os.path.basename(file_path)
            results.append([basename, file_path_ext])
        return results

    def find_backlinks(self):
        """ Returns [[basename, path]]. """
        self.current_file = self.view.file_name()
        _, _, _, uid = path_file_suffix(self.current_file)
        results = []
        search = ExternalSearch()
        file_paths = search.rg_search_in(ZETTEL_DIRS, uid)
        for fp in file_paths:
            if not fp:
                continue
            dirname, basename, extension, uid = path_file_suffix(fp)
            results.append([basename, fp])
        return results

    def open_selected_file(self, selected_index):
        if selected_index != -1:
            _, file = self.file_list[selected_index]
            print("Opening file '%s'" % (file))
            self.view.window().open_file(file)

    def open_new_file(self, pagename, title):
        current_syntax = self.view.settings().get("syntax")
        current_file = self.view.file_name()
        current_dir = os.path.dirname(current_file)

        markdown_extension = self.view.settings().get(
            "sz.markdown_extension", DEFAULT_MARKDOWN_EXTENSION
        )

        filename = os.path.join(current_dir, pagename + markdown_extension)

        new_view = self.view.window().new_file()
        new_view.retarget(filename)

        new_view.run_command(
            "prepare_from_template",
            {"title": title, "template": "20200314163455_Note Template.md"},
        )
        new_view.set_syntax_file(current_syntax)


def append_to_line(file, line_num, text):
    for num, line in enumerate(fileinput.input(file, inplace=True), start=1):
        line = line.rstrip("\r\n")
        if num == line_num:
            print(line + " " + text)
        else:
            print(line)
    return
