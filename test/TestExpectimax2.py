import unittest

from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameState import GameState

BOARD_ROWS = 8
BOARD_COLUMNS = 7
MAX_ENEMIES_AT_ANY_TIME = 5
PLAYER_INITIAL_SPAWN_ROW_POSITION = BOARD_ROWS // 2  # spawn in middle of board rows
PLAYER_INITIAL_SPAWN_COL_POSITION = 0  # spawn player at furthest left position
PLAYER_LIVES = 1
PLAYER_HP = 3
MAX_ENEMIES_AT_ANY_TIME = 5



class TestExpectimax2(unittest.TestCase):

    def setUp(self) -> None:
        self.init_gameState = GameState(board_len= BOARD_COLUMNS, board_height= BOARD_ROWS,
                 max_enemies_at_one_time =MAX_ENEMIES_AT_ANY_TIME,
                 turns_left= 300, player_lives = PLAYER_LIVES)
        self.player_agent = PlayerAgent(1,1,PLAYER_INITIAL_SPAWN_ROW_POSITION, PLAYER_INITIAL_SPAWN_COL_POSITION)
        self.player_agent.set_hp(3)
        self.init_gameState.addAgent(self.player_agent)

    def test_getStateAfterAction1(self):
        """
        1 player agent, moves right, up, down, left
        1 SimpleGoLeftAgent
        1 BasicFireAndMove
        1 EnemyMoveFire
        1 BasicCounter

        Each will make a series of moves. No one else should move
        while one is moving
        :return:
        """

        state = self.init_gameState
        goLeftAgent = SimpleGoLeftAgent()

