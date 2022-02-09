import os
import pandas as pd
from src.scrapers import get_standings, get_round_matchups
from src.analysis.coach_analyzer import CoachAnalyzer
from src import utils


ROUND_NUMBER = utils.get_current_round_number()
BASE_OUTPUTS_FOLDER = rf'{os.getcwd()}/outputs/round{ROUND_NUMBER}'


# create the outputs folder for the upcoming round
os.mkdir(BASE_OUTPUTS_FOLDER) if not os.path.exists(BASE_OUTPUTS_FOLDER) else None

# TODO: path should be changed everytime - automate this.
# round_stats = pd.read_excel(input('enter path to round stats excel:\n'))
round_stats = utils.get_fantasy_stats_df()
round_stats = round_stats.set_index("Team Abbreviation")

standings = get_standings()
matchups = get_round_matchups()


coach_analyzer = CoachAnalyzer(standings, round_stats['Quotation'].to_dict())
coach_analysis_df = coach_analyzer.generate_coach_analysis_df(matchups)
coach_analysis_df.to_excel(os.path.join(BASE_OUTPUTS_FOLDER, 'coach_analysis.xlsx'))
coach_analyzer.generate_coach_analysis_plot(coach_analysis_df, os.path.join(BASE_OUTPUTS_FOLDER, 'coach_analysis.jpg'))
