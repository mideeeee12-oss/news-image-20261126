#!/usr/bin/env python3
"""Hand the news picture in: copy entry.png to the output directory.

The entry for make.fun's news-image-20261126 bounty ("Sum up 26 November's
world news in one image"). The picture itself — a newspaper front page
summing up Thursday 26 November 2026 — was drawn by render_image.py, kept
beside this file; the rules expressly allow a repository holding the image
and a program that copies it. Standard library only, no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, 'entry.png'), os.path.join(out_dir, 'entry.png'))


if __name__ == '__main__':
    main()
