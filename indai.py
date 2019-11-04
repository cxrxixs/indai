# indai.py

from api import githubapi
from api import herokuapi

import os
import sys
from getpass import getpass
from dotenv import load_dotenv


class Action():

    def __init___(self):
        pass

    def help(self):
        print('Helping action')

    def deploy(self):
        print('Deploy app')
        credential = read_credentials()
        gh = githubapi.Github(credential)
        gh.deploy()

        hk = herokuapi.Heroku(credential, gh.repo_hash())
        hk.deploy()

    def test(self):
        print('Testing function')
        read_credentials()

    def cleanup(self):
        """Destroy current test repo"""
        print('Cleaning up...')
        credential = read_credentials()
        # clear Github repo
        gh = githubapi.Github(credential)
        gh.destroy_repo()

        # clear Heroku app
        hk = herokuapi.Heroku(credential, 0)
        hk.destroy_app()


def read_credentials():
    """
    Read credentials of Heroku and Github
    for authenticating with their API's.
    """

    # Load if there is available envar
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path)

    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PW')
    heroku_user = os.environ.get('HEROKU_USER')
    heroku_pass = os.environ.get('HEROKU_PW')

    if github_user == '':
        # request user to input their credentials
        github_user = input('Github username: ')
        github_pass = getpass()
        heroku_user = input('Heroku username: ')
        heroku_pass = getpass()

    secret = {
        'github': {
            'username': github_user,
            'password': github_pass
            },
        'heroku': {
            'username': heroku_user,
            'password': heroku_pass
            }
        }

    return secret


def main():

    # Check if there is argument provided
    # Check what is the name of the folder where the app in invoked

    options_available = {
        'help': 'Show all available actions',
        ' ': 'Show available actions',
        'deploy': 'Deploy temporay app',
        'cleanup': 'Delete temporary app',
        'test': 'Test temporary app'
        }

    try:
        option = sys.argv[1]

    except IndexError:
        # when there is no argument provided
        print('Available actions are')
        for key, val in options_available.items():
            print('<{}> - {}' .format(key, val))
        print('\n')

        sys.exit(1)

    if option in options_available:
        act = Action()
        # print('Your option is {}' .format(option))
        getattr(act, option)()

    else:
        print('Unknown option: {}' .format(option))


if __name__ == '__main__':
    main()
