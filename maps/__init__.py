from pathlib import Path


CAMPAIGN_COUNT = 3


def get_user_amount():
    path = Path('maps/user/')
    return sum(1 for _ in list(path.iterdir()))


print(get_user_amount())
