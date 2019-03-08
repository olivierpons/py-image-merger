#!/usr/bin/env python
"""
Images merger

Merges a directory of images (recursively) into one big image file.

"""
import textwrap
import argparse
import os
from PIL import Image

__author__ = "Olivier Pons"
__copyright__ = "Copyright 2019, HQF Development"
__credits__ = ["https://stackoverflow.com/"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Olivier Pons"
__email__ = "olivier.pons@gmail.com"
__status__ = "Production"


# Arg parsing to accept boolean in many different ways:
# Thanks stackoverflow https://stackoverflow.com/
#                      questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        --------------------------------
        Image merger
        --------------------------------
            Merge image files into one
            (C) HQF Development - 2019
    '''))
parser.add_argument("-s", "--src",
                    help="src directory where all image files are", type=str)
parser.add_argument("-d", "--dst",
                    help="destination image file", type=str)
parser.add_argument("-w", "--max-width",
                    help="max width of dst image file", type=int)
parser.add_argument("-b", "--best-fit", nargs='?', const=True, default=False,
                    help="try the closest to 'width=height' of dst image file",
                    type=str2bool)

args = parser.parse_args()
print(args)
if args.src is None:
    print("There's no src!")
    parser.print_help()
    exit(0)

if args.dst is None:
    print("There's no dst!")
    parser.print_help()
    exit(0)

if args.best_fit and args.max_width is not None:
    print("Max width and best fit are mutual exclusive, choose only one")
    parser.print_help()
    exit(0)

images = []
for root, sub_dirs, files in os.walk(args.src):
    for subdir in sub_dirs:
        print('\t- subdirectory ' + subdir)
    for filename in files:
        images.append(os.path.join(root, filename))

image_files = [image for image in images if image.lower().endswith(('.gif',
                                                                    '.jpg',
                                                                    '.png', ))]
images = map(Image.open, image_files)
widths, heights = zip(*(i.size for i in images))
max_width = total_width = sum(widths)
max_height = max(heights)

if args.best_fit or args.max_width:
    # Customized version of the stackoverflow answer (see in the "else:" code)
    # first loop to find the "correct" max width:
    if args.max_width:
        max_width = args.max_width
    else:
        # to do: find the right formulae, here it's a simple division:
        max_width = max_width // 2
    max_width_correct = 0
    max_height_correct = 0
    x_offset = 0
    y_offset = 0
    y_max_offset = 0
    images = map(Image.open, image_files)
    for im in images:
        width, height = im.size
        x_offset += width
        y_max_offset = max(y_max_offset, height)
        if x_offset > max_width:
            max_width_correct = max(max_width_correct, x_offset)
            x_offset = 0
            y_offset += y_max_offset
            max_height_correct += y_max_offset
            y_max_offset = 0

    max_height_correct += y_max_offset

    new_im = Image.new('RGB', (max_width_correct, max_height_correct))
    x_offset = 0
    y_offset = 0
    y_max_offset = 0
    images = map(Image.open, image_files)
    for im in images:
        new_im.paste(im, (x_offset, y_offset))
        width, height = im.size
        x_offset += width
        y_max_offset = max(y_max_offset, height)
        if x_offset > max_width:
            x_offset = 0
            y_offset += y_max_offset
            y_max_offset = 0

else:
    # Very simple save
    # Thanks stackoverflow :
    # https://stackoverflow.com/
    # questions/30227466/combine-several-images-horizontally-with-python
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    images = map(Image.open, image_files)
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

new_im.save(args.dst)
