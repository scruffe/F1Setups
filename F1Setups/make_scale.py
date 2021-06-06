import tkinter
from tkinter import ttk
from limiter import Limiter


class MakeScale:
    def __init__(self, frame, step=0.0, offset=1.0, res=1):
        self.row_i = 1
        self.column = 2
        self.rowspan = 1
        self.sticky = 'NSEW'
        self.frame = frame
        self.text = ""

        self.from_ = 1
        self.to = 11
        self.step = step
        self.offset = offset
        self.res = res

        self.input_var = tkinter.IntVar()

    def create_separator(self):
        tkinter.ttk.Separator(self.frame).grid(row=self.row_i)

    def create_empty_space(self):
        tkinter.ttk.Label(self.frame, anchor=tkinter.W).grid(row=self.row_i)
        self.row_i += 1

    def create_scale(self):
        scale = Limiter(
            self.frame,
            from_=self.from_,
            to=self.to,
            orient=tkinter.HORIZONTAL,
            length=200,
            variable=self.input_var,
            precision=0,
            step=self.step,
            offset=self.offset,
            res=self.res
        )
        scale.grid(
            row=self.row_i,
            column=self.column + 1,
            columnspan=2,
            rowspan=self.rowspan,
            sticky=self.sticky)
        return scale

    def set_offset(self, label):
        var = self.input_var
        step = self.step
        res = self.res
        offset = self.offset

        def update_other_label(*args):
            value = var.get()
            multiplier = round(value * step, res)
            product = round(offset + multiplier - step, res)

            input_var_mult.set(product)

        self.input_var.trace_add("write", update_other_label)
        input_var_mult = tkinter.DoubleVar()

        label.config(textvariable=input_var_mult)

    def create_text_label(self):
        txt = tkinter.ttk.Label(
            self.frame,
            text=self.text,
            anchor=tkinter.W)
        txt.grid(
            row=self.row_i,
            column=self.column,
            columnspan=1,
            rowspan=self.rowspan,
            sticky=self.sticky)

    def create_value_label(self):
        scale_nr = tkinter.ttk.Label(
            self.frame,
            textvariable=self.input_var,
            anchor=tkinter.E,
            width=5)
        scale_nr.grid(
            row=self.row_i,
            column=self.column + 4,
            columnspan=1,
            rowspan=self.rowspan,
            sticky=self.sticky)

        return scale_nr

    def make(self, text, from_=1, to=11, step=0.0, offset=1.0, res=1):
        self.input_var = tkinter.IntVar()

        self.from_ = from_
        self.to = to
        self.text = text
        self.step = step
        self.offset = offset
        self.res = res

        if (self.row_i % 3) == 0:  # create empty space every 2 sliders
            self.create_empty_space()

        self.create_separator()
        scale = self.create_scale()
        self.create_text_label()
        scale_nr = self.create_value_label()

        if step != 0:
            self.set_offset(scale_nr)

        self.row_i += 1
        return scale
