class SliderCounter:
    """reads corresponding slider value in setup file and sets a slider to that value"""

    def __init__(self, unpacked_setup):
        self.setup = unpacked_setup
        self.x = 41

    def set_slider_value(self, scale):
        self.x += 3

        if scale.offset != 1:
            self.set_slider_with_offset(scale)
        else:
            scale.set(self.setup[self.x])

    # Translates the 10 steps in sliders to actual values for/from the setup files
    def set_slider_with_offset(self, scale):
        value = self.setup[self.x]
        p = round(value - scale.offset, scale.res)
        product = round(p / scale.step, scale.res) + 1
        scale.set(product)