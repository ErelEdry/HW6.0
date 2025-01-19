from CellUpdateError import CellUpdateError
from ADTs import Node


class Cell:
    VALID_CELL_TYPES = {"R", "S", "L"}

    def __init__(self, position: int, cell_type: str = "R"):
        if not isinstance(position, int):
            raise TypeError("Position must be an integer")
        if not isinstance(cell_type, str):
            raise TypeError("Cell type must be a string")

        if position < 1:
            raise ValueError("Position must be a positive number")
        if cell_type not in self.VALID_CELL_TYPES:
            raise ValueError("Cell type must be one of: R, S, L")

        self.position = position
        self.data = Node(position)
        self.cell_type = cell_type
        self.next = None
        self.leap = None

    def update_next(self, next_cell: 'Cell') -> None:
        if not isinstance(next_cell, Cell):
            raise CellUpdateError(next_cell)

        if self.next is not None:
            raise CellUpdateError(next_cell)

        if next_cell.position != self.position + 1:
            raise ValueError("The next cell must be in the next position")

        self.next = next_cell
        self.data.next = next_cell.data

    def update_leap(self, leap: 'Cell') -> None:
        if self.cell_type == "R":
            raise CellUpdateError(leap)

        if not isinstance(leap, Cell):
            raise CellUpdateError(leap)

        if self.cell_type == "L" and leap.position <= self.position:
            raise ValueError("Invalid value")

        if self.cell_type == "S" and leap.position >= self.position:
            raise ValueError("Invalid value")

        self.leap = leap

    def __repr__(self) -> str:
        if self.cell_type == "R":
            next_pos = str(self.next.position) if self.next else ""
            return f"{self.position}:{self.cell_type}->"
        else:
            leap_pos = str(self.leap.position) if self.leap else ""
            return f"{self.position}:{self.cell_type}->{leap_pos}"

