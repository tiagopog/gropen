"""
Main module of the command line application.
It contains all the logic for building and openning URLs on remote repos.
"""

import os
import re
import sys
import subprocess
import webbrowser

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
    Error class to be raised when something fails while trying to parse
    git-related data on the user's local environment.
    """

    DEFAULT_MESSAGE = "Error: non-existing or unsupported remote git repository"

    def __init__(self, message=None):
        self.message = message or self.DEFAULT_MESSAGE

    def __str__(self):
        return self.message


def run_shell(command):
    """
    Simple wrapper for shell commands.
    """
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, text=True)
    return result.stdout


def extract_paths(path):
    """
    Extracts some directory/file paths of interest for other gropen functions.
    """
    working_dir = os.path.abspath(os.getcwd())
    target_absolute_path = os.path.abspath(path)

    if os.path.isdir(target_absolute_path):
        target_absolute_path += "/"

    target_deepest_dir = os.path.dirname(target_absolute_path)
    os.chdir(target_deepest_dir)

    target_project_dir = run_shell("git rev-parse --show-toplevel").rstrip("\n")
    target_project_dir += "/"
    is_gropening_project_root = target_absolute_path == target_project_dir

    target_relative_path = (
        CURRENT_DIR_PATH
        if is_gropening_project_root
        else target_absolute_path.replace(target_project_dir, "")
    )

    os.chdir(working_dir)

    return {
        "working_dir": working_dir,
        "target_project_dir": target_project_dir,
        "target_relative_path": target_relative_path,
    }


def parse_git_remotes(remotes, remote_name=DEFAULT_REMOTE_NAME):
    """
    Parses the result string regarding the remote repos fetched from the
    local git repository.
    """
    pattern = REMOTE_PARSE_REGEX.format(remote_name=remote_name)
    match = re.search(pattern, remotes)

    if not match:
        raise UnsupportedRemoteError

    return match.group("domain"), match.group("path")


def build_remote_url(
    domain,
    project_path,
    branch=DEFAULT_GIT_BRANCH,
    path=DEFAULT_SOURCE_PATH,
    commit=None,
):
    """
    Builds the URL that will be opened on the user's default browser.

    For instance, "github.com/tiagopog/gropen/blob/main/gropen/gropen.py"
    gets composed as:

    - domain: "github.com"
    - project_path: "tiagopog/gropen"
    - remote_source_path: "blob"
    - branch: "main"
    - source_path: "gropen/gropen.py"

    """
    remote_source_path = build_remote_source_path(domain, path)
    versioning_path = build_versioning_path(domain, branch, commit)

    source_path = "" if path == CURRENT_DIR_PATH else path
    source_path = fix_line_anchor(domain, source_path)

    base_uri = "/".join(
        [domain, project_path, remote_source_path, versioning_path, source_path]
    )

    return DEFAULT_PROTOCOL + base_uri


def build_remote_source_path(domain, path):
    """
    Builds a proper path for source files which may vary for each remote
    repo supported by gropen.

    Source path on GitHub:

     - path/to/tree/**/
     - path/to/blob/**/*.*

    Source path on Bitbucket:

     - path/to/src/**/*.*

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
    Translates the line number notation (i.e. "path/to/file:n,n") to anchors
    in the URL that are supported by the remote repos.

    GitHub:

    - "path/to/file:42" => "path/to/file#L42"
    - "path/to/file:16,32" => "path/to/file#L16-L32"

    Bitbucket:

    - "path/to/file:42" => "path/to/file#lines-10"
    - "path/to/file:16,32" => "path/to/file#lines-10:12"

    """
    if ":" not in path:
        return path

    replacement = LINE_ANCHOR_REPLACEMENT[domain]["start_line"]
    fixed_path = re.sub(START_LINE_ANCHOR_REGEX, replacement, path)

    replacement = LINE_ANCHOR_REPLACEMENT[domain]["end_line"]
    fixed_path = re.sub(END_LINE_ANCHOR_REGEX, replacement, fixed_path)

    return fixed_path


def build_versioning_path(domain, branch, commit):
    """
    Makes sure to version the source path in accordance with each git
    remote provider supported by gropen.

    This is pretty much due to some remote repos like Bitbucket not
    supporting branches with a path in URL paths, for instance, for a
    branch named as "feature/add-bar":

    * Not supported: https://bitbucket.org/my-account/my-project/src/feature/add-bar/bar.py
    * Supported: https://bitbucket.org/my-account/my-project/src/366f5aad6900555eb79c8525b95a568928736e1b/bar.py

    """
    if domain == GITHUB_DOMAIN or "/" not in branch:
        return branch
    else:
        return commit


def fix_relative_path(path):
    """
    Makes it possible to gropen files from any given `path` in a
    git-versioned project.

    TODO: to be implemented.
    """
    pass


def run(path):
    """
    Runs all the steps for building and opening an URL for a given
    `path` on the remote repo.
    """
    paths = extract_paths(path)
    os.chdir(paths["target_project_dir"])

    remotes = run_shell("git remote -v")
    domain, project_path = parse_git_remotes(remotes)
    branch = run_shell("git rev-parse --abbrev-ref HEAD").rstrip("\n")
    commit = run_shell("git rev-parse HEAD").rstrip("\n")
    relative_path = paths["target_relative_path"]
    remote_url = build_remote_url(domain, project_path, branch, relative_path, commit)

    os.chdir(paths["working_dir"])
    webbrowser.open(remote_url)


def main():
    """
    Command line application's entry point.
    """
    has_arguments = len(sys.argv) > 1
    path = sys.argv[1] if has_arguments else DEFAULT_SOURCE_PATH

    try:
        run(path)
    except UnsupportedRemoteError as error:
        print(error)
        os._exit(os.EX_USAGE)
