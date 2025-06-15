import re

def parse_recipe(recipe_text):
    ingredients = []
    for line in recipe_text.split('\n'):
        if line.strip():
            parts = re.split(r'(\d+\.?\d*)', line.strip(), maxsplit=1)
            if len(parts) > 1:
                amount = float(parts[1])
                rest = parts[2].strip().split()
                unit = rest[0] if rest else "unit"
                name = " ".join(rest[1:]) if len(rest) > 1 else rest[0]
                ingredients.append({"name": name, "amount": amount, "unit": unit})
    return ingredients