# Warbler

A Twitter clone with a Rithm spin.

[Live site](https://warbler-app.herokuapp.com/)

### Installation

```sh
# make a virtual environment
mkvirtualenv warbler
# install python requirements
pip install -r requirements.txt

# set up database
dropdb warbler_db
createdb warbler_db
flask db upgrade

# The database must be freshly created before doing this command
# If you have already added data, make sure to follow the steps above
# to reset the database.
python seed.py

# start the server!
flask run
```
