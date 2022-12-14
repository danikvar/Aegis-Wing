import random

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.PlayerAgent import PlayerAgent
#TODO delete import below
from Model.GameState import GameState

#global DEBUG_TEST_COUNTER
#DEBUG_TEST_COUNTER = 0


class ExpectimaxPlayerAgent2(PlayerAgent):

    def __init__(self, agent_length: int = 1, agent_height: int = 1, lowest_row: int = 0, least_col: int = 0, expectimax_depth: int =0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.isInvulnerable = False
        self.turnsUntilInvulnerabilityOver = 0
        self.spawn_x = least_col
        self.spawn_y = lowest_row
        self.id = "1"
        self.expectimaxDepth = expectimax_depth

    def deepcopy(self):
        copy = ExpectimaxPlayerAgent2(self.agent_length, self.agent_height, self.lowest_row, self.least_col)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.hp = self.get_hp()
        return copy

      #TODO test this method if necessary, use when player dies and has another life left
    def respawnPlayer(self):
        #TODO would be an issue if game has more than 1 player life beacuse health not copied over
        respawned = ExpectimaxPlayerAgent2(self.agent_length,self.agent_height,self.spawn_y, self.spawn_x)
        return respawned

    def autoPickAction(self, state: GameState =None) -> Actions:
        if state == None:
            raise RuntimeError("Expectimax agent autopick action requires state")

        #Expectimax Algorithm
        best_action = None
        best_score = float('-inf')
        all_potential_actions = state.getAllLegalActions(0)

        #stores states which have the same score
        tied_states = []

        for i in range(len(all_potential_actions)):
            each_action = all_potential_actions[i]
            next_state = state.getStateAfterAction(0,each_action,moveBullets=True)

            if len(next_state.current_agents) > 1:
                state_score = self.chance_node(1,0,next_state)
            else:
                state_score = next_state.score

            if state_score > best_score:
                best_score = state_score
                best_action = each_action
            elif state_score == best_score:
                tied_states.append((each_action, state_score))
                if (best_action,best_score) not in tied_states:
                    tied_states.append((best_action, best_score))

        if len(tied_states) > 1:
            best_action = random.choice(tied_states)[0]

        #TODO DELETE
        print(f"tied states at turn={state.turns_left}\n{tied_states}")

        return best_action





    def chance_node(self, agentIndex: int, depth: int, state: GameState=None):
        #global DEBUG_TEST_COUNTER

        #Terminating case
        if depth >= self.expectimaxDepth:
            return state.score

        nextAgentIndex = None
        nextDepth = depth
        updateStateFlag = False

        if agentIndex + 1 > len(state.current_agents) - 1:
            nextAgentIndex = 0
            nextDepth = depth + 1
            updateStateFlag = True
        else:
            nextAgentIndex = agentIndex + 1

        #TODO delete
        #DEBUG_TEST_COUNTER += 1
        #print(DEBUG_TEST_COUNTER)

        #if DEBUG_TEST_COUNTER == 311:
            #print("WIll encounter error")

        all_legal_actions = state.getAllLegalActions(agentIndex)
        states_after_action = []
        arr_score_each_state = []

        for each_action in all_legal_actions:
            #maximizer node
            if agentIndex == 0 and state.current_agents[0].isPlayer() == True:
                stateAfterAction = state.getStateAfterAction(agentIndex,each_action,True)
            elif state.current_agents[0].isPlayer() == False:
                state.checkBulletAgentClashes()
                state.removeBullets()
                state.checkPlayerAgentClashes()
                state.updateAgentsList()
                state.update_board()
                state.reset_agents_move_status()
                state.decrement_turn()
                return state.score
            else:
                #minimizer nodes
                stateAfterAction = state.getStateAfterAction(agentIndex,each_action)

            #reached the end of a depth
            if updateStateFlag == True:
                stateAfterAction.checkBulletAgentClashes()
                stateAfterAction.removeBullets()
                stateAfterAction.checkPlayerAgentClashes()
                stateAfterAction.updateAgentsList()
                stateAfterAction.update_board()
                stateAfterAction.reset_agents_move_status()
                stateAfterAction.decrement_turn()

            states_after_action.append(stateAfterAction)

        chance_node_score = 0

        for each_state in states_after_action:
            if len(each_state.current_agents) > 1:
                score = self.chance_node(nextAgentIndex, nextDepth, each_state)
                chance_node_score += (1/len(states_after_action)) * score
            else:
                chance_node_score += (1/len(states_after_action)) * each_state.score

        return chance_node_score

