import unittest

from Model.Agents.Actions import Actions
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameState import GameState



class TestProjectiles(unittest.TestCase):

    def setUp(self) -> None:
        self.gamestate = GameState()

    def testPlayerProjectile1(self):
        #player, shoots prohectiles no enemies

        gamestate = self.gamestate
        player_agent = PlayerAgent(1,1,5,5)
        enemy_1 = SimpleGoLeftAgent(5,9)
        addedSuccessfully = gamestate.addAgent(player_agent)
        gamestate.addAgent(enemy_1)

        if addedSuccessfully == False:
            raise ValueError

        gamestate.update_board()

        newState = gamestate.generateSuccessorState(0,Actions.FIRE)
        newState = newState.generateSuccessorState(1, Actions.LEFT)
        newState.update_board()

        print(newState.gameBoard)

        self.assertEqual(1,1)


