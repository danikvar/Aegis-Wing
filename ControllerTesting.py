from Model.GameModel import GameModel
from SimplePlayerController import SimplePlayerController
from SimpleTurtleView import SimpleTurtleView


def main():
    pass
    view = SimpleTurtleView()
    #default values
    gameModel = GameModel()
    controller = SimplePlayerController(view, gameModel)
    
if __name__ == "__main__":
    main()