import unittest

from gropen import gropen


class ParseGitRemotesTest(unittest.TestCase):
    def test_parsing_several_remotes(self):
        pass

    def test_parsing_git_based_uris(self):
        pass

    def test_parsing_http_based_uris(self):
        pass

    def test_parsing_with_no_origin_remote(self):
        pass


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

    def test_building_file_path__for_github(self):
        domain = gropen.GITHUB_DOMAIN
        project_path = "username/my-project"
        branch = "release/2.4.8"
        path = "foo/bar.py"
        commit = "1217ac95844c1ae1deca58144133d68f3b171056"

        url = gropen.build_remote_url(domain, project_path, branch, path, commit)
        expected_url = "https://github.com/username/my-project/blob/release/2.4.8/foo/bar.py"

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

    def test_building_file_path_in_branch_with_paths_for_bitbucket(self):
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
