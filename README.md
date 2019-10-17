# Warbler

A Twitter clone! Check it out [here]("https://ks-warbler.herokuapp.com/").

## Key Features

* User can create and edit their profile.
* User can follow other users and like their posts.

### Installation

```sh
# make a virtual environment
python3 -m venv venv

# use a virtual environment
source venv/bin/activate

# install python requirements
pip install -r requirements.txt

# set up database
dropdb warbler_db
createdb warbler_db
python -m flask db upgrade

# The database must be freshly created before doing this command
# If you have already added data, make sure to follow the steps above
# to reset the database.
python seed.py

# start the server!
python -m flask run
```
