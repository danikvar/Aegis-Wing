#encoding: utf-8
import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.GameState import GameState
import sys

class TestGameStateGameExamples(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()

    def test_game_example_1(self):
        """
        For this test
            - 1 simple and 1 heuristic enemy
            - simple enemy does not hit player
            - one enemy exits the game before the other
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(3, 3)
        # row 1, col = 7
        enemy_2 = EnemyMoveFireHeuristicAgent(1, 7)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(2, state.gameBoard.board_array[0][2])

    #TODO: What happens if 2 bullets are fired from the same spot?
    def test_game_example_2(self):
        """
        For this test
            - 2 enemies
            - neither enemy hits player
            - one enemy exits the game before the other
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)


        enemy_1 = EnemyMoveFireHeuristicAgent(3, 3)
        #row 1, col = 7
        enemy_2 = EnemyMoveFireHeuristicAgent(7, 7)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(2, state.gameBoard.board_array[0][2])

    def test_game_example_3(self):
        """
        For this test
            - 2 enemies
            - One enemy hits player, causes player to lose
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(9, 9)
        # row 1, col = 7
        enemy_2 = SimpleGoLeftAgent(8, 9)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEquals(0, state.gameBoard.board_array[0][0])
#ramzi merged
def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()