from enum import Enum

class VolumeUnits(Enum):
    """A enum relating US cooking measures to mL"""
    mL = 1
    TEASPOON = 5
    TABLESPOON = 14.79
    FLUID_OUNCE = 29.57
    CUP = 236.59
    PINT = 473.18
    QUART = 9500
    GALLON = 37900

class Volume:
    """A class to represent a volume with a defined unit"""
    def __init__(self, volume: float, unit: VolumeUnits):
        self.volume = volume * unit.value
    def get(self, unit = VolumeUnits.mL):
        """Returns the volume of the volume in the specified unit (mL by default)"""
        return self.volume / unit.value