import unittest

from Actions import Actions
from newVersion.NewGameState import NewGameState
from AgentAbstractClass import PlayerAgent, AgentAbstractClass


class TestGameState(unittest.TestCase):
    def setUp(self) -> None:
        self.gamestateInit = NewGameState()
        self.gameState_2 = NewGameState()

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
            enemy_agent = AgentAbstractClass(lowest_row=each[0], least_col=each[1])
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
        board_min_col_boundary = self.gamestateInit.gameBoard.min_col
        board_max_col_boundary = self.gamestateInit.gameBoard.board_max_x_boundary
        board_min_row_boundary = self.gamestateInit.gameBoard.min_row
        board_max_row_boundary = self.gamestateInit.gameBoard.board_max_y_boundary

        valid_p1 = PlayerAgent()
        self.gamestateInit.addAgent(valid_p1)
        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 0,0 player can move up, right, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.UP, Actions.RIGHT, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        gameState2 = NewGameState()
        valid_p2 = PlayerAgent()



def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()