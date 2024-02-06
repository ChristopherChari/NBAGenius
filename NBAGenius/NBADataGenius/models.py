from django.db import models

# Create your models here.

from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    conference = models.CharField(max_length=50)
    division = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    jersey_number = models.PositiveIntegerField()
    position = models.CharField(max_length=5)
    height = models.CharField(max_length=10)
    weight = models.PositiveIntegerField()
    wingspan = models.CharField(max_length=10)  
    birthdate = models.DateField()
    college_team = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    date = models.DateField()
    home_team_score = models.PositiveIntegerField()
    away_team_score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.date}"

class PlayerStatistic(models.Model):
    player = models.ForeignKey(Player, related_name='statistics', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='player_statistics', on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    rebounds = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    # Add more fields as needed (e.g., steals, blocks, turnovers)

    class Meta:
        unique_together = ['player', 'game']

class TeamStatistic(models.Model):
    team = models.ForeignKey(Team, related_name='statistics', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='team_statistics', on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    rebounds = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    # Add more fields as needed (e.g., steals, blocks, turnovers)

    class Meta:
        unique_together = ['team', 'game']
