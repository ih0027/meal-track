from database import Database
from ingredient import Ingredient
from recipe import Recipe
from units import Volume
from flask import Flask

db = Database()
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"