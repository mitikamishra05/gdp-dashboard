import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ----------------------------
# Dummy Food Data
# ----------------------------
food_data = pd.DataFrame({
    'Food': ['Oatmeal', 'Grilled Chicken', 'Salad', 'Brown Rice', 'Apple', 'Greek Yogurt'],
    'Calories': [150, 250, 100, 220, 95, 120],
    'Protein': [5, 30, 2, 5, 0, 10],
    'Carbs': [27, 0, 5, 45, 25, 8],
    'Fat': [3, 3, 0, 2, 0, 0]
})

# ----------------------------
# Train Dummy ML Model
# ----------------------------
X_dummy = pd.DataFrame({
    'Age': np.random.randint(18, 60, 100),
    'Weight': np.random.randint(50, 100, 100),
    'Height': np.random.randint(150, 190, 100),
    'Activity_Level': np.random.randint(1, 4, 100),
    'Goal': np.random.randint(0, 2, 100)
})

y_dummy = (X_dummy['Weight'] * 10 + X_dummy['Height'] * 6.25 - X_dummy['Age'] * 5) + \
          5 * X_dummy['Activity_Level'] + 200 * (1 - X_dummy['Goal'])

model = RandomForestRegressor()
model.fit(X_dummy, y_dummy)

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🍎 Smart Diet Planner")

st.header("📋 Enter Your Details")
age = st.slider('Age', 10, 80, 25)
gender = st.selectbox('Gender', ['Male', 'Female'])
weight = st.slider('Weight (kg)', 30, 150, 70)
height = st.slider('Height (cm)', 100, 220, 170)
activity_level = st.selectbox('Activity Level', ['Sedentary', 'Moderately active', 'Very active'])
goal = st.selectbox('Health Goal', ['Weight Loss', 'Maintenance', 'Muscle Gain'])

# ----------------------------
# Process Input
# ----------------------------
activity_map = {'Sedentary': 1, 'Moderately active': 2, 'Very active': 3}
goal_map = {'Weight Loss': 1, 'Maintenance': 0, 'Muscle Gain': 0}

input_data = pd.DataFrame({
    'Age': [age],
    'Weight': [weight],
    'Height': [height],
    'Activity_Level': [activity_map[activity_level]],
    'Goal': [goal_map[goal]]
})

# Predict calories
predicted_calories = int(model.predict(input_data)[0])
st.success(f"✅ Your Estimated Daily Calorie Requirement: **{predicted_calories} kcal**")

# ----------------------------
# Recommend Meals
# ----------------------------
st.header("🍽️ Recommended Meals")

calories_remaining = predicted_calories
meal_plan = pd.DataFrame(columns=food_data.columns)
available_foods = food_data.copy()

# Select meals until close to calorie target
while calories_remaining > 0 and not available_foods.empty:
    choice = available_foods.sample(1)
    cal = int(choice['Calories'].values[0])
    
    if calories_remaining - cal >= -100:  # buffer of 100 kcal
        meal_plan = pd.concat([meal_plan, choice], ignore_index=True)
        calories_remaining -= cal
    
    available_foods = available_foods.drop(choice.index)

# Show meal plan
if not meal_plan.empty:
    st.write("### 🥗 Your Meal Plan")
    for _, row in meal_plan.iterrows():
        st.write(f"- {row['Food']} ({int(row['Calories'])} kcal)")
    
    st.markdown("---")
    st.markdown(f"**Total Calories:** {int(meal_plan['Calories'].sum())} kcal")
    st.markdown(f"**Protein:** {meal_plan['Protein'].sum()} g")
    st.markdown(f"**Carbs:** {meal_plan['Carbs'].sum()} g")
    st.markdown(f"**Fat:** {meal_plan['Fat'].sum()} g")
else:
    st.warning("⚠️ Not enough food items to create a full plan. Please add more foods.")
