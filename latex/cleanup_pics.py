#!/usr/bin/env python3

"""
A small script to find and move pics not used in a LaTeX file.

Pics that are not included in the TeX file are moved
to a special dir for later use or deletion or whatever.
"""

__author__ = "Daniel Cervenkov"
__date__ = "Oct. 8, 2015"

import os
import sys
import shutil

PIC_SUFFIXES = (".png", ".gif", ".pdf", ".ps", ".jpg", ".jpeg")
NOT_USED_DIR = "unused_pics"


def get_pics_from_tex(tex_files):
    """Return a list of pictures used in supplied TeX files."""
    pics = []
    for tex_file in tex_files:
        with open(tex_file, "r") as file:
            searchlines = file.readlines()
        for line in searchlines:
            if "includegraphics" in line:
                beg = line.index('{')
                end = line.index('}')
                pics.append(line[beg+1:end])
    return pics


def get_pics_from_dir(pic_dir):
    """Return a list of pictures present in a directory."""
    pics = []
    for root, _, filenames in os.walk(pic_dir):
        for filename in filenames:
            if any([filename.endswith(ext) for ext in PIC_SUFFIXES]):
                pics.append(os.path.join(root, filename))
    return pics


def move_unused_files(all_files, used_files, directory):
    """Move files not present in the second list to directory."""
    num_moved = 0
    for all_file in all_files:
        # The rsplit removes the extension but we also test with the extension
        # as LaTeX can do both
        if ((all_file.rsplit('.', 1)[0] not in used_files) and
                (all_file not in used_files)):
            new_path = os.path.join(directory, all_file)
            new_dir_path = os.path.dirname(new_path)

            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)

            shutil.move(all_file, new_path)
            num_moved += 1

    return num_moved


def delete_empty_dirs(path, delete_root=False):
    """Delete empty folders contained in the path."""
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    contents = os.listdir(path)
    if contents:
        for element in contents:
            full_path = os.path.join(path, element)
            if os.path.isdir(full_path):
                delete_empty_dirs(full_path, True)

    # if folder empty, delete it
    contents = os.listdir(path)
    if not contents and delete_root:
        os.rmdir(path)


def main():
    """Main."""
    if len(sys.argv) < 3:
        print("ERROR: Not enough arguments!")
        print("USAGE: {0} TEX-FILES... PICS-DIR".format(sys.argv[0]))
        sys.exit(1)


    num_args = len(sys.argv)

    tex_filenames = sys.argv[1:(num_args-1)]
    pic_dir = sys.argv[num_args-1]

    for tex_filename in tex_filenames:
        if not os.path.isfile(tex_filename):
            print("ERROR: File {0} not found!".format(tex_filename))
            sys.exit(2)

    if not os.path.isdir(pic_dir):
        print("ERROR: Directory {0} not found!".format(pic_dir))
        sys.exit(3)


    real_paths = get_pics_from_dir(pic_dir)
    tex_paths = get_pics_from_tex(tex_filenames)
    num_moved = move_unused_files(real_paths, tex_paths, NOT_USED_DIR)
    delete_empty_dirs(pic_dir)

    print("Moved " + str(num_moved) +
          " unused files to directory '" + NOT_USED_DIR + "'.")


if __name__ == "__main__":
    main()
