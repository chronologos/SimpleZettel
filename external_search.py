import sublime, sublime_plugin
import os, string
import re
import subprocess

from collections import defaultdict

DEFAULT_SEARCH_COMMAND = "/usr/local/bin/rg"
SETTINGS_FILE = "Simple Zettel.sublime-settings"
RG_SETTING = "sz.rg_location"
ZETTEL_DIRS = ["/Users/iantay/Library/Mobile Documents/com~apple~CloudDocs/zk"]


class ExternalSearch:
    def __init__(self):
        self.search_cmd = sublime.load_settings(SETTINGS_FILE).get(
            RG_SETTING, DEFAULT_SEARCH_COMMAND
        )

    def rg_search_in(self, folders, regexp):
        """
        Perform an external search for regexp in folder.
        """
        # -l to return only matching filenames.
        args = [self.search_cmd, "-l", regexp, " ".join(folders)]
        print("rg_search_in args={}".format(args))
        raw_res = self.run(args)
        return [r for r in raw_res.split("\n") if r != ""]

    def rg_search_for_file(self, folders, glob):
        """   
        Perform an external search for file names matching glob in folder.
        """
        args = [self.search_cmd, "-g", glob, "--files", " ".join(folders)]
        print("rg_search_for_file args={}".format(args))
        raw_res = self.run(args)
        return [r for r in raw_res.split("\n") if r != ""]

    def rg_search_for_text(self, folders, regexp):
        """   
        Perform an external search for regexp in folder.
        Returns dictionary with filename as key, list of (linenum, line) as value.
        """
        args = [
            self.search_cmd,
            "--line-number",
            "--smart-case",
            regexp,
            " ".join(folders),
        ]
        print("rg_search_for_text args={}".format(args))
        raw_res = self.run(args)
        res_split = [r for r in raw_res.split("\n") if r != ""]
        file_to_lines = defaultdict(list)
        for r in res_split:
            # filename:linenum:text
            split_line = r.split(":")
            filename, linenum, line = (
                split_line[0],
                int(split_line[1]),
                split_line[2].strip(" "),
            )
            file_to_lines[filename].append((linenum, line))
        return file_to_lines

    def run(self, args):
        """
        Execute SEARCH_COMMAND to run a search, handle errors & timeouts.
        Return output of stdout as string.
        """
        output = b""
        verbose = False
        if verbose:
            print("cmd:", " ".join(args))
        try:
            output = subprocess.check_output(args, shell=False, timeout=10000)
        except subprocess.CalledProcessError as e:
            print(
                "sublime_zk: search unsuccessful. retcode={}, cmd={}".format(
                    e.returncode, e.cmd
                )
            )
            for line in e.output.decode("utf-8", errors="ignore").split("\n"):
                print("    ", line)
        except subprocess.TimeoutExpired:
            print("sublime_zk: search timed out:", " ".join(args))
        if verbose:
            print("run verbose logs:")
            print(output.decode("utf-8", errors="ignore"))
        return output.decode("utf-8", errors="ignore").replace("\r", "")
