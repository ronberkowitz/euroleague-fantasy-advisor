import requests

def get_current_round_number() -> int:
    return requests.get(
        "https://api.dunkest.com/api/rounds/current?league_id=3&fanta_league_id=3").json()['number']