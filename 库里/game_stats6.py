import json
from pathlib import Path


class GameStats:
    #跟踪游戏信息
    def __init__(self,ai_game):
        #初始化游戏信息
        self.settings = ai_game.settings
        self.reset_stats()
        #任何情况下都不应该重置最高得分
        self.high_score = self.get_saved_high_score()

    def get_saved_high_score(self):
        """Gets high score from file, if it exists."""
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0

    def reset_stats(self):
        #初始化游戏运行期间可能变更的信息
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1