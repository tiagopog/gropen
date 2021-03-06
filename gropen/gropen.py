import os
import re
import sys
import subprocess

CURRENT_DIR_PATH = "."

DEFAULT_PROTOCOL = "https://"
DEFAULT_REMOTE_NAME = "origin"
DEFAULT_GIT_BRANCH = "main"
DEFAULT_SOURCE_PATH = CURRENT_DIR_PATH

GITHUB_DOMAIN = "github.com"
BITBUCKET_DOMAIN = "bitbucket.org"

REMOTE_TREE_PATH = {GITHUB_DOMAIN: "tree", BITBUCKET_DOMAIN: "src"}
REMOTE_SOURCE_PATH = {GITHUB_DOMAIN: "blob", BITBUCKET_DOMAIN: "src"}

START_LINE_ANCHOR_REGEX = re.compile(r":(\d+)")
END_LINE_ANCHOR_REGEX = re.compile(r",(\d+)$")

LINE_ANCHOR_REPLACEMENT = {
    GITHUB_DOMAIN: {"start_line": "#L\\1", "end_line": "-L\\1"},
    BITBUCKET_DOMAIN: {"start_line": "#lines-\\1", "end_line": ":\\1"},
}

REMOTE_PARSE_REGEX = (
    r"{remote_name}\t(https://|git@)(?P<domain>[\w\-\.]+)(\/|:)(?P<path>[\w\-\/]+)"
)


class UnsupportedRemoteError(Exception):
    """
    TODO
    """

    DEFAULT_MESSAGE = "Error: unsupported remote git repository"

    def __init__(self, message=None):
        self.message = message or self.DEFAULT_MESSAGE

    def __str__(self):
        return self.message


def run_shell(command):
    """
    TODO
    """
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, text=True)
    return result.stdout


def parse_remotes(remotes, remote_name=DEFAULT_REMOTE_NAME):
    """
    TODO
    """
    pattern = REMOTE_PARSE_REGEX.format(remote_name=remote_name)
    match = re.search(pattern, remotes)

    if not match:
        raise UnsupportedRemoteError

    return match.group("domain"), match.group("path")


def build_remote_url(domain, project_path, branch, path):
    """
    TODO
    """
    remote_source_path = get_remote_source_path(domain, path)
    source_path = "" if path == CURRENT_DIR_PATH else path
    source_path = fix_line_anchor(domain, source_path)
    base_uri = "/".join([domain, project_path, remote_source_path, branch, source_path])
    return DEFAULT_PROTOCOL + base_uri


def get_remote_source_path(domain, path):
    """
    TODO
    """
    try:
        if path == CURRENT_DIR_PATH:
            return REMOTE_TREE_PATH[domain]
        else:
            return REMOTE_SOURCE_PATH[domain]
    except KeyError:
        raise UnsupportedRemoteError


def fix_line_anchor(domain, path):
    """
    TODO
    """
    if ":" not in path:
        return path

    replacement = LINE_ANCHOR_REPLACEMENT[domain]["start_line"]
    fixed_path = re.sub(START_LINE_ANCHOR_REGEX, replacement, path)

    replacement = LINE_ANCHOR_REPLACEMENT[domain]["end_line"]
    fixed_path = re.sub(END_LINE_ANCHOR_REGEX, replacement, fixed_path)

    return fixed_path


def fix_relative_path():
    """
    TODO
    """
    pass


def run(path):
    """
    TODO
    """
    remotes = run_shell("git remote -v")
    domain, project_path = parse_remotes(remotes)
    branch = run_shell("git rev-parse --abbrev-ref HEAD").rstrip("\n")
    remote_url = build_remote_url(domain, project_path, branch, path)
    run_shell(f"open {remote_url}")


def main():
    """
    TODO
    """
    has_arguments = len(sys.argv) > 1
    path = sys.argv[1] if has_arguments else DEFAULT_SOURCE_PATH

    try:
        run(path)
    except UnsupportedRemoteError as error:
        print(error)
        os._exit(os.EX_USAGE)
