import re
import sys
import subprocess

DEFAULT_PROTOCOL = "https://"
DEFAULT_REMOTE_NAME = "origin"

PARSE_REGEX = (
    r"^{remote_name}\t(https://|git@)(?P<domain>[\w\-\.]+)(\/|:)(?P<path>[\w\-\/]+)"
)

SOURCE_PATH = {"github.com": "blob", "bitbucket.org": "src"}


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
    pattern = PARSE_REGEX.format(remote_name=remote_name)
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

    base_uri = "/".join([base_uri, source_path, branch, path])
    return DEFAULT_PROTOCOL + base_uri


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
