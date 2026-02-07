import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_recipe_suggestions(meal_plan):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant that suggests recipes based on meal plans."},
                {"role": "user", "content": f"Based on this meal plan: {meal_plan}, suggest some detailed recipes with ingredients and cooking instructions."}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating recipe suggestions: {str(e)}"

def generate_grocery_list(meal_plan):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates grocery lists based on meal plans."},
                {"role": "user", "content": f"Create a grocery shopping list for this meal plan: {meal_plan}. Include quantities and organize by category."}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating grocery list: {str(e)}"
