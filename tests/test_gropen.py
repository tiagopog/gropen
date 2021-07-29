import unittest

from gropen import gropen


class ParseGitRemotesTest(unittest.TestCase):
    def test_parsing_ssh_based_uris(self):
        remotes = (
            "origin\tgit@github.com:tiagopog/gropen.git (fetch)\n"
            "origin\tgit@github.com:tiagopog/gropen.git (push)\n"
            "bitbucket\tgit@bitbucket.org:tiagopog/gropen.git (fetch)\n"
            "bitbucket\tgit@bitbucket.org:tiagopog/gropen.git (push)\n"
            "github\tgit@github.com:tiagopog/gropen.git (fetch)\n"
            "github\tgit@github.com:tiagopog/gropen.git (push)\n"
        )

        # Assertions on implicit default remote repo (origin):
        domain, path = gropen.parse_git_remotes(remotes)

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

        # Assertions on explicit remote repo (GitHub):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="github")

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

        # Assertions on explicit remote repo (Bitbucket):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="bitbucket")

        self.assertEqual(domain, gropen.BITBUCKET_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

    def test_parsing_http_based_uris(self):
        remotes = (
            "origin\thttps://github.com/tiagopog/gropen (fetch)\n"
            "origin\thttps://github.com/tiagopog/gropen (push)\n"
            "bitbucket\thttps://tiagopog@bitbucket.org/tiagopog/gropen.git (fetch)\n"
            "bitbucket\thttps://tiagopog@bitbucket.org/tiagopog/gropen.git (push)\n"
            "github\thttps://github.com/tiagopog/gropen.git (fetch)\n"
            "github\thttps://github.com/tiagopog/gropen.git (push)\n"
        )

        # Assertions on implicit default remote repo (origin):
        domain, path = gropen.parse_git_remotes(remotes)

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

        # Assertions on explicit remote repo (GitHub):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="github")

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

        # Assertions on explicit remote repo (Bitbucket):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="bitbucket")

        self.assertEqual(domain, gropen.BITBUCKET_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

    def test_parsing_with_no_origin_remote(self):
        remotes = (
            "bitbucket\thttps://tiagopog@bitbucket.org/tiagopog/gropen.git (fetch)\n"
            "bitbucket\thttps://tiagopog@bitbucket.org/tiagopog/gropen.git (push)\n"
            "github\thttps://github.com/tiagopog/gropen.git (fetch)\n"
            "github\thttps://github.com/tiagopog/gropen.git (push)\n"
        )

        # Assertions on implicit default remote repo (origin):
        expected_error = gropen.UnsupportedRemoteError
        self.assertRaises(expected_error, gropen.parse_git_remotes, remotes)

        # Assertions on explicit remote repo (GitHub):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="github")

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

        # Assertions on explicit remote repo (Bitbucket):
        domain, path = gropen.parse_git_remotes(remotes, remote_name="bitbucket")

        self.assertEqual(domain, gropen.BITBUCKET_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen")

    def test_parsing_uri_paths_with_non_alphanumeric_chars(self):
        remotes = (
            "origin\thttps://github.com/tiagopog/gropen.foo_bar-foobar.git (fetch)\n"
        )

        domain, path = gropen.parse_git_remotes(remotes)

        self.assertEqual(domain, gropen.GITHUB_DOMAIN)
        self.assertEqual(path, "tiagopog/gropen.foo_bar-foobar")


class BuildRemoteURLTest(unittest.TestCase):
    def test_building_url_for_unsupported_remoted_repo(self):
        pass

    ##
    # GitHub
    ##

    def test_building_directory_path_for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = "https://github.com/username/my-project/blob/main/foo/"

        self.assertEqual(url, expected_url)

    def test_building_file_path_for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = "https://github.com/username/my-project/blob/main/foo/bar.py"

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_complex_branch_name_for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "release/2.4.8"
        path = "foo/bar.py"
        commit = "1217ac95844c1ae1deca58144133d68f3b171056"

        url = gropen.build_remote_url(domain, project_path, branch, path, commit)
        expected_url = (
            "https://github.com/username/my-project/blob/release/2.4.8/foo/bar.py"
        )

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_line_anchor_for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py:42"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = "https://github.com/username/my-project/blob/main/foo/bar.py#L42"

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_line_range_anchor_for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py:16,32"

        url = gropen.build_remote_url(domain, project_path, branch, path)

        expected_url = (
            "https://github.com/username/my-project/blob/main/foo/bar.py#L16-L32"
        )

        self.assertEqual(url, expected_url)

    ##
    # Bitbucket
    ##

    def test_building_directory_path_for_bitbucket(self):
        domain = gropen.BITBUCKET_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = "https://bitbucket.org/username/my-project/src/main/foo/"

        self.assertEqual(url, expected_url)

    def test_building_file_path_for_bitbucket(self):
        domain = gropen.BITBUCKET_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = "https://bitbucket.org/username/my-project/src/main/foo/bar.py"

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_complex_branch_name_for_bitbucket(self):
        domain = gropen.BITBUCKET_DOMAIN
        project_path = "username/my-project"
        branch = "release/2.4.8"
        path = "foo/bar.py"
        commit = "1217ac95844c1ae1deca58144133d68f3b171056"

        url = gropen.build_remote_url(domain, project_path, branch, path, commit)

        expected_url = (
            "https://bitbucket.org/username/my-project/"
            "src/1217ac95844c1ae1deca58144133d68f3b171056/"
            "foo/bar.py"
        )

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_line_anchor_for_bitbucket(self):
        domain = gropen.BITBUCKET_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py:42"

        url = gropen.build_remote_url(domain, project_path, branch, path)
        expected_url = (
            "https://bitbucket.org/username/my-project/src/main/foo/bar.py#lines-42"
        )

        self.assertEqual(url, expected_url)

    def test_building_file_path_with_line_range_anchor_for_bitbucket(self):
        domain = gropen.BITBUCKET_DOMAIN
        project_path = "username/my-project"
        branch = "main"
        path = "foo/bar.py:16,32"

        url = gropen.build_remote_url(domain, project_path, branch, path)

        expected_url = (
            "https://bitbucket.org/username/my-project/src/main/foo/bar.py#lines-16:32"
        )

        self.assertEqual(url, expected_url)
