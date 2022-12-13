import unittest

from Model.Agents.Actions import Actions
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
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
        while one is moving.
        :return:
        """

        printBoard = True

        state = self.init_gameState
        goLeftAgent = SimpleGoLeftAgent(0,BOARD_COLUMNS -1)
        basicFireMoveAgent = EnemyAgentBasicFireAndMove(1,BOARD_COLUMNS - 2)
        heuristicEnemyAgent = EnemyMoveFireHeuristicAgent(2,4)
        turnSpanAgent = BasicCounterAgent(3,3,10,6,7)

        state.addAgent(goLeftAgent)
        state.addAgent(basicFireMoveAgent)
        state.addAgent(heuristicEnemyAgent)
        state.addAgent(turnSpanAgent)

        state = state.getStateAfterAction(0, Actions.RIGHT)
        state = state.getStateAfterAction(0, Actions.RIGHT)
        state = state.getStateAfterAction(0, Actions.UP)

        self.assertEquals((PLAYER_INITIAL_SPAWN_ROW_POSITION + 1, PLAYER_INITIAL_SPAWN_COL_POSITION + 2), state.current_agents[0].get_position())
        self.assertEquals((0,BOARD_COLUMNS -1), goLeftAgent.get_position())


        state = state.getStateAfterAction(0, Actions.LEFT)
        state = state.getStateAfterAction(0,Actions.LEFT)
        state = state.getStateAfterAction(0, Actions.FIRE)

        state = state.getStateAfterAction(0, Actions.UP)
        state = state.getStateAfterAction(0,Actions.UP)

        self.assertEquals(1, len(state.current_projectiles))
        self.assertEquals((5,1), state.current_projectiles[0].get_position())

        state = state.getStateAfterAction(0, Actions.STOP,True)
        self.assertEquals((5,2), state.current_projectiles[0].get_position())
        state.print_board()


def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()

