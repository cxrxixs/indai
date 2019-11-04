# api/herokuapi.py

import os
import sys
import json
import requests
from subprocess import Popen, PIPE


class Heroku():

    def __init__(self, credential, repo_hash):
        self.username = credential['heroku']['username']
        self.password = credential['heroku']['password']
        self.repo_hash = repo_hash
        self.URL = 'https://api.heroku.com'
        self.dir_name = os.getcwd().split('/')[-1]
        self.app_name = ''.join(['temp-', self.dir_name])

    def generate_token(self):
        """Generate Heroku token using heroku cli"""
        self.TOKEN = Popen(
            'heroku auth:token',
            stdout=PIPE,
            shell=True).communicate()[0].decode(
                'utf-8').strip()

        self.HEADERS = {
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer {}' .format(self.TOKEN)
        }

    def create_app(self):
        """Create heroku app"""

        # TODO
        # Create config file for APP setup
        print('Creating Heroku app...', end='')
        payload = {
            'name': self.app_name,
            'region': 'us',
            'stack': 'heroku-18'
        }

        API_LINK = '/apps'

        resp = requests.post(
            self.URL + API_LINK,
            data=payload,
            headers=self.HEADERS
        )

        if resp.status_code == 201:
            self.response = json.loads(resp.content)
            print('Done')

        else:
            print('CREATE APP ERROR: {}' .format(resp.status_code))
            print('APP NAME: {}' .format(self.app_name))
            print(json.loads(resp.content))
            sys.exit(1)

    def get_upload_path(self):

        API_LINK = '/apps/{}/sources' .format(self.app_name)

        resp = requests.post(
            self.URL + API_LINK,
            headers=self.HEADERS
        )

        if resp.status_code == 201:
            self.source_blob = json.loads(resp.content)

        else:
            print('SOURCE Error: {}' .format(resp.status_code))
            print(json.loads(resp.content))
            sys.exit(1)

    def upload_source(self):

        print('Uploading source...', end='')
        self.get_upload_path()

        with open(self.app_name + '.tar.gz', 'rb') as infile:
            data = infile.read()

        resp = requests.put(
            self.source_blob['source_blob']['put_url'],
            headers={
                'Content-Type': '',
            },
            data=data
        )

        if resp.status_code == 200:
            print('Done')
        else:
            print('Upload source ERROR: {}' .format(resp.status_code))
            sys.exit(1)

    def build_app(self):
        print('Building app...', end='')
        self.upload_source()
        API_LINK = '/apps/{}/builds' .format(self.app_name)

        payload = {
            'source_blob':
            {
                'url': self.source_blob['source_blob']['get_url'],
                'version': self.repo_hash
            }
        }

        resp = requests.post(
            self.URL + API_LINK,
            headers=self.HEADERS,
            data=json.dumps(payload)
        )

        if resp.status_code == 201:
            self.slug = json.loads(resp.content)
            print('Done')

        else:
            print('Build ERROR {}' .format(resp.status_code))
            print(resp.content)
            sys.exit(1)

    def setup_database(self):
        """Allocate datbase"""

        # Postgresql database provision
        API_LINK = '/apps/{}/addons' .format(self.app_name)

        payload = {
            'plan': 'heroku-postgresql:hobby-dev'
        }

        print('Povissioning database...', end='')
        resp = requests.post(
            self.URL + API_LINK,
            headers=self.HEADERS,
            data=payload)

        if resp.status_code == 201:
            self.addons = json.loads(resp.content)
            print('Done')

        else:
            print('ERROR: {}' .format(resp.status_code))
            print(resp.content)
            sys.exit(1)

    def setup_confvar(self):
        """Update config variables"""

        API_LINK = '/apps/{}/config-vars' .format(self.app_name)

        payload = {
            'FLASK_APP': 'run.py',
            'FLASK_CONFIG': 'development',
            'SECRET': 'Sup4S3c37keynumbahWanxX'
        }

        resp = requests.patch(
            self.URL + API_LINK,
            headers=self.HEADERS,
            data=payload
        )

        if resp.status_code == 200:
            print('Successfully updated config variables')

        else:
            print('Config varialbe update ERROR: {}' .format(resp.status_code))
            sys.exit(1)

    def destroy_app(self):

        print('Clearing Heroku app...', end='')
        self.generate_token()
        API_LINK = '/apps/{}' .format(self.app_name)

        resp = requests.delete(
            self.URL + API_LINK,
            headers=self.HEADERS
        )

        if resp.status_code == 200:
            print('Done')
            print('Successfully deleted app {}'. format(self.app_name))

        else:
            print('HEROKU Error')
            print('Error deleting app: {}' .format(resp.status_code))

    def deploy(self):

        self.generate_token()
        self.create_app()
        self.build_app()
        self.setup_database()
        self.setup_confvar()
