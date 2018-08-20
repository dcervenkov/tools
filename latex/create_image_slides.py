#!/usr/bin/env python3

"""
Script that creates LaTeX slides with all supplied images.

Number of columns and rows per slide can be changed via CLI arguments as well
as the includegraphics options.
"""

__author__ = "Daniel Cervenkov"
__date__ = "Mar. 11, 2017"

import argparse
import os

PIC_SUFFIXES = (".png", ".gif", ".pdf", ".ps", ".jpg", ".jpeg")

HEADER = ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
          "\\begin{frame}\n\n"
          "\\noindent\\makebox[\\textwidth][c]{\n"
          "\\begin{minipage}{1.2\\textwidth}\n"
          "  \\centering\n")

FOOTER = ("\\end{minipage}}\n\n"
          "\\end{frame}")


def decode_arguments():
    """Decode CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Script that creates LaTeX slides with all supplied images.")

    parser.add_argument("-y", "--vertical", type=int,
                        nargs='?', default=2, help="number of image rows")

    parser.add_argument("-x", "--horizontal", type=int,
                        nargs='?', default=3, help="number of image columns")

    parser.add_argument("-o", "--image-options", type=str, nargs='?',
                        default=r"width=0.305\textwidth, angle=-90",
                        help="options for includegraphics")

    parser.add_argument("images", type=str, nargs='+')
    args = parser.parse_args()

    return args.images, args.horizontal, args.vertical, args.image_options


def sanitize_images(images):
    """Delete directories and other non-images from the list."""
    sanitized_images = []
    for image in images:
        if os.path.isfile(image) and image.lower().endswith(PIC_SUFFIXES):
            sanitized_images.append(image)
        elif os.path.isfile(image):
            print("Non-image file '" + image + "' removed from the list")

    return sanitized_images


def create_slides(images, horizontal, vertical, image_options):
    """Create slides from an image list."""
    slides = []
    num_images_per_slide = horizontal * vertical
    for i in range(0, len(images), num_images_per_slide):
        slides.append(create_slide(
            images[i:i + num_images_per_slide], horizontal, image_options))

    return slides


def create_slide(images, horizontal, image_options):
    """Create a single slide."""
    slide = HEADER
    for i, image in enumerate(images):
        slide = slide + \
            "  \\includegraphics[{}]{{{}}}".format(image_options, image)
        if (i + 1) % horizontal == 0 and i != 0:
            slide = slide + r'\\'
        slide = slide + '\n'
    slide += FOOTER

    return slide


def main():
    """Main."""
    images, horizontal, vertical, image_options = decode_arguments()
    images = sanitize_images(images)
    slides = create_slides(images, horizontal, vertical, image_options)

    for slide in slides:
        print(slide)


if __name__ == "__main__":
    main()
