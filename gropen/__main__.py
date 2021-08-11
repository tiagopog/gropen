"""
gropen package main entry point.
It's executed when gropen directory is called as script.
"""

from .gropen import main
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-v",
    "--version",
    action="store_true",
    dest="version",
    default=False,
    help="gropen version",
)

(options, _) = parser.parse_args()

main(options)
