# coding: utf-8
from .base import HammockAPI


class TravisCI(HammockAPI):
    base_url = 'https://api.travis-ci.org'

    def headers(self):
        return {
            'Accept': 'application/vnd.travis-ci.2+json, */*; q=0.01'
        }

    def get_build_status(self, full_name):
        """ Get build status of the repo

            JSON: https://api.travis-ci.org/docs/#/repos/:owner_name/:name
        """
        repo = self.api.repos(full_name).GET().json().get('repo', {})
        try:
            return {
                'html_url': 'https://travis-ci.org/%s' % repo['slug'],
                'last_build_state': repo['last_build_state'] or 'unknown',
            }
        except KeyError:
            return {}
