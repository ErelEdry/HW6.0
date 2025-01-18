from Cell import Cell

class Board:
    def __init__(self, board_width=5, board_height=5,snakes_ladders={'L': {3: 9, 5: 11, 6: 24}, 'S': {20: 4, 16: 2, 18: 10}}):
        if not isinstance(board_width, int):
            raise TypeError("board_width must be a int")
        if board_width < 4:
            raise ValueError("board_width must be bigger than 4")
        if not isinstance(board_height, int):
            raise TypeError("board_height must be a int")
        if board_height < board_width:
            raise ValueError("board_height must be a equally or bigger than the board_width")
        if not isinstance(snakes_ladders, dict):
            raise TypeError("snakes_ladders must be a dictionary")
        if not all(key in ['S', 'L'] for key in snakes_ladders):
            raise ValueError("snakes_ladders must be a dictionary with keys 'S' and 'L'")

        self.board_width = board_width
        self.board_height = board_height
        self.snakes_ladders = snakes_ladders

    def __iter__(self):
        self.position = 0
        return self

    def __next__(self):
        position= self.position+1
        if position >self.board_width*self.board_height:
            return StopIteration()
        self.position=position
        return self.get_grid()[position]

    def __repr__(self):
        board_repr = ""
        ladder_snake_positions = {}

        for cell in self:
            if cell.cell_type in {"L", "S"}:
                ladder_snake_positions[cell.data.val] = (
                    cell.leap.data.val,
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
        grid = {}

        for position in range(1, self.board_width * self.board_height + 1):
            grid[position] = Cell(position)

        for start, end in self.snakes_ladders['L'].items():
            grid[start] = Cell(start, "L")
            grid[start].update_leap(grid[end])

        for start, end in self.snakes_ladders['S'].items():
            grid[start] = Cell(start, "S")
            grid[start].update_leap(grid[end])

        for position in range(1, self.board_width * self.board_height):
            grid[position].update_next(grid[position + 1])

        return grid

    def __len__(self):
        board_size=self.board_height*self.board_width
        return board_size