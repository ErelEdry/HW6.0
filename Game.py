from ADTs import MyQueue
from Dice import Dice
from Board import Board
from Player import Player


class Game:
    def __init__(self, board_width, board_height, snakes_ladders, game_players=["Omri", "Tal"]):
            try:
                self.__board = Board(board_width, board_height, snakes_ladders)
                self.__dice = Dice()
                self.game_players = ["Omri", "Tal"] if game_players is None or len(game_players) < 2 else game_players

                self.__players = []
                for player_name in self.game_players:
                    player = Player(player_name, self.__board)
                    self.__players.append(player)

                self.winner = None
                self.total_turns = 0
                self.current_player_index = 0
            except (TypeError, ValueError):
                self.__board = Board(5, 5, {'L': {3: 9, 5: 11, 6: 24}, 'S': {20: 4, 16: 2, 18: 10}})
                self.__dice = Dice()
                self.__players = []
                self.game_players = ["Omri", "Tal"] if game_players is None or len(game_players) < 2 else game_players

                for name in self.game_players:
                    player = Player(name, self.__board)
                    self.__players.append(player)

                self.winner = None
                self.total_turns = 0
                self.current_player_index = 0

    def handle_snake_ladder(self, player):
        if player.position and player.position.cell_type in ["S", "L"]:
            player.position = player.position.leap

    def play_turn(self):
        if self.winner is not None:
            return

        current_player = self.__players[self.current_player_index]
        try:
            roll_result = self.__dice.roll()
            print(f"{current_player.name} rolled a {roll_result}.")
            current_player.num_turns += 1

            if current_player.move(roll_result):
                print(f"{current_player.name} reached the end and wins!")
                self.winner = current_player
                return

            self.handle_snake_ladder(current_player)

            for other_player in self.__players:
                if (other_player != current_player and
                        other_player.position and current_player.position and
                        other_player.position.position == current_player.position.position):
                    other_player.position = self.__board.get_grid()

        except (ValueError, TypeError) as e:
            print(f"Error in player turn: {e}")
            self.__players.remove(current_player)
            if self.__players:
                self.current_player_index = self.current_player_index % len(self.__players)
            return

        self.current_player_index = (self.current_player_index + 1) % len(self.__players)

    def run_game(self):
        self.play_turn()
        print("Game Board:")
        print(self.__board)
        print("Starting the game!")
        first_turn = True

        while self.winner is None and self.__players:
            if first_turn:
                first_turn = False
            else:
                self.play_turn()

        if not self.__players:
            return None, 0

        winning_turns = sum(p.num_turns for p in self.__players)
        return self.winner, winning_turns

    def solve(self):
        queue = MyQueue()
        queue.enqueue((1, [1]))
        visited = {1}
        board_size = len(self.__board)

        while not queue.is_empty():
            curr_pos, path = queue.dequeue()

            if curr_pos == board_size:
                return path

            for roll in range(1, 7):
                next_pos = curr_pos + roll

                if next_pos > board_size:
                    continue

                if next_pos in visited:
                    continue

                visited.add(next_pos)
                new_path = path.copy()

                for intermediate_pos in range(curr_pos + 1, next_pos + 1):
                    new_path.append(intermediate_pos)

                next_cell = None
                for cell in self.__board:
                    if cell.position == next_pos:
                        next_cell = cell
                        break

                if next_cell and next_cell.cell_type in ['S', 'L']:
                    leap_pos = next_cell.leap.position
                    if leap_pos not in visited:
                        visited.add(leap_pos)
                        new_path.append(leap_pos)
                    queue.enqueue((leap_pos, new_path))
                else:
                    queue.enqueue((next_pos, new_path))


    def __repr__(self):
        return f"Game(players={self.__players},\nboard={self.__board}\n****winner={self.winner if self.winner else 'game is still going on….'}****)"
game = Game(2, 2, 2, ["Shir"])
game.play_turn()
print(game.run_game())
path = game.solve()
print(path, f"\nTest result for shortest path {path == [1, 2, 3, 4, 5, 6, 24, 25]}")
add_game = Game(6, 6, snakes_ladders={"L": {5: 18, 10: 33, 14: 25}, "S": {34: 9, 32: 16, 22: 12, 19: 17}},game_players=["Tal", "Yuval"])
add_game.play_turn()
print(add_game.run_game())
path = add_game.solve()
print(path, f"\nTest result for shortest path {path == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 33, 34, 35, 36]}")
