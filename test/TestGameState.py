import unittest

from Actions import Actions
from AgentInterface import AgentInterface
from newVersion.GameState import GameState
from AgentSuperClass import PlayerAgent, AgentSuperClass, SimpleGoLeftAgent

UP = Actions.UP
DOWN = Actions.DOWN
LEFT = Actions.LEFT
RIGHT = Actions.RIGHT
STOP = Actions.STOP
FIRE = Actions.FIRE

class TestGameState(unittest.TestCase):
    def setUp(self) -> None:
        self.gamestateInit = GameState()
        self.gameState_2 = GameState()

    # test default values
    def test_default_values(self) -> None:
        g = self.gamestateInit
        self.assertEquals(0,len(g.current_agents))
        self.assertFalse(g.isPlayerAdded)
        self.assertEquals(100, g.turns_left)
        self.assertEquals(1, g.max_enemies_at_any_given_time)

    #testing trying to add player agent in valid position
    def test_is_valid_agent_player(self):
        temp_p = PlayerAgent(1,1,4,5)
        isValid = self.gamestateInit.isValidAgent(temp_p)
        self.assertTrue(isValid)

    def test_is_valid_enemy_agents(self):
        board_min_col_boundary = self.gamestateInit.gameBoard.min_col
        board_max_x_boundary = self.gamestateInit.gameBoard.board_max_x_boundary
        board_min_row_boundary = self.gamestateInit.gameBoard.min_row
        board_max_y_boundary = self.gamestateInit.gameBoard.board_max_y_boundary

        invalidCount = 0
        agentsList = []

        invalid_tuples = [
            # go one row lower than minimum board min
            (board_min_row_boundary - 1, board_min_col_boundary),
            # go one col lower than board min, enemy is allowed to do this
            # enemy agents allowed to go beyond board_min_bounds
            (board_min_row_boundary, board_min_col_boundary - 1),
            # go one higher than max row of board
            (board_max_y_boundary + 1, board_max_x_boundary),
            # go one higher than max col of board, enemy is allowed to do this
            # enemy agents allowed to come in from col > board_col_max bounds
            (board_max_y_boundary, board_max_x_boundary + 1)]

        for each in invalid_tuples:
            enemy_agent = AgentSuperClass(lowest_row=each[0], least_col=each[1])
            agentsList.append(enemy_agent)

        for eachAgent in agentsList:
            isValid = self.gamestateInit.isValidAgent(eachAgent)
            if isValid == False:
                invalidCount += 1

        self.assertEqual(2, invalidCount)

    #testing trying to add player agent who is out of bounds
    def test_not_valid_agent_player(self):
        board_min_col_boundary = self.gamestateInit.gameBoard.min_col
        board_max_x_boundary = self.gamestateInit.gameBoard.board_max_x_boundary
        board_min_row_boundary = self.gamestateInit.gameBoard.min_row
        board_max_y_boundary = self.gamestateInit.gameBoard.board_max_y_boundary

        invalidCount = 0
        agentsList = []

        invalid_tuples = [
            # go one row lower than minimum board min
            (board_min_row_boundary-1, board_min_col_boundary),
            #go one col lower than board min
            (board_min_row_boundary,board_min_col_boundary - 1),
            #go one higher than max row of board
            (board_max_y_boundary + 1, board_max_x_boundary),
            # go one higher than max col of board
            (board_max_y_boundary, board_max_x_boundary + 1)]

        for each in invalid_tuples:
            temp_p = PlayerAgent(lowest_row=each[0],least_col=each[1])
            agentsList.append(temp_p)

        for eachAgent in agentsList:
            isValid = self.gamestateInit.isValidAgent(eachAgent)
            if isValid == False:
                invalidCount += 1

        self.assertEqual(4,invalidCount)


    def test_add_valid_player(self) -> None:
        p1 = PlayerAgent()
        self.gameState_2.addAgent(p1)
        self.assertTrue(self.gameState_2.isPlayerAdded)
        self.assertEquals(1, len(self.gameState_2.current_agents))

    # should not be able to add a second player agent
    def test_adding_2_players(self):
        p1 = PlayerAgent()
        self.gameState_2.addAgent(p1)
        player_2 = PlayerAgent()
        self.assertFalse(self.gameState_2.addAgent(player_2))
        self.assertEquals(1,len(self.gameState_2.current_agents) )

    def testGetAllLegalActionsPlayer(self):
        valid_p1 = PlayerAgent()
        self.gamestateInit.addAgent(valid_p1)
        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 0,0 (bottom left corner) player can move up, right, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.UP, Actions.RIGHT, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        gameState3 = GameState()
        # from (9,9) top right corner player can move left, down, stop , or fire
        valid_p2 = PlayerAgent(1,1,9,9)
        gameState3.addAgent(valid_p2)
        p2_legal_actions = gameState3.getAllLegalActions(0)
        gameState3.getAllLegalActions(0)
        self.assertEquals(4,len(p2_legal_actions))
        self.assertEquals([Actions.LEFT, Actions.DOWN, Actions.STOP,Actions.FIRE],
                          p2_legal_actions)

        #TODO test player and enemy getLegalActions together

    def testCheckPlayerAgentClashes_no_clash_simple(self):
        # set to true to print board to terminal/console for visual aid
        print_board = False

        player = PlayerAgent(1,1,3,3)
        enemy_1 = SimpleGoLeftAgent(3,4)
        state = self.gamestateInit

        state.addAgent(player)
        state.addAgent(enemy_1)

        #no clashes agents should be right next to each other
        state.checkPlayerAgentClashes()
        state.update_board()

        self.assertEquals(1,state.gameBoard.board_array[3][3])
        self.assertEquals(2, state.gameBoard.board_array[3][4])
        self.assertEquals(2,len(state.current_agents))

        if print_board:
            print(state.gameBoard)
            print("/****** END OF testCheckPlayerAgentClashes_no_clash_simple *****/\n")

        #TODO test agent clash but if enemy moved beyond min col boundary, should be allowed and should remove from agent list

    def test_check_clash_player_vs_simple(self):
        #This also tests updateAgentsList
        # set to true to print board to terminal/console for visual aid
        print_board = False

        #player and agent on same space, should both lose 1 hp and die
        player = PlayerAgent(1, 1, 4, 4)
        enemy_1 = SimpleGoLeftAgent(4, 4)

        state = self.gamestateInit

        state.addAgent(player)
        state.addAgent(enemy_1)

        # agents should clash and both die
        state.checkPlayerAgentClashes()
        state.updateAgentsList()
        state.update_board()

        # agents should have been removed since both lost 1 hp and died
        self.assertEqual(0, len(state.current_agents))
        self.assertEqual(0, state.gameBoard.board_array[4][4])

        if print_board:
            print("KEY:\n0 = Empty Space\n1 = Player\n> 1 = Enemy Agent")
            print(state.gameBoard)
            print("/***** END OF test_check_clash_player_vs_simple *****/\n")

    def test_agent_clash_with_enemy_index_2(self):
        # This also tests updateAgentsList
        # set to true to print board to terminal/console for visual aid
        print_board = False

        # player and agent on same space, should both lose 1 hp and die
        player = PlayerAgent(1, 1, 4, 4)
        enemy_1 = SimpleGoLeftAgent(5,6)
        enemy_2 = SimpleGoLeftAgent(4,4)

        # need to allow more than 1 enemy at a time
        state = GameState(max_enemies_at_one_time=2)

        state.addAgent(player)
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        # player and enemy 2 clash and both die
        state.checkPlayerAgentClashes()
        state.updateAgentsList()
        state.update_board()

        #enemy 1 still exists though
        self.assertEqual(1, len(state.current_agents))
        self.assertEqual(0, state.gameBoard.board_array[4][4])

        if print_board:
            print("KEY:\n0 = Empty Space\n1 = Player\n> 1 = Enemy Agent")
            print(state.gameBoard)
            print("/***** END OF test_check_clash_player_vs_simple *****/\n")

    def test_generate_successor_state_player_moves_valid(self):
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        player = PlayerAgent(1, 1, 4, 4)
        state.addAgent(player)

        newState = state.generateSuccessorState(0,LEFT)
        #check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[4][4])
        #check new position NOT empty
        self.assertEquals(1,newState.gameBoard.board_array[4][3])
        #turn should also decrement by
        self.assertEquals(99, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 4, y = 4")
            print("Player moves left (col - 1), so new position:\n\tx = 3, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = newState.generateSuccessorState(0,UP)
        #check old position is empty
        self.assertEquals(0, newState.gameBoard.board_array[4][3])
        #check new position NOT empty on board
        self.assertEquals(1,newState.gameBoard.board_array[5][3])
        # turn should also decrement by
        self.assertEquals(98, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 4")
            print("Player moves up (row + 1), so new position:\n\tx = 3, y = 5")
            print(newState.gameBoard)
            print("-" * 40 + "\n")


        newState = newState.generateSuccessorState(0, DOWN)
        # check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[5][3])
        # check new position NOT empty on board
        self.assertEquals(1, newState.gameBoard.board_array[4][3])
        # turn should also decrement by
        self.assertEquals(97, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 5")
            print("Player moves down (row - 1), so new position:\n\tx = 3, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = newState.generateSuccessorState(0,RIGHT)
        # check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[4][3])
        # check new position NOT empty on board
        self.assertEquals(1, newState.gameBoard.board_array[4][4])
        # turn should also decrement by
        self.assertEquals(96, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 4")
            print("Player moves down (row - 1), so new position:\n\tx = 4, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        #TODO repeat test but with larger player length and height


    def test_generate_successor_state_player_invalid_moves(self):
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        #agent in bottom corner, should not be able to move down or left
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        newState = state.generateSuccessorState(0,LEFT)
        #check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[0][0])
        #check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[1][0])
        self.assertEquals(0, newState.gameBoard.board_array[0][1])
        #check turn decrement
        self.assertEquals(99,newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 0, y = 0")
            print("Player can NOT move left (i.e cannot col - 1), so new position:\n\tx = 0, y = 0")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = state.generateSuccessorState(0, DOWN)
        # check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[0][0])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[1][0])
        self.assertEquals(0, newState.gameBoard.board_array[0][1])
        # check turn decrement
        self.assertEquals(98, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 0, y = 0")
            print("Player can NOT move down (i.e cannot row - 1), so new position:\n\tx = 0, y = 0")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        #manually move player to top right corner to perform tests there
        player_agent: AgentInterface = newState.current_agents[0]
        player_agent.set_position(9,9)

        newState = state.generateSuccessorState(0, UP)
        # check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[9][9])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[8][9])
        self.assertEquals(0, newState.gameBoard.board_array[9][8])
        # check turn decrement
        self.assertEquals(97, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 9, y = 9")
            print("Player can NOT move down (i.e cannot row + 1), so new position:\n\tx = 9, y = 9")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = state.generateSuccessorState(0, RIGHT)
        # check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[9][9])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[8][9])
        self.assertEquals(0, newState.gameBoard.board_array[9][8])
        # check turn decrement
        self.assertEquals(96, newState.turns_left)

        if (print_board):
            print("Player initial position:\n\tx= 9, y = 9")
            print("Player can NOT move down (i.e cannot col + 1), so new position:\n\tx = 9, y = 9")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        #TODO maybe make test with diff board_height and lenght too?

def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()