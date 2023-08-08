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


class Game:
    def __init__(self, team_a: list[Players], team_b: list[Players], format: Format) -> None:
        self.gamemode = Gamemode(format)
        self.max_balls = self.gamemode.overs*6


    def coinToss(self):
        return round(random.random())

    def sim(self):
        return math.ceil(random.random()*7) -1

    def start(self):
        # coin toss
        if self.coinToss():
            self.innings((team_a, team_b))
            self.innings((team_b, team_a))
        else:
            self.innings((team_b, team_a))
            self.innings((team_a, team_b))
        # team a 1st innings
        # team b 1nd innings

    def innings(self, teams: tuple[list[Players]]):
        balls_bowled: int = 0
        outs: int = 0
        runs: int = 0

        batting_team = teams[0]
        bowling_team = teams[1]

        batter1 = batting_team[0]
        batter2 = batting_team[1]
        bowler = bowling_team[-1]

        while self.max_balls > balls_bowled and outs < 10:
            balls_bowled += 1
            bowler.balls_bowled += 1
            result = self.sim()

            if result == 5:
                bowler.outs += 1
                outs += 1
                display = f'{batter1.name} bowled by {bowler.name}'
                if outs >= 10:
                    break
                batter1 = batting_team[outs+1]
            else:
                runs += result
                batter1.runs += result
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


team_a = [Players('A1'), Players('A2'), Players('A3'), Players('A4'), Players('A5'), Players('A6'), Players('A7'), Players('A8'), Players('A9'), Players('A10'), Players('A11')]
team_b = [Players('B1'), Players('B2'), Players('B3'), Players('B4'), Players('B5'), Players('B6'), Players('B7'), Players('B8'), Players('B9'), Players('B10'), Players('B11')]
new_game = Game(team_a, team_b, Format.T10)
new_game.start()
