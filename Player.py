from Board import Board
class Player:
    def __init__(self, name, board):
        if not isinstance(name, str):
           raise TypeError("name must be a string")
        if not name.isalpha():
            raise ValueError("name must be a string of letters")
        if not isinstance(board, Board):
            raise TypeError("board must be a Board object")
        self.name=name
        self.board=board
        self.position=None
        self.num_turns=0

    def __repr__(self):
        return f"Player(name={self.name}, position={self.position})"

    def move(self, roll):
        if not isinstance(roll, int):
            raise TypeError("roll need to be an int")
        if roll < 0 or roll > 7:
            raise ValueError("roll need to be smaller than 7 and bigger than 0")

        if self.position is None:
            self.position = 1

        new_position = self.position + roll

        board_size = len(self.board)
        if new_position >= board_size:
            self.position = board_size
            return True
        else:
            self.position = new_position
            return False






    
