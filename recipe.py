from ingredient import Ingredient, NutritionalInfo
from units import Volume
from flask import jsonify


class Recipe:
    """A class to represent a single recipe"""

    def __init__(
        self,
        id: int,
        name: str,
        ingredients: list[Ingredient],
        amounts: dict[int, float | Volume],
        steps: list[str],
    ):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.amounts = amounts
        self.steps = steps
        info = NutritionalInfo(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        for i in ingredients:
            info += i.getNutritionalInfoForAmount(amounts[i.id])
        self.nutritionalInfo = info

    def updateNutritionalInfo(self):
        for i in self.ingredients:
            info += i.getNutritionalInfoForAmount(self.amounts[i.id])
        self.nutritionalInfo = info

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": [ingredient.toDict() for ingredient in self.ingredients],
            "amounts": {
                id: (value.toDict() if isinstance(value, Volume) else value)
                for id, value in self.amounts.items()
            },
            "steps": self.steps,
        }
