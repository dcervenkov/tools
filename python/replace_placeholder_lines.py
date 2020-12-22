#!/usr/bin/env python3

import argparse
import sys


def decode_args():
    """Decode CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k",
        "--keyword",
        help=(
            "keyword triggering replacement at the beggining of line "
            "(whitespace ignored)"
        ),
        default="%%REPLACE%% ",
    )
    parser.add_argument("file")
    args = parser.parse_args()
    return args


def replace_and_print(path: str, keyword: str) -> int:
    """Replace line starting with keyword by contents of file.

    The line triggering the replacement looks like [KEYWORD][PATH], so e.g.,
    %%REPLACE%% /tmp/file

    Args:
        path: Path to the file to process.
        keyword: Keyword which triggers replacement.
    """
    num_replacements = 0
    with open(path) as file:
        for line in file:
            if line.strip().startswith(keyword):
                num_replacements += 1
                # We remove the last character - the newline
                replace_path = line[len(keyword) : -1]  # noqa
                with open(replace_path) as replace_file:
                    replace_text = replace_file.read()
                print(replace_text, end="")
            else:
                print(line, end="")

    return num_replacements


def main():
    """Decode arguments and call the replacement function."""
    args = decode_args()
    num_replaced = replace_and_print(args.file, args.keyword)
    if num_replaced == 0:
        print("ERROR: No lines to replace found!")
        sys.exit(1)


if __name__ == "__main__":
    main()
