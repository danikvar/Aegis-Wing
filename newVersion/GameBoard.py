from AgentInterface import AgentInterface


class GameBoard:
    '''
    This class represents a GameBoard, which is the environment the agents
    will be traversing through.
    '''

    def __init__(self, board_length: int,
                 board_height: int , minimum_x: int = 0,
                 minimum_y: int = 0):
        '''
        This represents the GameBoard for AegisWing
        It will be used to render a visual representation
        of agents and their positions
        :param board_length: {int} the length of the board
        :param board_height: {int} the height of the board
        :param minimum_x: {int} the lowest x/column value for the board, by default it is 0
        :param minimum_y: {int} the lowest y/row value for the board, by default it is 0
        '''

        if (board_length <= 0):
            raise ValueError("board length cannot be less than 0")
        if (board_height <= 0):
            raise ValueError("board height cannot be less than 0")

        self.board_length = board_length #
        self.board_height = board_height
        self.min_col = minimum_x # least column value
        self.min_row = minimum_y  # least row value

        # storing board as a 2D array, each row starts at x = 0
        # so if board is 10 units long, then x = {0,1,2...9}
        self.board_max_x_boundary = self.min_col + board_length - 1
        self.board_max_y_boundary = self.min_row + board_height - 1
        self.board_array = self.setUpBlankBoard()

    def getBoardBoundaries(self):
        """
        Get the board's inclusive boundaries
        :return: {quadruple} (min x, max_x, min_y,max_y)
        """
        return (self.min_col, self.board_max_y_boundary, self.min_row, self.board_max_y_boundary)

    def populate_board(self, agentIndex: int, agent: AgentInterface):
        """
        Add numbers that represent agents on board. Does not check
        if agents are beyond board or if agents clash. This is done by gameState class.
        :param agentIndex: {int} index value of agent
        :return: {None}
        """
        if agentIndex == 0:
            raise ValueError("0 represents empty space, agentIndex passed cannot be 0, must be 1 for player for ex.")

        agent_row_min, agent_row_max = agent.get_row_boundaries()
        agent_col_min, agent_col_max = agent.get_col_boundaries()

        for eachRow in self.board_array:
            if eachRow >= agent_row_min and eachRow <= agent_row_max:
                for eachCol in eachRow:
                    if eachCol >= agent_col_min and eachCol <= agent_col_max:
                        self.board_array[eachRow][eachCol] = agentIndex


    def setUpBlankBoard(self) -> list:
       '''
       Creates a board represented as a 2D array where all
       values inside each inner list is 0
       :return: {list[list[int]]} A 2D array of list
       '''

       board_2d_array = []

       for i in range(0, self.board_length):
           any_row = []
           for j in range(0, self.board_height):
               any_row.append(0)
           board_2d_array.append(any_row)

       return board_2d_array

    def __str__(self):
        '''
        Converts the 2D array board representation
        into a string
        :return:
        '''

        list_row_str = []
        board_str = ""

        for row in range(len(self.board_array)):
            temp = "|"
            temp += "\u0332" + " "
            current_row_list = self.board_array[row]
            for col in range(len(current_row_list)):
                temp += "\u0332" + (str(current_row_list[col]))
                temp += "\u0332" + " "
                temp += "|"
                if col < len(current_row_list) - 1:
                    temp += "\u0332" + " "
                else:
                    list_row_str.append(temp)

        for i in range(-1, -len(list_row_str) - 1, -1):
            board_str += list_row_str[i] + "\n"

        return board_str
