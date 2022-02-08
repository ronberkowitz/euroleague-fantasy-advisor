from typing import List
import requests
from src.objects.euroleague_team import EuroleagueTeam
import pandas as pd
from src.objects.matchup import Matchup
import src.utils as utils
from src.objects.standing import Standing


def get_standings() -> List[Standing]:
    """
    fetches the current euroleague standings, cleans the data and returns a list of Standing objects.
    """
    standings_url = 'https://www.eurosport.com/basketball/euroleague/standing.shtml'

    resp = requests.get(standings_url)
    df = pd.read_html(resp.text, index_col=0)[0]
    df.columns = ["team", "last5", "played", "wins", "losses", "pts"]

    return [Standing(EuroleagueTeam(row['team'].lower()), row['wins'], row['losses'])
            for index, row in df.iterrows()]


def get_round_matchups() -> List[Matchup]:
    """
    first fetches the current round number, and then fetches the upcoming round's matchups.
    returns a list of Matchup objects.
    """
    # this round = real round number + 80
    round_number = utils.get_current_round_number()
    resp = requests.get(
        f"https://api.dunkest.com/api/rounds/{80 + round_number}/games/v2")

    return [Matchup(EuroleagueTeam[game["home_team_abbreviation"]],
                    EuroleagueTeam[game["away_team_abbreviation"]]) for game in resp.json()['games']]
