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
