# Logic for meal planning (based on budget, health data)
import random

def generate_meal_plan(health_data, budget, cuisine_preference="No Preference", cooking_time=45, meal_types=None):
    """
    Generate a comprehensive meal plan based on user preferences and health data
    """
    if meal_types is None:
        meal_types = ["Breakfast", "Lunch", "Dinner"]
    
    try:
        # Extract health metrics
        bmi = health_data.get('bmi', 25)
        blood_sugar = health_data.get('blood_sugar', 100)
        bp = health_data.get('blood_pressure', '120/80')
        dietary_restrictions = health_data.get('dietary_restrictions', [])
        
        # Determine dietary recommendations based on health data
        health_recommendations = []
        
        if bmi > 25:
            health_recommendations.append("Low-calorie options for weight management")
        if blood_sugar > 140:
            health_recommendations.append("Low-sugar, complex carbohydrate meals")
        if "Diabetic-Friendly" in dietary_restrictions:
            health_recommendations.append("Diabetic-friendly with controlled portions")
        if "Low-Sodium" in dietary_restrictions:
            health_recommendations.append("Low-sodium preparations")
        
        # Base meal recommendations by cuisine
        meal_suggestions = {
            "Mediterranean": {
                "Breakfast": ["Greek yogurt with berries and nuts", "Whole grain toast with avocado", "Mediterranean omelet"],
                "Lunch": ["Greek salad with grilled chicken", "Hummus and vegetable wrap", "Lentil soup with whole grain bread"],
                "Dinner": ["Grilled fish with roasted vegetables", "Chicken souvlaki with quinoa", "Mediterranean pasta with vegetables"],
                "Snacks": ["Mixed nuts", "Greek yogurt", "Fresh fruit"]
            },
            "Asian": {
                "Breakfast": ["Congee with vegetables", "Miso soup with tofu", "Green tea and rice cakes"],
                "Lunch": ["Stir-fried vegetables with brown rice", "Miso glazed salmon", "Vegetable sushi rolls"],
                "Dinner": ["Steamed fish with ginger", "Vegetable curry with brown rice", "Grilled chicken teriyaki"],
                "Snacks": ["Edamame", "Green tea", "Seaweed snacks"]
            },
            "No Preference": {
                "Breakfast": ["Oatmeal with fresh fruits", "Scrambled eggs with vegetables", "Whole grain cereal"],
                "Lunch": ["Grilled chicken salad", "Quinoa bowl with vegetables", "Turkey and avocado wrap"],
                "Dinner": ["Baked salmon with sweet potato", "Lean beef stir-fry", "Vegetable pasta"],
                "Snacks": ["Apple slices with almond butter", "Greek yogurt", "Handful of nuts"]
            }
        }
        
        # Get appropriate meal suggestions
        if cuisine_preference in meal_suggestions:
            suggestions = meal_suggestions[cuisine_preference]
        else:
            suggestions = meal_suggestions["No Preference"]
        
        # Build meal plan
        meal_plan = f"🍽️ **Personalized 7-Day Meal Plan**\n\n"
        meal_plan += f"**Health Considerations:** {', '.join(health_recommendations) if health_recommendations else 'General healthy eating'}\n"
        meal_plan += f"**Budget:** ${budget}/week\n"
        meal_plan += f"**Cuisine Style:** {cuisine_preference}\n"
        meal_plan += f"**Max Cooking Time:** {cooking_time} minutes\n\n"
        
        for day in range(1, 8):
            meal_plan += f"**Day {day}:**\n"
            for meal_type in meal_types:
                if meal_type in suggestions:
                    meal = random.choice(suggestions[meal_type])
                    meal_plan += f"  • {meal_type}: {meal}\n"
            meal_plan += "\n"
        
        # Add shopping tips based on budget
        if budget < 50:
            meal_plan += "💡 **Budget Tips:** Focus on affordable proteins like eggs, beans, and chicken. Buy seasonal vegetables.\n"
        elif budget < 100:
            meal_plan += "💡 **Budget Tips:** Include variety with fish, lean meats, and diverse vegetables.\n"
        else:
            meal_plan += "💡 **Budget Tips:** You have flexibility for organic options and premium ingredients.\n"
        
        return meal_plan
        
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"

def budget_filter(meals, budget):
    """
    Filter meals based on the user's budget
    Args:
        meals: List of meal options with their costs
        budget: User's budget limit
    Returns:
        Filtered list of meals within budget
    """
    try:
        if isinstance(meals, list):
            return [meal for meal in meals if meal.get('cost', 0) <= budget]
        else:
            # Budget categories
            if budget < 50:
                return "Budget-friendly meals: Rice dishes, pasta, eggs, beans, seasonal vegetables"
            elif budget < 100:
                return "Moderate budget meals: Include chicken, fish, variety of vegetables, some organic options"
            else:
                return "Premium budget meals: Organic ingredients, premium proteins, diverse international cuisine"
    except Exception as e:
        return f"Error applying budget filter: {str(e)}"

def get_health_based_recommendations(health_data):
    """
    Generate specific dietary recommendations based on health metrics
    """
    recommendations = []
    
    try:
        bmi = health_data.get('bmi', 25)
        blood_sugar = health_data.get('blood_sugar', 100)
        
        if bmi > 30:
            recommendations.append("Focus on portion control and high-fiber foods")
        elif bmi > 25:
            recommendations.append("Include more vegetables and lean proteins")
        
        if blood_sugar > 140:
            recommendations.append("Choose low glycemic index foods")
            recommendations.append("Limit refined sugars and simple carbohydrates")
        
        if not recommendations:
            recommendations.append("Maintain a balanced diet with variety")
        
        return recommendations
    except Exception as e:
        return ["Focus on balanced nutrition"]
