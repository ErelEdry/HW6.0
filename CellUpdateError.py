class CellUpdateError(Exception):
    def __init__(self,next_cell):
        self.next_cell=next_cell
    def __str__(self):
        return f"Invalid attempt to modify the next or leap attribute!"

