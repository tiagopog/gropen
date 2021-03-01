import re
import sys
import subprocess

DEFAULT_PROTOCOL = "https://"
DEFAULT_REMOTE_NAME = "origin"

GITHUB_DOMAIN = "github.com"
BITBUCKET_DOMAIN = "bitbucket.org"

SOURCE_PATH = {GITHUB_DOMAIN: "blob", BITBUCKET_DOMAIN: "src"}

START_LINE_ANCHOR_REGEX = re.compile(r":(\d+)")
END_LINE_ANCHOR_REGEX = re.compile(r",(\d+)$")

LINE_ANCHOR_REPLACEMENT = {
    GITHUB_DOMAIN: {"start_line": "#L\\1", "end_line": "-L\\1"},
    BITBUCKET_DOMAIN: {"start_line": "#lines-\\1", "end_line": ":\\1"},
}

REMOTE_PARSE_REGEX = (
    r"^{remote_name}\t(https://|git@)(?P<domain>[\w\-\.]+)(\/|:)(?P<path>[\w\-\/]+)"
)


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
    return match.group("domain"), match.group("path") if match else None


def build_remote_url(domain, project_path, branch=None, path=None):
    """
    TODO
    """
    base_uri = "/".join([domain, project_path])

    if None in (branch, path):
        return DEFAULT_PROTOCOL + base_uri

    source_path = SOURCE_PATH.get(domain)
    if not source_path:
        return

    path = fix_line_anchor(domain, path)
    base_uri = "/".join([base_uri, source_path, branch, path])
    return DEFAULT_PROTOCOL + base_uri


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
    pass


def gropen(path):
    """
    TODO
    """
    remotes = run_shell("git remote -v")
    domain, project_path = parse_remotes(remotes)
    branch = run_shell("git rev-parse --abbrev-ref HEAD").rstrip("\n")
    remote_url = build_remote_url(domain, project_path, branch, path)

    print(f"Opening {remote_url}")
    run_shell(f"open {remote_url}")


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        path = None
    gropen(path)
