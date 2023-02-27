#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from client import GithubOrgClient
from typing import Dict
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Dict):
        GithubOrgClient(org_name).org()
        mock_get_json.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org_name))

class TestGithubOrgClient(unittest.TestCase):
    @patch('client.get_json')
    def test_org(self, mock_get_json):
        test_payload = {'test_key': 'test_value'}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient('test_org')
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with('https://api.github.com/orgs/test_org')

    @patch.object(GithubOrgClient, 'org', new_callable=property)
    def test_public_repos_url(self, mock_org):
        test_payload = [{'name': 'test_repo1'}, {'name': 'test_repo2'}]
        mock_org.return_value = {'repos_url': 'http://test-repos-url.com'}
        with patch('client.get_json', return_value=test_payload) as mock_get_json:
            client = GithubOrgClient('test_org')
            self.assertEqual(client._public_repos_url, 'http://test-repos-url.com')
            mock_get_json.assert_called_once_with('http://test-repos-url.com')

if __name__ == '__main__':
    unittest.main()

class TestGithubOrgClient(TestCase):
    
    @parameterized.expand([
        ("google", None, ["repo1", "repo2"]),
        ("abc", "MIT", ["repo3"]),
    ])
    @mock.patch("client.get_json")
    @mock.patch("client.GithubOrgClient._public_repos_url", new_callable=mock.PropertyMock)
    def test_public_repos(self, org_name, license_key, expected_repos, mock_repos_url, mock_get_json):
        mock_repos_url.return_value = "http://api.github.com/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3", "license": {"key": "MIT"}},
        ]
        
        client = GithubOrgClient(org_name)
        repos = client.public_repos(license=license_key)
        
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once()
        self.assertEqual(repos, expected_repos)
