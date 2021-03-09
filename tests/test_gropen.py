import unittest


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
    def test_building_directory_path_for_github(self):
        pass

    def test_building_file_path_for_github(self):
        pass

    def test_building_file_path_with_line_anchor_for_github(self):
        pass

    def test_building_file_path_with_line_range_anchor_for_github(self):
        pass

    def test_building_directory_path_for_bitbucket(self):
        pass

    def test_building_file_path_for_bitbucket(self):
        pass

    def test_building_file_path_with_line_anchor_for_bitbucket(self):
        pass

    def test_building_file_path_with_line_range_anchor_for_bitbucket(self):
        pass

    def test_building_url_for_unsupported_remoted_repo(self):
        pass
