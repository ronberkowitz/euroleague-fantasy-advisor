from numpy import mat
import pandas as pd
from typing import List
from src.objects.matchup import Matchup
from src.objects.standing import Standing
import matplotlib.pyplot as plt


class CoachAnalyzer:
    def __init__(self, standings: List[Standing], coach_price_by_team: dict) -> None:
        """
        params:
        * standings - a list of Standing objects.
        * coach_price_by_team - a dictionary where the keys are the euroleague team enum names, and the value is the head coach's price.
        """
        self.standings = standings
        self.coach_price_by_team = coach_price_by_team

    def recommend_coach_by_matchup(self, matchup: Matchup):
        """
        gets a matchup and returns a dict containing keys "team", "price" for the recommended coach's team and his price.
        """
        percentage_difference = matchup.calculate_percentage_difference(self.standings)

        home_coach =  {"team": matchup.home_team.name, "price":  self.coach_price_by_team[matchup.home_team.name]}
        away_coach =  {"team": matchup.away_team.name, "price":  self.coach_price_by_team[matchup.away_team.name]}

        # if the percentage is positive, the home team is better
        if percentage_difference > 0:
            return home_coach

        # if the percentage is negative, the away team is better
        elif percentage_difference < 0:
            return away_coach

        # if the percentages are the same - return the cheaper coach
        else:
            return home_coach if home_coach['price'] < away_coach['price'] else away_coach


    def generate_coach_analysis_df(self, matchups: List[Matchup]) -> pd.DataFrame:
        """
        Analysis the received data and generates a DataFrame that helps deciding the most valuable coach.
        params:
        * matchups - a list of Matchup objects. The upcoming round's matchups.

        return value:
        a DataFrame with a row for each matchup, with keys "team", "price", "strength". -- "team" is the abbrevation of the recommended coach's team,
        price is the head coach's price and strength is the difference between the teams' winning percentages.
        """
        matchups_analysis_data = []

        for matchup in matchups:
            percentage_difference = matchup.calculate_percentage_difference(self.standings)
            recommended_coach = self.recommend_coach_by_matchup(matchup)

            matchups_analysis_data.append({
                "team": recommended_coach['team'],#.name?
                "price": recommended_coach['price'],
                "strength": abs(percentage_difference)
            })

        return pd.DataFrame.from_records(matchups_analysis_data, index="team").sort_values(by="strength", ascending=False)

    def generate_coach_analysis_plot(self, coach_analysis_df: pd.DataFrame, output_path: str):
        fig, ax = plt.subplots()
        ax.scatter(x=coach_analysis_df['price'], y=coach_analysis_df['strength'])

        for index, row in coach_analysis_df.iterrows():
            ax.annotate(index, (row['price'], row['strength']))
            
        ax.plot([0, 1], [0, 1], transform=ax.transAxes, color='red', alpha=0.1)
        plt.ylim([0, 100])

        plt.xlabel("Recommended Coach Price")
        plt.ylabel("Recommendation Strength")
        plt.grid()
        plt.savefig(output_path)