# api/githubapi.py

import os
import sys
import time
import json
import requests
import subprocess


class Github():

    def __init__(self, credential):
        self.username = credential['github']['username']
        self.password = credential['github']['password']
        self.URL = "https://api.github.com"
        self.dir_name = os.getcwd().split('/')[-1]
        self.repo_name = ''.join(['temp-', self.dir_name])

    def create_repo(self):
        """Create temporary github repo"""

        API_LINK = "/user/repos"

        headers = {
            'content-type': 'application/json',
            'User-Agent': 'indai'
        }

        payload = {
            'name': self.repo_name,
            'description': 'temporary repo for {}' .format(self.dir_name),
            'private': 'true'
        }

        resp = requests.post(
            self.URL + API_LINK,
            auth=(self.username, self.password),
            headers=headers,
            data=json.dumps(payload)
        )

        if resp.status_code == 201:
            # wait couple of sec for repo to be created
            print('Successfully created repo {}' .format(self.repo_name))

            self.response = json.loads(resp.text)
            # return json.loads(resp.text)

        else:
            print('Error: {}' .format(resp.status_code))
            # return json.loads(resp.text)
            # error 401: Unauthorized access
            sys.exit(1)

    def upload_repo(self):
        print('Pushing repo to Github...', end='')
        time.sleep(5)

        # Add new repo to git remote
        cmd_add_remote = 'git remote add indai {}' .format(
            self.response['svn_url'])
        subprocess.call(cmd_add_remote, shell=True)

        # Push to remote
        # cmd_push_remote = 'git push indai master'
        cmd_push_remote = 'git push indai HEAD:master'
        subprocess.call(cmd_push_remote, shell=True)

        print('Done')

    def download_repo(self):
        # https://github.com/:user/:repo/archive/master.tar.gz
        # GET /repos/:owner/:repo/:archive_format/:ref

        print('Downloading archived repo...', end='')
        headers = {'User-Agent': 'indai'}
        API_LINK = '/repos/{}/{}/tarball/master' .format(
            self.username, self.repo_name)

        resp = requests.get(
            self.URL + API_LINK,
            auth=(self.username, self.password),
            headers=headers)

        if resp.status_code == 200:
            print('Done')
            print('Saving archived repo...', end='')

            with open(self.repo_name + '.tar.gz', 'wb') as outfile:
                outfile.write(resp.content)
            print('Done')

        else:
            print('Error: {}' .format(resp.status_code))

    def repo_hash(self):
        """Get hash of archived repo"""

        API_LINK = '/repos/{}/{}/git/ref/heads/master' .format(
            self.username, self.repo_name)

        print('Acquiring repo hash...', end='')
        resp = requests.get(
            self.URL + API_LINK,
            headers={'User-Agent': 'indai'},
            auth=(self.username, self.password)
        )

        if resp.status_code == 200:
            print('Done')
            return (json.loads(resp.content))['object']['sha']

        else:
            print('Error: {}' .format(resp.status_code))
            print(json.loads(resp.content))

    def destroy_repo(self):

        # Remove remote
        cmd_remove_remote = 'git remote remove indai'
        subprocess.call(cmd_remove_remote, shell=True)

        # Delete tarball
        cmd_delete_tar = 'rm {}' .format(self.repo_name + '.tar.gz')
        subprocess.call(cmd_delete_tar, shell=True)

        # Delete repo
        # DELETE /repos/:owner/:repo

        headers = {
            'User-Agent': 'indai'
        }
        API_LINK = '/repos/{}/{}' .format(
            self.username,
            self.repo_name)

        resp = requests.delete(
            self.URL + API_LINK,
            auth=(self.username, self.password),
            headers=headers
        )

        if resp.status_code == 204:
            print('Successfully deleted repo {}' .format(self.repo_name))

        else:
            print('GITHUB Error: {}' .format(resp.status_code))
            print(json.loads(resp.content)['message'])
            sys.exit(1)

    def deploy(self):
        """Deploy current repo to GH"""

        self.create_repo()
        self.upload_repo()
        self.download_repo()
