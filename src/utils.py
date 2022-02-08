import requests
import pandas as pd


def get_current_round_number() -> int:
    return requests.get(
        "https://api.dunkest.com/api/rounds/current?league_id=3&fanta_league_id=3").json()['number']


def get_fantasy_stats_df() -> pd.DataFrame:
    headers = {
        'authority': 'api.dunkest.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'accept-language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://euroleaguefantasy.euroleaguebasketball.net',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://euroleaguefantasy.euroleaguebasketball.net/',
    }

    data = '{"league_id":3}'

    response = requests.post('https://api.dunkest.com/api/stats', headers=headers, data=data)
    return pd.read_excel(response.content)
