"""
gropen package main entry point.
It's executed when gropen directory is called as script.
"""

from .gropen import main
from optparse import OptionParser

usage = "usage: gropen [options] local_path_to_gropen"
parser = OptionParser(usage=usage)

parser.add_option(
    "-v",
    "--version",
    action="store_true",
    dest="version",
    default=False,
    help="gropen version",
)

parser.add_option(
    "-u",
    "--url",
    action="store_true",
    dest="url_only",
    default=False,
    help="prints the repo URL instead of opening it on a web browser",
)

(options, args) = parser.parse_args()
main(args, options)
