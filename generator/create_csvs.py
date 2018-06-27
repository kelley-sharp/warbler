import csv
from random import choice, randint, sample
from itertools import permutations
from requests import get
from faker import Faker
from helpers import get_random_datetime, profile_data

num_users = 300
num_messages = 1000
num_followers = 5000

fake = Faker()

profile_urls = [
    f"https://randomuser.me/api/portraits/{d['kind']}/{i}.jpg"
    for d in profile_data for i in range(d['count'])
]

header_image_urls = [
    get(f"http://www.splashbase.co/api/v1/images/{i}").json()['url']
    for i in range(1, 46)
]

with open('generator/users.csv', 'w') as users_csv:
    headers = [
        'email', 'username', 'image_url', 'password', 'bio',
        'header_image_url', 'location'
    ]
    data_writer = csv.DictWriter(users_csv, fieldnames=headers)
    data_writer.writeheader()
    for i in range(num_users):
        data_writer.writerow({
            'email':
            fake.email(),
            'username':
            fake.user_name(),
            'image_url':
            choice(profile_urls),
            'password':
            '$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe',
            'bio':
            fake.sentence(),
            'header_image_url':
            choice(header_image_urls),
            'location':
            fake.city()
        })

with open('generator/messages.csv', 'w') as messages_csv:
    headers = ['text', 'timestamp', 'user_id']
    data_writer = csv.DictWriter(messages_csv, fieldnames=headers)
    data_writer.writeheader()
    for i in range(num_messages):
        data_writer.writerow({
            'text': fake.paragraph()[:140],
            'timestamp': get_random_datetime(),
            'user_id': randint(1, num_users)
        })

with open('generator/follows.csv', 'w') as follows_csv:
    all_pairs = list(permutations(range(1, num_users + 1), 2))
    headers = ['followee_id', 'follower_id']
    data_writer = csv.DictWriter(follows_csv, fieldnames=headers)
    data_writer.writeheader()
    for pair in sample(all_pairs, num_followers):
        data_writer.writerow({'followee_id': pair[0], 'follower_id': pair[1]})
