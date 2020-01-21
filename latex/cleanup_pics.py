#!/usr/bin/env python3

"""
A small script to find and move pics not used in a LaTeX file.

Pics that are not included in the TeX file are moved
to a special dir for later use or deletion or whatever.
"""

__author__ = "Daniel Cervenkov"
__date__ = "Oct. 8, 2015"

import argparse
import os
import sys
import shutil

PIC_SUFFIXES = (".png", ".gif", ".pdf", ".ps", ".jpg", ".jpeg")
NOT_USED_DIR = "unused_pics"

def decode_arguments():
    """Decode CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("files", nargs="+")
    parser.add_argument("-D", "--dry-run", action="store_true",
                        help="don't move any files, just list what would be done")
    args = parser.parse_args()

    return args.dry_run, args.dir, args.files


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


def move_unused_files(all_files, used_files, used_dir, unused_dir, dry_run):
    """Move files not present in the second list to directory."""
    num_moved = 0
    size_moved = 0
    for all_file in all_files:
        # The rsplit removes the extension but we also test with the extension
        # as LaTeX can do both
        if ((all_file.rsplit('.', 1)[0] not in used_files) and
                (all_file not in used_files)):
            relative_path = os.path.relpath(all_file, used_dir)
            new_path = os.path.join(unused_dir, relative_path)
            new_dir_path = os.path.dirname(new_path)

            size_moved += os.path.getsize(all_file)
            num_moved += 1

            if dry_run:
                print(f"Move '{all_file}' > '{new_path}'")
            else:
                if not os.path.exists(new_dir_path):
                    os.makedirs(new_dir_path)
                shutil.move(all_file, new_path)


    return num_moved, size_moved


def delete_empty_dirs(path, dry_run, delete_root=False):
    """Delete empty folders contained in the path."""
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    contents = os.listdir(path)
    if contents:
        for element in contents:
            full_path = os.path.join(path, element)
            if os.path.isdir(full_path):
                delete_empty_dirs(full_path, dry_run, True)

    # if folder empty, delete it
    contents = os.listdir(path)
    if not contents and delete_root:
        if dry_run:
            print(f"Delete empty directory '{path}'")
        else:
            os.rmdir(path)
        delete_empty_dirs.num_deleted += 1


def main():
    """Main."""
    dry_run, pic_dir, tex_filenames = decode_arguments()

    for tex_filename in tex_filenames:
        if not os.path.isfile(tex_filename):
            print(f"ERROR: File {tex_filename} not found!")
            sys.exit(2)

    if not os.path.isdir(pic_dir):
        print(f"ERROR: Directory {pic_dir} not found!")
        sys.exit(3)

    real_paths = get_pics_from_dir(pic_dir)
    tex_paths = get_pics_from_tex(tex_filenames)
    unused_dir = os.path.join(os.path.split(pic_dir)[0], NOT_USED_DIR)
    num_moved, size_moved = move_unused_files(real_paths, tex_paths, pic_dir, unused_dir, dry_run)
    delete_empty_dirs.num_deleted = 0
    delete_empty_dirs(pic_dir, dry_run)

    print(f"Moved {num_moved} ({size_moved / (1024 * 1024):.1f} MB) unused files to directory '{NOT_USED_DIR}'.")
    if delete_empty_dirs.num_deleted:
        print(f"Deleted {delete_empty_dirs.num_deleted} empty directories.")


if __name__ == "__main__":
    main()
