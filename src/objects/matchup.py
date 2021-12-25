from src.objects.euroleague_team import EuroleagueTeam
from pandas import DataFrame
from typing import List
from src.objects.standing import Standing

class Matchup:
    def __init__(self, home_team: EuroleagueTeam, away_team: EuroleagueTeam) -> None:
        self.home_team = home_team
        self.away_team = away_team

    def calculate_percentage_difference(self, standings: List[Standing]) -> float:
        """
        Gets a standings Dataframe and calculates and returns the difference between the winning percentages of the home team and the away team.
        if the percentage is positive, the home team is better. if negative, the away team is better.
        If the percentage is zero they are the same.
        """
        home_team_standing = [standing for standing in standings if standing.team == self.home_team][0]
        away_team_standing = [standing for standing in standings if standing.team == self.away_team][0]

        return home_team_standing.winning_percentage - away_team_standing.winning_percentage

    def recommend_coach(self, percentage_difference: float,  coach_price_by_name: dict) -> dict:
        """
        gets a dictionary of coach prices by team name (abbrevation) and returns a dict containing keys "team", "price"
        """

        home_coach =  {"team": self.home_team.name, "price": coach_price_by_name[self.home_team.name]}
        away_coach =  {"team": self.away_team.name, "price": coach_price_by_name[self.away_team.name]}

        # if the percentage is positive, the home team is better
        if percentage_difference > 0:
            return home_coach

        # if the percentage is negative, the away team is better
        elif percentage_difference < 0:
            return away_coach

        # if the percentages are the same - return the cheaper coach
        else:
            return home_coach if home_coach['price'] < away_coach['price'] else away_coach

    def __repr__(self) -> str:
        return f"{self.home_team.name} <-> {self.away_team.name}"