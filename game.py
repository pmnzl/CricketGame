import math
import random
from enum import Enum

class Format(Enum):
    T10 = 10
    T20 = 20
    ODI = 50
    TEST = -1


class Gamemode:
    def __init__(self, format:Format) -> None:
        match format:
            case Format.T10:
                self.overs: int = 10
                self.max_bowler_overs: int = 2
                self.innings: int = 1
            case Format.T20:
                self.overs: int = 20
                self.max_bowler_overs: int = 4
                self.innings: int = 1
            case Format.ODI:
                self.overs: int = 50
                self.max_bowler_overs: int = 10
                self.innings: int = 1
            case Format.TEST:
                self.overs: int = 90*5
                self.max_bowler_overs: int = -1
                self.innings: int = 2


class Players:
    def __init__(self, name: str) -> None:
        # unique identifier
        self.name: str = name
        # skills (get from database based on name)
        self.batting: int = 0
        self.bowling: int = 0
        self.fielding: int = 0
        # in game batting score
        self.runs: int = 0
        self.balls_faced: int = 0
        # in game bowling score
        self.outs: int = 0
        self.balls_bowled: int = 0
        self.runs_against: int = 0


class Game:
    def __init__(self, team_a: list[Players], team_b: list[Players], team_a_name: str, team_b_name: str, format: Format) -> None:
        self.gamemode = Gamemode(format)
        self.max_balls = self.gamemode.overs*6
        self.innings_played = 0
        self.team_a = team_a
        self.team_b = team_b
        self.team_a_name = team_a_name
        self.team_b_name = team_b_name

    def coinToss(self):
        return round(random.random())

    def sim(self):
        return math.ceil(random.random()*7) -1

    def start(self):
        # coin toss
        if self.coinToss():
            first = (self.team_a, self.team_b)
            second = (self.team_b, self.team_a)
            team_names = (self.team_a_name, self.team_b_name)
        else:
            first = (self.team_b, self.team_a)
            second = (self.team_a, self.team_b)
            team_names = (self.team_b_name, self.team_a_name)
        second_score = (math.inf, 0)
        while self.innings_played + 1 < self.gamemode.innings:
            first_score = self.innings(first, second_score)
            second_score = self.innings(second, first_score)
            self.innings_played += 1
        first_score = self.innings(first, second_score)
        second_score = self.innings(second, first_score)
        self.scoreboard(first[0], team_names[0], first_score)
        self.scoreboard(first[1], team_names[1], second_score)
        self.matchSummary(first_score[0]-second_score[0], second_score[1], team_names)
        

    def innings(self, teams: tuple[list[Players]], score: tuple[int, int]):
        balls_bowled: int = 0
        outs: int = 0
        runs: int = 0

        batting_team = teams[0]
        bowling_team = teams[1]

        batter1 = batting_team[0]
        batter2 = batting_team[1]
        bowler = bowling_team[-1]

        while self.max_balls > balls_bowled and outs < 10 and runs <= score[0]:
            balls_bowled += 1
            bowler.balls_bowled += 1
            batter1.balls_faced += 1
            result = self.sim()

            if result == 5:
                bowler.outs += 1
                outs += 1
                display = f'{batter1.name} bowled by {bowler.name}'
                print(f'[{math.floor((balls_bowled-1)/6)}.{(balls_bowled-1) % 6}] {display}')
                if outs >= 10:
                    break
                batter1 = batting_team[outs+1]
            else:
                runs += result
                batter1.runs += result
                bowler.runs_against += result
                display = f'{batter1.name} hit {bowler.name} for {result} runs'
                if result % 2 == 1:
                    # switch batters
                    temp = batter1
                    batter1 = batter2
                    batter2 = temp
            print(f'[{math.floor((balls_bowled-1)/6)}.{(balls_bowled-1) % 6}] {display}')
            if balls_bowled % 6 == 0:
                bowler = bowling_team[-1 - math.floor(balls_bowled/6)]
                print(f"OVER {round(balls_bowled/6)}, {runs}/{outs}")
        print(f'Final score {runs}/{outs}')
        return (runs, outs)
    
    def scoreboard(self, team: list[Players], team_name: str, score: tuple[int, int]):
        print(f'{team_name.upper()} ({score[0]}/{score[1]})')
        print(f'        Batting        |       Bowling')
        print(f'  Player  Runs  Balls  |  Balls  Runs  Outs')
        for player in team:
            print(f'  {"{:<6}".format(player.name[:6])}  {"{:<4}".format(str(player.runs)[:4])}  {"{:<4}".format(str(player.balls_faced)[:4])}   |  {"{:<4}".format(str(player.balls_bowled)[:4])}   {"{:<4}".format(str(player.runs_against)[:4])}  {"{:<4}".format(str(player.outs)[:4])}')

    def matchSummary(self, run_difference: int, wickets: int, team: tuple[str, str]):
        if run_difference == 0:
            print(f'draw game!')
        elif run_difference > 0:
            print(f'{team[0].upper()} won by {run_difference} runs!')
        else:
            print(f'{team[1].upper()} won by {10 - wickets} wicket(s)!')




team_a = [Players('A1'), Players('A2'), Players('A3'), Players('A4'), Players('A5'), Players('A6'), Players('A7'), Players('A8'), Players('A9'), Players('A10'), Players('A11')]
team_b = [Players('B1'), Players('B2'), Players('B3'), Players('B4'), Players('B5'), Players('B6'), Players('B7'), Players('B8'), Players('B9'), Players('B10'), Players('B11')]
new_game = Game(team_a, team_b, "team a", "team b", Format.T10)
new_game.start()
