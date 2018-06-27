from app import db
from models import User, Message
import csv

db.drop_all()
db.create_all()

with open('generator/users.csv') as users_csv:
    users_reader = csv.DictReader(users_csv)
    users = [User(**row) for row in users_reader]
    db.session.add_all(users)
    db.session.commit()

with open('generator/messages.csv') as messages_csv:
    messages_reader = csv.DictReader(messages_csv)
    messages = [Message(**row) for row in messages_reader]

with open('generator/follows.csv') as follows_csv:
    follows_reader = csv.DictReader(follows_csv)
    for follow in follows_reader:
        followee = User.query.get(follow['followee_id'])
        follower = User.query.get(follow['follower_id'])
        followee.followers.append(follower)

db.session.add_all(messages)
db.session.commit()