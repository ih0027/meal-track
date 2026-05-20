import units as units
import dataclasses
import numbers


@dataclasses.dataclass
class NutritionalInfo:
    """A class to represent the complete nutritional info of an ingredient or recipe"""

    calories: float
    fat: float
    transFat: float
    cholesterol: float
    sodium: float
    carbs: float
    fiber: float
    sugars: float
    addedSugars: float
    protein: float
    vitaminD: float
    calcium: float
    iron: float
    potassium: float

    def __add__(self, other: "NutritionalInfo") -> "NutritionalInfo":
        if not isinstance(other, NutritionalInfo):
            return NotImplemented
        summed = {
            attr: getattr(self, attr) + getattr(other, attr) for attr in vars(self)
        }

        return NutritionalInfo(**summed)

    def __mul__(self, other: float) -> "NutritionalInfo":
        if not isinstance(other, numbers.Real):
            return NotImplemented
        multiplied = {
            attr: getattr(self, attr) * other for attr in vars(self)
        }

        return NutritionalInfo(**multiplied)\
            
    def __rmul__(self, other: float) -> "NutritionalInfo":
        return self.__mul__(self, other)


class Ingredient:
    """A class to represent a single ingredient"""

    def __init__(
        self,
        id: int,
        name: str,
        servingGrams: float,
        servingVolume: units.Volume,
        nutritionalInfo: NutritionalInfo,
        servingArbitrary: bool = False,
    ):
        self.id = id
        self.name = name
        self.servingArbitrary = servingArbitrary
        if servingArbitrary:
            self.nutritionalInfo = nutritionalInfo
        else:
            self.mLPerGram = servingVolume.get() / servingGrams
            self.nutritionalInfo = self._normalizeNutritionalInfo(
                nutritionalInfo, servingGrams
            )

    def _normalizeNutritionalInfo(
        self, nutritionalInfo: NutritionalInfo, servingGrams: float
    ) -> NutritionalInfo:

        normalized = {
            attr: value / servingGrams for attr, value in vars(nutritionalInfo).items()
        }

        return NutritionalInfo(**normalized)

    def getNutritionalInfoForAmount(self, amount: float | units.Volume):
        """
        Get nutrition information for a specified amount.

        Numeric amounts are interpreted as:
        - grams for normalized ingredients
        - serving counts for arbitrary-serving ingredients
        """
        if isinstance(amount, (float, numbers.Real)):
            info = {
                attr: value * amount
                for attr, value in vars(self.nutritionalInfo).items()
            }
        else:
            info = {
                attr: value * amount.get() / self.mLPerGram
                for attr, value in vars(self.nutritionalInfo).items()
            }
        return NutritionalInfo(**info)
