from tkinter import E, W


class GridWidgets:
    def __init__(self, startrow=0, increment_horizontal=False, sticky=(E, W), padx=0):
        self.row = startrow
        self.column = 0
        self.increment_horizontal = increment_horizontal
        self.sticky = sticky
        self.padx = padx

    def grid_box(self, box, rowspan=1, columnspan=1):
        box.grid(
            column=self.column,
            row=self.row,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=self.sticky,
            padx=self.padx
        )
        if self.increment_horizontal:
            self.column += columnspan
        else:
            self.row += rowspan
