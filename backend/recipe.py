from ingredient import Ingredient, NutritionalInfo
from backend.units import Volume

class Recipe:
    """A class to represent a single recipe"""
    def __init__(
        self,
        name: str,
        ingredients: list[Ingredient],
        amounts: dict[int, float | Volume],
        steps: list[str],
    ):
        self.name = name
        self.ingredients = ingredients
        self.amounts = amounts
        self.steps = steps
        info = NutritionalInfo(0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        for i in ingredients:
            info += i.getNutritionalInfoForAmount(amounts[i.id])
        self.nutritionalInfo = info