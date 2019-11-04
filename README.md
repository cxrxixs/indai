# INDAI

What's in the name, **IN**termediate **D**eployment **A**ssistance **I**nterface.

**INDAI**, A helper tool in deploying app to Heroku for testing, this is accomplished by pushing the current repo to Github(temporarily) without commiting to your official repo then building Heroku app using the temporary source.

## Prerequisites
Requires Heroku account.

## TODO
- [ ] Main CLI
- [ ] Functions
    - [X] Deploy : Push current repo to Github and build Heroku app

    - [X] Cleanup : Delete Github repo and Heroku app

    - [ ] Reupload : If repo/app already exist skip creation and proceed to upload/build

    - [ ] Test : Run test on temporary app
