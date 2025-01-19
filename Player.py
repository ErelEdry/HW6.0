from Board import Board
from Dice import Dice


class Player:
    def __init__(self, name, board):
        if not isinstance(name, str):
           raise TypeError("name must be a string")
        if not name.isalpha():
            raise ValueError("name must be a string of letters")
        if not isinstance(board, Board):
            raise TypeError("board must be a Board object")
        self.name = name
        self.board = board
        self.position = None
        self.num_turns = 0

    def __repr__(self):
        pos_repr = str(self.position) if self.position else None
        return f"Player(name={self.name}, position={pos_repr})"

    def move(self, roll):
        if not isinstance(roll, int):
            raise TypeError("roll need to be an int")
        if roll < 0 or roll > 7:
            raise ValueError("roll need to be smaller than 7 and bigger than 0")

        if self.position is None:
            for cell in self.board:
                if cell.position == 1:
                    self.position = cell
                    return False

        target_position = self.position.position + roll
        board_size = len(self.board)

        if target_position > board_size:
            return False

        if target_position == board_size:
            for cell in self.board:
                if cell.position == board_size:
                    self.position = cell
                    break
            return True

        for cell in self.board:
            if cell.position == target_position:
                self.position = cell
                break

        return False