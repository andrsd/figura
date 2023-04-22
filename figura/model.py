
class Model:

    def __init__(self):
        self._units = "mm"

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        # can be: "mm", "cm", "m"
        if value in ["mm", "cm", "m"]:
            self._units = value
        else:
            raise ValueError("Units can be either 'mm', 'cm' or 'm'.")
