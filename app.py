import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nutrition_calculator import calculate_nutrition
from recipe_parser import parse_recipe

st.set_page_config(layout="wide")
st.title("🍏 Enhanced Nutrition Calculator")

# Input section
recipe = st.text_area(
    "Enter your recipe (one ingredient per line):",
    "1 cup flour\n2 eggs\n100g sugar\n1 tbsp oil",
    height=150
)

if st.button("Analyze Nutrition"):
    with st.spinner("Calculating nutrition..."):
        ingredients = parse_recipe(recipe)
        nutrition = calculate_nutrition(ingredients)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Ingredients Recognized")
            st.dataframe(pd.DataFrame(ingredients))
            
            st.subheader("🧮 Nutrition Facts")
            nutri_df = pd.DataFrame({
                "Nutrient": nutrition.keys(),
                "Amount": nutrition.values()
            })
            st.dataframe(nutri_df.style.format({"Amount": "{:.2f}"}))
        
        with col2:
            st.subheader("📊 Macronutrient Distribution")
            
            # Only plot if we have valid data
            if sum([nutrition["Protein"], nutrition["Carbs"], nutrition["Fat"]]) > 0:
                fig, ax = plt.subplots()
                ax.pie(
                    [nutrition["Protein"], nutrition["Carbs"], nutrition["Fat"]],
                    labels=["Protein", "Carbs", "Fat"],
                    autopct="%1.1f%%",
                    colors=["#4CAF50", "#2196F3", "#FF9800"]
                )
                st.pyplot(fig)
            else:
                st.warning("Insufficient data to generate chart")