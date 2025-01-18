from CellUpdateError import CellUpdateError
from ADTs import Node


class Cell:
    def __init__(self, position, cell_type="R"):
        if not isinstance(position, int):
            raise TypeError("Position must be an integer")
        if not isinstance(cell_type, str):
            raise TypeError("Cell type must be a string")
        if position < 1:
            raise ValueError("Position must be a positive number")
        if cell_type not in ["R", "S", "L"]:
            raise ValueError("Cell type must be one of: R, S, L")

        self.data = Node(position)
        self.cell_type = cell_type
        self.next = None
        self.leap = None

    def update_next(self, next_cell):
        if not isinstance(next_cell, Cell):
            raise CellUpdateError(next_cell)

        if self.next is not None:
            raise CellUpdateError(next_cell)

        if next_cell.data.val != self.data.val + 1:
            raise ValueError("The next cell must be in the next position")

        self.next = next_cell
        self.data.next = next_cell.data

    def update_leap(self, leap):
        if self.cell_type == "R":
            raise CellUpdateError(leap)

        if not isinstance(leap, Cell):
            raise CellUpdateError(leap)

        if self.cell_type == "L" and leap.data.val <= self.data.val:
            raise ValueError("For ladder cells, leap must be to a forward position")

        if self.cell_type == "S" and leap.data.val >= self.data.val:
            raise ValueError("For snake cells, leap must be to a backward position")

        self.leap = leap

    def __repr__(self):
        position_str = str(self.data.val)
        if self.cell_type == "R":
            next_pos = str(self.next.data.val) if self.next else ""
            return f"{position_str}:{self.cell_type}->{next_pos}"
        else:
            leap_pos = str(self.leap.data.val) if self.leap else ""
            return f"{position_str}:{self.cell_type}->{leap_pos}"