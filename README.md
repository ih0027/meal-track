# Meal Track

Meal Track is a lightweight backend for managing ingredients, recipes, and nutrition data. The project provides a Python + Flask API for storing meal-planning information in SQLite and calculating recipe-level nutrition totals.

## Overview

This repository currently contains the backend API and data layer. The frontend user interface is not yet implemented, so this project is best viewed as a backend-first foundation for a meal tracking app.

## Why this project exists

Meal Track is designed to help organize:

- ingredient databases with nutritional values
- recipe compositions and ingredient quantities
- nutrition aggregation across recipe ingredients
- persistence in a lightweight local database

## Features

- Ingredient management with nutrition metadata
- Recipe creation with ingredient quantities and steps
- Calculation of total nutrition for a recipe
- SQLite persistence with no external database required
- JSON API for integration with a future frontend or other tooling

## Tech stack

- Python
- Flask
- SQLite

## Project structure

- `main.py` – Flask app and API routes
- `database.py` – database setup and CRUD logic
- `ingredient.py` – ingredient and nutrition model logic
- `recipe.py` – recipe model and nutrition aggregation
- `units.py` – volume-unit conversion helpers
- `database.db` – SQLite database created automatically at runtime

## Requirements

- Python 3.10+
- Flask

Install the dependency:

```bash
pip install flask
```

## Getting started

Run the app from the project root:

```bash
python main.py
```

The server will start in Flask development mode and listen on port `5000` by default.

## API endpoints

The API exposes a small JSON interface for ingredient and recipe management.

### Ingredient endpoints

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/ingredients` | Return all ingredient records. |
| `GET` | `/ingredient/<id>` | Return one ingredient by ID. |
| `POST` | `/ingredient` | Create or update an ingredient. |
| `DELETE` | `/ingredient/<id>` | Delete an ingredient by ID. |

### Recipe endpoints

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/recipes` | Return all recipes. |
| `GET` | `/recipe/<id>` | Return one recipe by ID. |
| `POST` | `/recipe` | Create or update a recipe. |
| `DELETE` | `/recipe/<id>` | Delete a recipe by ID. |

### Example ingredient payload

```json
{
  "id": 1,
  "name": "Chicken Breast",
  "servingGrams": 100,
  "servingArbitrary": false,
  "servingVolume": {
    "amount": 1,
    "unit": "CUP"
  },
  "nutritionalInfo": {
    "calories": 165,
    "fat": 3.6,
    "transFat": 0,
    "cholesterol": 85,
    "sodium": 74,
    "carbs": 0,
    "fiber": 0,
    "sugars": 0,
    "addedSugars": 0,
    "protein": 31,
    "vitaminD": 0,
    "calcium": 11,
    "iron": 0.9,
    "potassium": 256
  }
}
```

### Example recipe payload

```json
{
  "id": 1,
  "name": "Chicken Rice Bowl",
  "ingredients": [1, 2],
  "amounts": {
    "1": {
      "amount": 150,
      "unit": "mL"
    },
    "2": 200
  },
  "steps": [
    "Cook the rice",
    "Season the chicken",
    "Assemble the bowl"
  ]
}
```

## Data model

The application models nutrition data around two primary entities: ingredients and recipes.

### Ingredient model

```json
{
  "id": 1,
  "name": "Chicken Breast",
  "servingArbitrary": false,
  "mLPerGram": 0.9,
  "nutritionalInfo": {
    "calories": 1.65,
    "fat": 0.036,
    "transFat": 0,
    "cholesterol": 0.85,
    "sodium": 0.74,
    "carbs": 0,
    "fiber": 0,
    "sugars": 0,
    "addedSugars": 0,
    "protein": 0.31,
    "vitaminD": 0,
    "calcium": 0.11,
    "iron": 0.009,
    "potassium": 2.56
  }
}
```

### Recipe model

```json
{
  "id": 1,
  "name": "Chicken Rice Bowl",
  "ingredients": [
    {
      "id": 1,
      "name": "Chicken Breast",
      "servingArbitrary": false,
      "mLPerGram": 0.9,
      "nutritionalInfo": {
        "calories": 1.65,
        "fat": 0.036,
        "transFat": 0,
        "cholesterol": 0.85,
        "sodium": 0.74,
        "carbs": 0,
        "fiber": 0,
        "sugars": 0,
        "addedSugars": 0,
        "protein": 0.31,
        "vitaminD": 0,
        "calcium": 0.11,
        "iron": 0.009,
        "potassium": 2.56
      }
    }
  ],
  "amounts": {
    "1": {
      "milliliters": 150,
      "amount": 150,
      "unit": "mL"
    }
  },
  "steps": [
    "Cook the rice",
    "Season the chicken",
    "Assemble the bowl"
  ]
}
```

## Database

SQLite is used for local persistence. The database file is created automatically as `database.db` in the project root when the app starts.