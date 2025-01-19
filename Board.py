from Cell import Cell


class Board:
    def __init__(self, board_width=5, board_height=5,snakes_ladders={'L': {3: 9, 5: 11, 6: 24}, 'S': {20: 4, 16: 2, 18: 10}}):
        try:
            if not isinstance(board_width, int) or not isinstance(board_height, int):
                raise TypeError("Invalid type for one of the following argument: board_width, board_height")

            if not isinstance(snakes_ladders, dict) or not all(key in ['S', 'L'] for key in snakes_ladders):
                raise ValueError("Invalid type for one of the following argument: board_width, board_height")

            calculated_size = board_width * board_height
            if calculated_size < 25:
                raise ValueError("Invalid type for one of the following argument: board_width, board_height")

            if not snakes_ladders['L'] or not snakes_ladders['S']:
                raise ValueError("Invalid type for one of the following argument: board_width, board_height")

            for ladder_start, ladder_end in snakes_ladders['L'].items():
                if not isinstance(ladder_start, int) or not isinstance(ladder_end, int):
                    raise TypeError("Invalid type for one of the following argument: board_width, board_height")
                if ladder_start >= ladder_end or ladder_start > calculated_size or ladder_end > calculated_size:
                    raise ValueError("Invalid type for one of the following argument: board_width, board_height")

            for snake_start, snake_end in snakes_ladders['S'].items():
                if not isinstance(snake_start, int) or not isinstance(snake_end, int):
                    raise TypeError("Invalid type for one of the following argument: board_width, board_height")
                if snake_start <= snake_end or snake_start > calculated_size or snake_end > calculated_size:
                    raise ValueError("Invalid type for one of the following argument: board_width, board_height")

        except (TypeError, ValueError) as e:
            print(f"{e}")
            board_width = 5
            board_height = 5
            snakes_ladders = {'L': {3: 9, 5: 11, 6: 24}, 'S': {20: 4, 16: 2, 18: 10}}
            calculated_size = board_width * board_height

        self.__size = calculated_size
        self.board_width = board_width
        self.board_height = board_height
        self.snakes_ladders = snakes_ladders
        self.__grid = {}
        self.get_grid()

    def __iter__(self):
        self.current_position = 1
        return self

    def __next__(self):
        if self.current_position > self.__size:
            raise StopIteration
        cell = self.__grid[self.current_position]
        self.current_position += 1
        return cell

    def __repr__(self):
        board_repr = ""
        ladder_snake_positions = {}

        for cell in self:
            if cell.cell_type in {"L", "S"}:
                ladder_snake_positions[cell.position] = (
                    cell.leap.position,
                    cell.cell_type,
                )

        for row in range(self.board_height):
            row_repr = ""
            for col in range(self.board_width):
                cell_num = row * self.board_width + col + 1
                if cell_num in ladder_snake_positions:
                    target, cell_type = ladder_snake_positions[cell_num]
                    if cell_type == "L":
                        row_repr += f"[L{cell_num:02d}->{target:02d}]"
                    elif cell_type == "S":
                        row_repr += f"[S{cell_num:02d}->{target:02d}]"
                else:
                    row_repr += f"[{cell_num:02d}]"
            board_repr = row_repr + "\n" + board_repr
        return board_repr

    def get_grid(self):
        for position in range(1, self.board_width * self.board_height + 1):
            self.__grid[position] = Cell(position)

        for start, end in self.snakes_ladders['L'].items():
            self.__grid[start] = Cell(start, "L")
            self.__grid[start].update_leap(self.__grid[end])

        for start, end in self.snakes_ladders['S'].items():
            self.__grid[start] = Cell(start, "S")
            self.__grid[start].update_leap(self.__grid[end])

        for position in range(1, self.board_width * self.board_height):
            self.__grid[position].update_next(self.__grid[position + 1])

        return self.__grid[1]

    def __len__(self):
        return self.__size
