from ADTs import MyQueue
from Dice import Dice
from Board import Board
from Player import Player


class Game:
    def __init__(self, board_width, board_height, snakes_ladders, game_players=["Omri", "Tal"]):
        self.board_width = board_width
        self.board_height = board_height
        self.snakes_ladders = snakes_ladders
        self.game_players = game_players
        self.__board = Board(board_width, board_height, snakes_ladders)
        self.__dice = Dice()
        self.__players = []
        for player_name in game_players:
            player = Player(player_name, self.__board)
            self.__players.append(player)
        self.winner = None

    def play_turn(self):
        if self.winner is not None:
            return

        for player in self.__players:
            roll_result = self.__dice.roll()
            print(f"{player.name} rolled {roll_result}")

            old_position = player.position.data.val if player.position else None

            if player.move(roll_result) is True:
                print(f"{player.name} won the game!")
                self.winner = player
                return

            print(f"{player.name} moved from position {old_position} to position {player.position.data.val}")

            for other_player in self.__players:
                if other_player != player and other_player.position.data.val == player.position.data.val:
                    print(f"{other_player.name} was sent back to position 1")
                    other_player.position = self.__board.get_grid()[1]

    def run_game(self):
        while self.winner is None:
            self.play_turn()

        winner_player = self.winner
        turns_played = sum(player.num_turns for player in self.__players)

        return winner_player, turns_played

    def solve(self):
        queue = MyQueue()
        queue.enqueue((1, [1]))
        visited = set()

        while not queue.is_empty():
            position, path = queue.dequeue()

            if position in self.snakes_ladders:
                new_pos = self.snakes_ladders[position]
                if (new_pos, 0) not in visited:
                    visited.add((new_pos, 0))
                    queue.enqueue((new_pos, path + [new_pos]))
                continue

            for roll in range(1, 7):
                new_pos = position + roll

                if new_pos == len(self.__board):
                    return path + [new_pos]

                if new_pos < len(self.__board):
                    state = (new_pos, roll)
                    if state not in visited:
                        visited.add(state)
                        queue.enqueue((new_pos, path + [new_pos]))

    def __repr__(self):
        return f"Game(players={self.__players},\nboard={self.__board}\n****winner={self.winner if self.winner else 'game is still going on….'}****)"