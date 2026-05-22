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
    
    @staticmethod
    def getFromString(s: str):
            try:
                return VolumeUnits[s]
            except KeyError:
                return None

class Volume:
    """A class to represent a volume with a defined unit"""
    def __init__(self, volume: float, unit: VolumeUnits):
        self.volume = volume * unit.value
        self.initialUnit = unit
    def get(self, unit = VolumeUnits.mL):
        """Returns the volume of the volume in the specified unit (mL by default)"""
        return self.volume / unit.value
    def getInInitialUnits(self):
        """Returns the volume of the volume in the units it was initially provided in"""
        return self.volume * self.initialUnit.value