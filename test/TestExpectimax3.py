import unittest

from Model.Agents.Actions import Actions
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.ExpectimaxPlayerAgent2 import ExpectimaxPlayerAgent2
from Model.Agents.ExpectimaxPlayerAgent3 import ExpectimaxPlayerAgent3
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


    def test_expectimaxV3_1_1(self):
        '''
        No enemies on board, should randomly move for like 5 turns
        Will NOT win and NOT Lose
        points should be 5 by the end
        :return:
        '''
        state = self.init_gameState
        #replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=5)

        for i in range(5):
            agent : ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            state.print_status()
            state.print_board()
            state.print_score()
            print("==========================\n")

        self.assertEquals(5,state.score)

    def test_expectimaxV3_1_2(self):
        '''
        No enemies on board, should randomly move for like 5 turns
        points should be 5 by the end
        Will win
        testing that getStateAtNextTurn works fine for winning cases
        :return:
        '''
        state = self.init_gameState
        state.turns_left = 5
        #replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=5)

        while state.isWin() == False and state.isLose() == False:
            agent : ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            state.print_status()
            state.print_board()
            state.print_score()
            print("==========================\n")

        self.assertEquals(10005, state.score)

    def test_expectimaxV3_2_1(self):
        '''
        1 Player
        1 SimpleGoLeftAgent
        Expectimax Depth = 2
        Player should not be taking any actions that would destroy
        SimpleGoLeft agent in general
        Player may randomly choose to fire though
        Play only for 2 turns
        Will not win or lose
        :return:
        '''
        state = self.init_gameState
        #replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=2)

        goLeftEnemy = SimpleGoLeftAgent(4,6)
        state.addAgent(goLeftEnemy)
        state.update_board()

        for i in range(2):
            agent : ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            state.print_status()
            state.print_board()
            state.print_score()
            print("==========================\n")

        self.assertEquals(2,state.score)

    def test_expectimaxV3_2_2(self):
        '''
        1 Player
        1 SimpleGoLeftAgent
        Expectimax Depth = 3
        Player SHOULD be taking any actions that would destroy
        SimpleGoLeft agent in general
        Player may randomly choose to fire though
        Play at max for 4 turns
        Player should want to fire at least for the first turn
        :return:
        '''
        state = self.init_gameState
        state.turns_left = 5
        #replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=3)

        print(state.getAllLegalActions(0))

        goLeftEnemy = SimpleGoLeftAgent(4,6)
        state.addAgent(goLeftEnemy)
        state.update_board()
        print("initial state")
        state.print_board()

        while state.isWin() == False and state.isLose() == False:
            agent : ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            state.print_status()
            state.print_projectile_locations()
            state.print_board()
            state.print_score()
            print("==========================\n")

        #should win so score should be 10015
        self.assertEquals(10015, state.score)

    def test_expectimaxV3_3(self):
        '''
        1 Player
        1 BasicFireAndMove
        Expectimax Depth = 3
        Player should be taking actions to destroy or avoid enemy and win
        Player may randomly choose to fire though
        Play at max for 4 turns
        Player should want to fire at least for the first turn
        :return:
        '''
        turns_survival = 7
        state = self.init_gameState
        state.turns_left = turns_survival
        # replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=3)

        basicFireAndMoveEnemy = EnemyAgentBasicFireAndMove(4,6)
        state.addAgent(basicFireAndMoveEnemy)
        state.update_board()
        print("initial state")
        state.print_board()

        for i in range(turns_survival):
            playerAction = state.current_agents[0].autoPickAction(state)
            state = state.getStateAfterAction(0,playerAction,True)
            try:
                state = state.getStateAfterAction(1, Actions.FIRE)
            except IndexError:
                x= 5
            except RuntimeError:
                x=5

            ########## update state ###########
            state.checkBulletAgentClashes()
            state.removeBullets()
            state.checkPlayerAgentClashes()
            state.updateAgentsList()
            state.update_board()
            state.reset_agents_move_status()
            state.decrement_turn()

            ###### Printing #########
            state.print_status()
            state.print_projectile_locations()
            state.print_board()
            state.print_score()

    def test_avoid_bullet_directly_in_front(self):
        '''
        1 Player
        1 Basic Fire and Move
        Fire and move fire a shot
        Player should move away
        :return:
        '''

        print_board = True
        turns_survival = 7
        state = self.init_gameState
        state.turns_left = turns_survival
        # replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=3)

        basicFireAndMoveEnemy = EnemyAgentBasicFireAndMove(4, 2)
        state.addAgent(basicFireAndMoveEnemy)
        state = state.getStateAfterAction(1,Actions.FIRE)
        state.update_board()
        print("initial board")
        state.print_board()

        while state.isWin() == False and state.isLose() == False:
            agent: ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            if print_board == True:
                state.print_status()
                state.print_projectile_locations()
                state.print_board()
                state.print_score()
                print("==========================\n")

        print("Final State")
        state.print_status()
        state.print_projectile_locations()
        state.print_board()
        state.print_score()

    def test_expectimaxV3_3_1(self):
        '''
        1 Player
        1 BasicFireAndMove
        Expectimax Depth = 3
        Player should be taking actions to destroy or avoid enemy and win
        Play at max for 4 turns
        Player should want to fire at least for the first turn
        :return:
        '''
        print_board = True
        turns_survival = 7
        state = self.init_gameState
        state.turns_left = turns_survival
        # replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=3)

        basicFireAndMoveEnemy = EnemyAgentBasicFireAndMove(4,6)
        state.addAgent(basicFireAndMoveEnemy)
        state.update_board()

        while state.isWin() == False and state.isLose() == False:
            agent: ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            if print_board == True:
                state.print_status()
                state.print_projectile_locations()
                state.print_board()
                state.print_score()
                print("==========================\n")

        print("Final State")
        state.print_status()
        state.print_projectile_locations()
        state.print_board()
        state.print_score()

        self.assertTrue(state.score > 10000)

    def test_expectimaxV3_4(self):
        '''
        1 Player
        1 TurnSpan agent
        Expectimax Depth = 3, To run faster
        Player should be taking actions to destroy or avoid enemy and win
        Player may randomly choose to fire though
        Play at max for 4 turns
        Player should want to fire at least for the first turn
        :return:
        '''
        print_board = True
        turns_survival = 7
        state = self.init_gameState
        state.turns_left = turns_survival
        # replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=2)

        turnSpanAgent = BasicCounterAgent(4,6,10,5,6)
        state.addAgent(turnSpanAgent)
        state.update_board()

        while state.isWin() == False and state.isLose() == False:
            agent: ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            if print_board == True:
                state.print_status()
                state.print_projectile_locations()
                state.print_board()
                state.print_score()
                print("==========================\n")

        print("Final State")
        state.print_status()
        state.print_projectile_locations()
        state.print_board()
        state.print_score()

        self.assertTrue(state.score > 10000)

    def test_expectimaxV3_5(self):
        '''
        1 Player
        1 Heuristic Agent
        Expectimax Depth = 3, To run faster
        Player should be taking actions to destroy or avoid enemy and win
        Player may randomly choose to fire though
        Play at max for 4 turns
        Player should want to fire at least for the first turn
        :return:
        '''
        print_board = True
        turns_survival = 7
        state = self.init_gameState
        state.turns_left = turns_survival
        # replace player agent with expectimax agent
        state.current_agents[0] = ExpectimaxPlayerAgent3(
            lowest_row=PLAYER_INITIAL_SPAWN_ROW_POSITION,
            least_col=PLAYER_INITIAL_SPAWN_COL_POSITION,
            expectimax_depth=2)

        HeuristicAgent = EnemyMoveFireHeuristicAgent(4,6)
        state.addAgent(HeuristicAgent)
        state.update_board()

        while state.isWin() == False and state.isLose() == False:
            agent: ExpectimaxPlayerAgent3 = state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(state)
            state = state.getStateAtNextTurn(expectimaxAgentAction)
            if print_board == True:
                state.print_status()
                state.print_projectile_locations()
                state.print_board()
                state.print_score()
                print("==========================\n")

        print("Final State")
        state.print_status()
        state.print_projectile_locations()
        state.print_board()
        state.print_score()

        self.assertTrue(state.score > 10000)


def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()

