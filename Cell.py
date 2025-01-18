from CellUpdateError import CellUpdateError
class Cell:

    def __init__(self, position, cell_type="R"):
        self.position= position
        self.cell_type= cell_type
        if not isinstance(position, int):
            raise TypeError("Position need to be an number")

        if not isinstance(cell_type, str):
            raise TypeError("Cell type need to be a string")

        if position < 1:
            raise ValueError("Position need to be positive number")

        if cell_type not in ["R", "S", "L"]:

            raise ValueError("Cell type need to be one of: R, S, L")
        self.next = None
        self.leap = None

    def update_next(self, next_cell):
        if not isinstance(next_cell, Cell):
            raise TypeError("the next cell must be Cell type")
        if self.next is not None:
            raise CellUpdateError
        if next_cell.position != self.position + 1:
            raise ValueError("The next cell must be in the next number")
        self.next = next_cell

    def update_leap(self, leap):
            if self.cell_type == "R":
                raise CellUpdateError

            if not isinstance(leap, Cell):
                raise TypeError("The leap argument must be a Cell")

            if self.cell_type == "L" and leap.position <= self.position:
                raise ValueError("For ladder cells, leap must be to a forward position")

            if self.cell_type == "S" and leap.position >= self.position:
                raise ValueError("For snake cells, leap must be to a backward position")

            self.leap = leap

    def __repr__(self):
        if self.cell_type == "R":
            if self.next:
                next_pos = self.next.position
            else:
                next_pos = ""
            return f"{self.position}:{self.cell_type}->{next_pos}"
        else:
            if self.leap:
                leap_pos = self.leap.position
            else:
                leap_pos = ""
            return f"{self.position}:{self.cell_type}->{leap_pos}"


