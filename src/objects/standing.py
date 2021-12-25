from src.objects.euroleague_team import EuroleagueTeam

class Standing:
    def __init__(self, team: EuroleagueTeam, wins: int, losses: int):
        self.team = team        
        self.wins = wins
        self.losses = losses
    
    @property
    def total_games_played(self):
        return self.wins + self.losses

    @property
    def winning_percentage(self):
        return self.wins / self.total_games_played * 100

    def __repr__(self) -> str:
        return f"{self.team.name}: {self.wins}-{self.losses}"