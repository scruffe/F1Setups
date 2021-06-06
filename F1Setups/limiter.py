from tkinter import ttk

# precision limiter
# https://stackoverflow.com/questions/54186639/tkinter-control-ttk-scales-increment-as-with-tk-scale-and-a-tk-doublevar
class Limiter(ttk.Scale):
    """ ttk.Scale subclass that limits the precision of values. """

    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')  # Remove non-std kwarg.
        self.offset = kwargs.pop('offset')
        self.res = kwargs.pop('res')
        self.step = kwargs.pop('step')

        self.chain = kwargs.pop('command', lambda *a: None)  # Save if present.
        super(Limiter, self).__init__(*args, command=self._value_changed, **kwargs)

    def get(self, x=None, y=None):
        """Get the current value of the value option, or the value
        corresponding to the coordinates x, y if they are specified.

        x and y are pixel coordinates relative to the scale widget
        origin."""
        if self.offset != 1:  # offset has to do with sliders being 10 steps
            value = self.tk.call(self._w, 'get', x, y)

            m = round(value * self.step, self.res)
            return round(self.offset + m - self.step, self.res)

        return self.tk.call(self._w, 'get', x, y)

    def _value_changed(self, new_value):
        new_value = round(float(new_value), self.precision)
        if self.precision == 0:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), (int(new_value)))
        else:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), new_value)
        self.chain(new_value)  # Call user specified function.

