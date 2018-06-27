from datetime import datetime
from random import uniform

profile_data = [{
    "kind": "lego",
    "count": 10
}, {
    "kind": "men",
    "count": 100
}, {
    "kind": "women",
    "count": 100
}]


def get_random_datetime(year_gap=2):
    now = datetime.now()
    then = now.replace(year=now.year - 2)
    random_time = uniform(then.timestamp(), now.timestamp())
    return datetime.fromtimestamp(random_time)
