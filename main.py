from database import Database
from ingredient import Ingredient, NutritionalInfo
from recipe import Recipe
from units import Volume
import units
from flask import Flask, request, jsonify, abort

db = Database()

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.get("/ingredients")
def getIngredients():
    return jsonify(db.getAllIngredients())


@app.get("/ingredient/<int:id>")
def getIngredient(id):
    return jsonify(db.getIngredient(int(id)).toDict())


@app.post("/ingredient")
def addIngredient():
    try:
        try:
            id = request.json["id"]
        except Exception:
            id = None
        isArbitrary = request.json["servingArbitrary"] is True
        servingVolume = None
        if not isArbitrary:
            vol = request.json["servingVolume"]
            servingVolume = Volume(
                vol["amount", units.VolumeUnits.getFromString(vol["unit"])]
            )
        ingredient = Ingredient(
            id,
            request.json["name"],
            float(request.json["servingGrams"]),
            servingVolume,
            NutritionalInfo(**request.json["nutritionalInfo"]),
            servingArbitrary=isArbitrary,
        )
    except Exception as e:
        abort(400)
    # try:
    db.addIngredient(ingredient)
    # except Exception as e:
    #     raise(e)
    #     abort(500)
    return jsonify(ingredient.toDict()), 201


@app.get("/recipes")
def getRecipes():
    return jsonify(db.getAllRecipes())


@app.get("/recipe/<int:id>")
def getRecipe(id: int):
    return jsonify(db.getRecipe(id).toDict())


@app.post("/recipe")
def addRecipe():
    # try:
    try:
        id = request.json["id"]
    except Exception:
        id = None
    ing = []
    for i in request.json["ingredients"]:
        ing.append(db.getIngredient(i))
    amo = {}
    for key, value in request.json["amounts"].items():
        unit = value.get("unit")
        if unit is not None:
            a = Volume(value["amount"], units.VolumeUnits.getFromString(unit))
        else:
            a = value["amount"]
        amo[int(key)] = a
    recipe = Recipe(id, request.json["name"], ing, amo, request.json["steps"])
    # except Exception:
    #     abort(400)
    db.addRecipe(recipe)
    return jsonify(recipe.toDict()), 201


@app.delete("/recipe/<int:id>")
def deleteRecipe(id: int):
    db.deleteRecipe(id)
    return jsonify(True), 200


@app.delete("/ingredient/<int:id>")
def deleteIngredient(id: int):
    try:
        deleted = db.deleteIngredient(id)
    except Exception:
        abort(500)
    if not deleted:
        return jsonify({"error": "Ingredient is used in recipes"}), 409
    return jsonify(True), 200
