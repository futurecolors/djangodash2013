# coding: utf-8
import logging
from django.test import TestCase
import pytest
from api.github import Github


logger = logging.getLogger('api')


@pytest.mark.functional
class GithubRealTest(TestCase):

    def setUp(self):
        self.gh = Github()
        logger.setLevel(logging.DEBUG)

    def tearDown(self):
        logger.setLevel(logging.ERROR)

    def test_github_api_with_real_repos(self):
        # Get 5 most popular repos
        repos = self.gh.api.search.repositories.GET(params={
            'q': 'language:python',
            'per_page': 5,
            'sort': 'stars',
        }).json()

        for i, repo in enumerate(repos['items']):
            full_name = repo['full_name']
            print(i,
                  full_name,
                  'forks: %s' % len(self.gh.get_py3_forks(full_name)),
                  'issues: %s' % len(self.gh.get_py3_issues(full_name) or self.gh.get_py3_pulls(full_name))
            )
