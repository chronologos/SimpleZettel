import os
import re

#                        Y Y Y Y M M D D H H M M S S
like_uid = re.compile(r"\d\d\d\d\d\d\d\d\d\d\d\d\d\d")


def path_file_suffix(filename):
    base = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    base_no_ext = os.path.splitext(base)[0]
    try:
        uid = like_uid.search(base_no_ext).group(0)
    except:
        uid = ""
    try:
        ext = os.path.splitext(base)[1]
    except:
        ext = ""
    return dirname, base_no_ext, ext, uid


def strip_file_suffix(filename):
    d, base, e, uid = path_file_suffix(filename)
    print("d={} b={} e={} uid={}".format(d, base, e, uid))
    return base


def looks_like_uid(s):
    return like_uid.search(s)
