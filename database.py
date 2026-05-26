import sqlite3
from ingredient import Ingredient, NutritionalInfo
from recipe import Recipe
import units
import json
import numbers


class Database:
    """A class to represent the main database"""

    def __init__(self):
        self.con = sqlite3.connect("database.db")
        cur = self.con.cursor()
        self.con.execute("PRAGMA foreign_keys = ON;")
        cur.execute("""CREATE TABLE IF NOT EXISTS ingredients(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            servingArbitrary INTEGER NOT NULL,
            mLPerGram REAL,
            calories REAL NOT NULL,
            fat REAL NOT NULL,
            transfat REAL NOT NULL,
            cholesterol REAL NOT NULL,
            sodium REAL NOT NULL,
            carbs REAL NOT NULL,
            fiber REAL NOT NULL,
            sugars REAL NOT NULL,
            addedSugars REAL NOT NULL,
            protein REAL NOT NULL,
            vitaminD REAL NOT NULL,
            calcium REAL NOT NULL,
            iron REAL NOT NULL,
            potassium REAL NOT NULL
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS recipes(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            steps TEXT NOT NULL
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS ingredientsToRecipe(
            recipeId INTEGER NOT NULL,
            ingredientId INTEGER NOT NULL,
            amount REAL NOT NULL,
            amountUnit TEXT,
            
            PRIMARY KEY (recipeId, ingredientId),
            FOREIGN KEY (recipeId) REFERENCES recipes(id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (ingredientId) REFERENCES ingredients(id) ON UPDATE CASCADE ON DELETE RESTRICT
            
        )""")
        self.con.commit()

    def addIngredient(self, ingredient: Ingredient):
        """Adds an ingredient to the database or updates an existing ingredient
        - Ingredients that do not currently exist should have an id of None"""
        con = self._getConnection()
        cur = con.cursor()
        if ingredient.id is None:
            cur.execute(
                """
                INSERT INTO ingredients (
                    name,
                    servingArbitrary,
                    mLPerGram,
                    calories,
                    fat,
                    transfat,
                    cholesterol,
                    sodium,
                    carbs,
                    fiber,
                    sugars,
                    addedSugars,
                    protein,
                    vitaminD,
                    calcium,
                    iron,
                    potassium
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    ingredient.name,
                    int(ingredient.servingArbitrary),
                    ingredient.mLPerGram,
                    ingredient.nutritionalInfo.calories,
                    ingredient.nutritionalInfo.fat,
                    ingredient.nutritionalInfo.transFat,
                    ingredient.nutritionalInfo.cholesterol,
                    ingredient.nutritionalInfo.sodium,
                    ingredient.nutritionalInfo.carbs,
                    ingredient.nutritionalInfo.fiber,
                    ingredient.nutritionalInfo.sugars,
                    ingredient.nutritionalInfo.addedSugars,
                    ingredient.nutritionalInfo.protein,
                    ingredient.nutritionalInfo.vitaminD,
                    ingredient.nutritionalInfo.calcium,
                    ingredient.nutritionalInfo.iron,
                    ingredient.nutritionalInfo.potassium,
                ),
            )

            ingredient.id = cur.lastrowid

        else:
            cur.execute(
                """
                UPDATE ingredients
                SET name = ?,
                    servingArbitrary = ?,
                    mLPerGram = ?,
                    calories = ?,
                    fat = ?,
                    transfat = ?,
                    cholesterol = ?,
                    sodium = ?,
                    carbs = ?,
                    fiber = ?,
                    sugars = ?,
                    addedSugars = ?,
                    protein = ?,
                    vitaminD = ?,
                    calcium = ?,
                    iron = ?,
                    potassium = ?
                WHERE id = ?
            """,
                (
                    ingredient.name,
                    int(ingredient.servingArbitrary),
                    ingredient.mLPerGram,
                    ingredient.nutritionalInfo.calories,
                    ingredient.nutritionalInfo.fat,
                    ingredient.nutritionalInfo.transFat,
                    ingredient.nutritionalInfo.cholesterol,
                    ingredient.nutritionalInfo.sodium,
                    ingredient.nutritionalInfo.carbs,
                    ingredient.nutritionalInfo.fiber,
                    ingredient.nutritionalInfo.sugars,
                    ingredient.nutritionalInfo.addedSugars,
                    ingredient.nutritionalInfo.protein,
                    ingredient.nutritionalInfo.vitaminD,
                    ingredient.nutritionalInfo.calcium,
                    ingredient.nutritionalInfo.iron,
                    ingredient.nutritionalInfo.potassium,
                    ingredient.id,
                ),
            )
        con.commit()
        con.close()

    def addRecipe(self, recipe: Recipe):
        con = self._getConnection()
        cur = con.cursor()
        if recipe.id is None:
            try:
                cur.execute(
                    """INSERT INTO recipes (
                    name,
                    steps
                    )
                    VALUES(?, ?)""",
                    (recipe.name, json.dumps(recipe.steps)),
                )
                recipe.id = cur.lastrowid

                for i in recipe.ingredients:
                    cur.execute(
                        """INSERT INTO ingredientsToRecipe(
                        recipeId,
                        ingredientId,
                        amount,
                        amountUnit
                        )
                        VALUES(?, ?, ?, ?)""",
                        (
                            recipe.id,
                            i.id,
                            (
                                recipe.amounts[i.id]
                                if isinstance(recipe.amounts[i.id], numbers.Real)
                                else recipe.amounts[i.id].getInInitialUnits()
                            ),
                            (
                                None
                                if isinstance(recipe.amounts[i.id], numbers.Real)
                                else recipe.amounts[i.id].initialUnit.name
                            ),
                        ),
                    )
                con.commit()
            except Exception:
                con.rollback()
                raise
        else:
            try:
                cur.execute(
                    """
                            UPDATE recipes
                            SET name = ?,
                            steps = ?
                        WHERE id = ?
                            """,
                    (recipe.name, json.dumps(recipe.steps), recipe.id),
                )
                if cur.rowcount == 0:
                    raise ValueError(f"Recipe id {recipe.id} does not exist")
                cur.execute(
                    """DELETE FROM ingredientsToRecipe WHERE recipeId = ?""",
                    (recipe.id,),
                )
                for i in recipe.ingredients:
                    cur.execute(
                        """INSERT INTO ingredientsToRecipe(
                        recipeId,
                        ingredientId,
                        amount,
                        amountUnit
                        )
                        VALUES(?, ?, ?, ?)""",
                        (
                            recipe.id,
                            i.id,
                            (
                                recipe.amounts[i.id]
                                if isinstance(recipe.amounts[i.id], numbers.Real)
                                else recipe.amounts[i.id].getInInitialUnits()
                            ),
                            (
                                None
                                if isinstance(recipe.amounts[i.id], numbers.Real)
                                else recipe.amounts[i.id].initialUnit.name
                            ),
                        ),
                    )
                con.commit()
            except Exception:
                con.rollback()
                raise
        con.close()

    def getAllIngredients(self) -> list[tuple[int, str]]:
        con = self._getConnection()
        cur = con.cursor()
        return list(cur.execute("SELECT id, name FROM ingredients"))

    def getIngredient(self, id: int) -> Ingredient:
        con = self._getConnection()
        cur = con.cursor()
        cur.execute(
            """SELECT id, name, servingArbitrary, mLPerGram,
               calories, fat, transfat, cholesterol,
               sodium, carbs, fiber, sugars, addedSugars,
               protein, vitaminD, calcium, iron, potassium FROM ingredients WHERE id = ?""",
            (id,),
        )
        data = cur.fetchone()
        if data is None:
            raise ValueError(f"Ingredient {id} not found")
        return Ingredient(
            id,
            data[1],
            1,
            data[3],
            NutritionalInfo(
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
                data[15],
                data[16],
                data[17],
            ),
            servingArbitrary=bool(data[2]),
        )

    def getAllRecipes(self) -> list[tuple[int, str]]:
        con = self._getConnection()
        cur = con.cursor()
        return list(cur.execute("SELECT id, name FROM recipes"))

    def getRecipe(self, id: int) -> Recipe:
        con = self._getConnection()
        cur = con.cursor()
        cur.execute("""SELECT id, name, steps FROM recipes WHERE id = ?""", (id,))
        data = cur.fetchone()
        cur.execute(
            """SELECT ingredientId, amount, amountUnit FROM ingredientsToRecipe WHERE recipeId = ?""",
            (id,),
        )
        ingredients = []
        amounts = {}
        for i in cur.fetchall():
            unit = units.VolumeUnits.getFromString(i[2])
            if unit is None:
                amounts[i[0]] = i[1]
            else:
                amounts[i[0]] = units.Volume(i[1], unit)
            ingredients.append(self.getIngredient(i[0]))
        recipe = Recipe(id, data[1], ingredients, amounts, json.loads(data[2]))
        return recipe

    def deleteRecipe(self, id: int):
        con = self._getConnection()
        cur = con.cursor()
        try:
            cur.execute("""DELETE FROM recipes WHERE id = ?""", (id,))
            con.commit()
            con.close()
        except:
            con.rollback()
            raise

    def deleteIngredient(self, id: int):
        """
        Delete an ingredient.

        Returns:
            True if deleted successfully.
            False if deletion is blocked by constraints
            (e.g. ingredient is used in a recipe).
        """
        con = self._getConnection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM ingredients WHERE id = ?", (id,))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            con.rollback()
            return False
        finally:
            con.close()

    def _getConnection(self):
        return sqlite3.connect("database.db")
