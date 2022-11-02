from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameModel import GameModel
from SimpleTurtleView import SimpleTurtleView



class SimplePlayerController:
    #TODO change viewtype to interface
    def __init__(self, view: SimpleTurtleView, gameModel: GameModel ):
        self.view = view
        self.model = gameModel
        min_x, max_x,min_y,max_y = self.model.gameState.gameBoard.getBoardBoundaries()
        self.view.set_coord_values(min_x, max_x,min_y,max_y)
        #make 2 enemy agents somwhere on screen
        enemy_1 = SimpleGoLeftAgent(6,7)
        enemy_2 = SimpleGoLeftAgent(6,6)
        self.model.gameState.addAgent(enemy_1)
        self.model.gameState.addAgent(enemy_2)
        enemy_agents = self.model.gameState.current_agents
        self.view.set_up_turtles(enemy_agents)
        self.view.window.mainloop()