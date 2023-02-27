#!/usr/bin/env python3
"""
test client modules
"""
from client import GithubOrgClient
import client
from parameterized import parameterized, parameterized_class
from unittest.mock import PropertyMock, patch, Mock, call
import unittest
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Github org client class
    """

    @parameterized.expand(
        [
            ("google", {"google": True}),
            ("abc", {"abc": True}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org, expected, mock_request):
        """
        test org method
        """
        mock_request.return_value = expected
        org_client = GithubOrgClient(org)
        self.assertEqual(org_client.org, expected)
        mock_request.assert_called_once()

    def test_public_repos_url(self):
        """
        test public repos url method
        """
        expected = "www.yes.com"
        payload = {"repos_url": expected}
        string = "client.GithubOrgClient.org"
        with patch(string, PropertyMock(return_value=payload)):
            org_client = GithubOrgClient("x")
            self.assertEqual(org_client._public_repos_url, expected)

    @patch("client.get_json")
    def test_public_repos(self, get_json_mock):
        """
        test the public repos
        """
        jeff = {"name": "Jeff", "license": {"key": "a"}}
        bobb = {"name": "Bobb", "license": {"key": "b"}}
        suee = {"name": "Suee"}
        to_mock = "client.GithubOrgClient._public_repos_url"
        get_json_mock.return_value = [jeff, bobb, suee]
        with patch(to_mock, PropertyMock(return_value="www.yes.com")) as y:
            x = GithubOrgClient("x")
            self.assertEqual(x.public_repos(), ["Jeff", "Bobb", "Suee"])
            self.assertEqual(x.public_repos("a"), ["Jeff"])
            self.assertEqual(x.public_repos("c"), [])
            self.assertEqual(x.public_repos(45), [])
            get_json_mock.assert_called_once_with("www.yes.com")
            y.assert_called_once_with()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """test the license checker"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected
            )


@parameterized_class(
    (
        "org_payload",
        "repos_payload",
        "expected_repos",
        "apache2_repos"
    ), TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for github org client
    """

    @classmethod
    def setUpClass(cls):
        """prepare for testing"""
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch("requests.get")
        cls.get = cls.get_patcher.start()

        options = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """
        unprepare for testing
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        public repos test
        """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls(
            [
                call("https://api.github.com/orgs/x"),
                call(self.org_payload["repos_url"])
            ]
        )

    def test_public_repos_with_license(self):
        """
        public repos test
        """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls(
            [
                call("https://api.github.com/orgs/x"),
                call(self.org_payload["repos_url"])
            ]
        )
