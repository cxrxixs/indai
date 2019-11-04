# INDAI

What's in the name, **IN**termediate **D**eployment **A**ssistance **I**nterface.

**INDAI**, A helper tool in deploying app to Heroku for testing by pushing the current repo to Github(temporarily) without commiting to your official repo then build Heroku app using temporary source.

## Prerequisites
Requires Heroku account.

## TODO
- [ ] Main CLI
- [ ] Functions
    - [ ] Deploy
      Deploy current repo to Github and build Heroku app
    - [ ] Test
      Run test to temporary app deployed in Heroku
    - [ ] Cleanup
      Destroy Heroku (temporary)app and Github (temporary)repo
