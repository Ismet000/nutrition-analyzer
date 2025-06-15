import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_nutrition_data(food_name):
    """Enhanced API call with better error handling"""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_name,
        "api_key": os.getenv("USDA_API_KEY"),
        "pageSize": 3  # Get more results for better matches
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        foods = response.json().get("foods", [])
        
        if foods:
            # Find first food with complete nutrient data
            for food in foods:
                nutrients = {n["nutrientName"]: n["value"] 
                           for n in food.get("foodNutrients", [])}
                if all(k in nutrients for k in ["Protein", "Total lipid (fat)", "Carbohydrate, by difference"]):
                    return {
                        "Calories": nutrients.get("Energy", 0),
                        "Protein": nutrients.get("Protein", 0),
                        "Carbs": nutrients.get("Carbohydrate, by difference", 0),
                        "Fat": nutrients.get("Total lipid (fat)", 0),
                        "Fiber": nutrients.get("Fiber, total dietary", 0),
                        "Sugar": nutrients.get("Sugars, total including NLEA", 0)
                    }
        return None
    except Exception as e:
        print(f"API Error for {food_name}: {str(e)}")
        return None

def calculate_nutrition(ingredients):
    """More robust calculation with defaults"""
    nutrition = {
        "Calories": 0, "Protein": 0, "Carbs": 0,
        "Fat": 0, "Fiber": 0, "Sugar": 0
    }
    
    # Common food defaults (fallback when API fails)
    food_defaults = {
        "flour": {"Carbs": 75, "Protein": 10, "Calories": 364},
        "egg": {"Protein": 6, "Fat": 5, "Calories": 68},
        "sugar": {"Carbs": 100, "Calories": 387},
        "oil": {"Fat": 100, "Calories": 884}
    }
    
    for ing in ingredients:
        data = get_nutrition_data(ing["name"]) or {}
        
        # Try to find matching default
        for food_key in food_defaults:
            if food_key in ing["name"].lower():
                data = food_defaults[food_key]
                break
                
        # Calculate amounts (per 100g basis)
        amount = ing["amount"]
        if "cup" in ing["unit"]:
            amount *= 120  # Approximate grams per cup
        elif "tbsp" in ing["unit"]:
            amount *= 15  # Approximate grams per tbsp
            
        for nutrient in nutrition:
            nutrition[nutrient] += data.get(nutrient, 0) * (amount / 100)
            
    return {k: round(v, 2) for k, v in nutrition.items()}