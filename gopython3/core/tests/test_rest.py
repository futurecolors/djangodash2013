# coding: utf-8
import datetime
from django.utils.timezone import pytz
from rest_framework.test import APITestCase
from core.factories import JobFactory, SpecFactory


class TestApi(APITestCase):
    maxDiff = None

    def setUp(self):
        self.job = JobFactory(specs=['django-model-utils==1.5.0',
                                     'jsonfield==0.9.19'])

    def test_api_root(self):
        response = self.client.get('/api/v1/')
        assert 'jobs' in response.data
        assert 'packages' in response.data

    def test_post_job(self):
        response = self.client.post('/api/v1/jobs/', {'requirements': 'foo\nbar>1.2'})
        assert response.status_code == 201
        assert response['Location'] == 'http://testserver/api/v1/jobs/2/'

    def test_jobs_list(self):
        response = self.client.get('/api/v1/jobs/', format='json')
        assert response.data == {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                            'id': 1,
                            'url': 'http://testserver/api/v1/jobs/1/',
                            'status': 'running',
                            'created_at': self.job.created_at,
                            'updated_at': self.job.updated_at,
                            'started_at': None,
                            'finished_at': None
                        }]
        }

    def test_job_detail(self):
        response = self.client.get('/api/v1/jobs/1/', format='json')
        assert response.data == {
            'id': 1,
            'url': 'http://testserver/api/v1/jobs/1/',
            'status': 'running',
            'lines': [{'id': 'django-model-utils==1.5.0',
                      'package': {'id': 'django-model-utils/1.5.0',
                                  'name': 'django-model-utils', 'version': '1.5.0',
                                  'status': 'pending',
                                  'created_at': self.job.specs.all()[0].created_at,
                                  'updated_at': self.job.specs.all()[0].updated_at,
                      'pypi': {
                          'current': {
                              'version': '1.5.0',
                              'release_date': None,
                              'url': 'https://pypi.python.org/pypi/django-model-utils/1.5.0',
                              'python3': None},
                          'latest': {
                              'version': '1.5.0',
                              'release_date': None,
                              'url': 'https://pypi.python.org/pypi/django-model-utils/1.5.0',
                              'python3': None}
                      },
                      'repo': {
                          'url': '',
                          'last_commit_date': None},
                      'issues': [{'url': '', 'status': 'unknown'}],
                      'forks': [],
                      'ci': {
                          'url': '',
                          'status': 'unknown'},
                      'url': 'http://testserver/api/v1/packages/django-model-utils/1.5.0/'}},
                      {'id': 'jsonfield==0.9.19',
                       'package': {
                           'id': 'jsonfield/0.9.19',
                           'name': 'jsonfield',
                           'version': '0.9.19',
                           'status': 'pending',
                           'created_at': self.job.specs.all()[1].created_at,
                           'updated_at': self.job.specs.all()[1].updated_at,
                       'pypi': {
                            'current': {
                                'version': '0.9.19',
                                'release_date': None,
                                'url': 'https://pypi.python.org/pypi/jsonfield/0.9.19',
                                'python3': None},
                            'latest': {
                                'version': '0.9.19',
                                'release_date': None,
                                'url': 'https://pypi.python.org/pypi/jsonfield/0.9.19',
                                'python3': None}},
                       'repo': {
                           'url': '',
                           'last_commit_date': None},
                       'issues': [{
                            'url': '',
                            'status': 'unknown'}], 'forks': [],
                       'ci': {
                              'url': '',
                              'status': 'unknown'},
                       'url': 'http://testserver/api/v1/packages/jsonfield/0.9.19/'}}],
                       'created_at': self.job.created_at,
                       'updated_at': self.job.updated_at,
                       'started_at': None,
                       'finished_at': None}

    def test_job_detail_empty(self):
        job = JobFactory(lines=['Fabric>=1.4', 'nose'])
        response = self.client.get('/api/v1/jobs/2/', format='json')
        assert response.data == {
            "id": 2,
            "url": "http://testserver/api/v1/jobs/2/",
            "status": "pending",
            "lines": [{
                "id": "Fabric>=1.4",
                "package": None},
                {"id": "nose",
                 "package": None}
            ],
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "started_at": None,
            "finished_at": None
        }

    def test_spec_detail(self):
        spec =  SpecFactory(package__name='django_compressor',
                            version='1.3',
                            status='success',
                            package__repo_url='https://github.com/jezdez/django_compressor',
                            package__repo_last_commit_date=datetime.datetime(2013, 9, 22, 1, 56, 12, tzinfo=pytz.utc),
                            package__issue_url='https://github.com/jezdez/django_compressor/issues/360',
                            package__issue_status='closed',
                            package__ci_url='https://travis-ci.org/jezdez/django_compressor',
                            package__ci_status='passing',
                            release_date=datetime.datetime(2013, 9, 22, 1, 56, 12, tzinfo=pytz.utc),
                            python_versions=['3.3'],
                            package__comment_count=1,
                            package__comment_most_voted='Enlarge your python!'
        )
        package = spec.package

        response = self.client.get('/api/v1/packages/django_compressor/1.3/', format='json')
        assert response.data == {
             "id": "django_compressor/1.3",
             "name": "django_compressor",
             "version": "1.3",
             "status": "success",
             "created_at": spec.created_at,
             "updated_at": spec.updated_at,
             "pypi": {
                 "current": {
                     "url": "https://pypi.python.org/pypi/django_compressor/1.3",
                     "version": "1.3",
                     "python3": ["3.3"],
                     "release_date": spec.release_date
                 },
                 "latest": {
                     "url": "https://pypi.python.org/pypi/django_compressor/1.3",
                     "version": "1.3",
                     "python3": ["3.3"],
                     "release_date": spec.release_date
                 }
             },
             "repo": {
                 "url": "https://github.com/jezdez/django_compressor",
                 "last_commit_date": package.repo_last_commit_date,
             },
             "issues": [{
                 "url": "https://github.com/jezdez/django_compressor/issues/360",
                 "status": "closed"
             }],
             "forks": [],
             "ci": {
                 "url": "https://travis-ci.org/jezdez/django_compressor",
                 "status": "passing"
             },
             'url': 'http://testserver/api/v1/packages/django_compressor/1.3/'
        }

    def test_job_restart(self):
        job = JobFactory(specs=['foo==1'])
        job.specs.all().update(status='success')

        response = self.client.post('/api/v1/jobs/1/restart/', format='json')
        assert response.status_code == 400

        response = self.client.post('/api/v1/jobs/2/restart/', format='json')
        assert response.status_code == 202

    # TODO: test other non-working methods for extra security
