# Flask app for Smart Grocery + Recipe Planner
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime, timedelta
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# OpenAI setup
openai_client = None
try:
    import openai
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        openai_client = openai.OpenAI(api_key=openai_api_key)
        logger.info("✅ OpenAI client initialized")
    else:
        logger.warning("⚠️ OpenAI API key not found")
except ImportError:
    logger.warning("⚠️ OpenAI library not installed")

# Import custom modules (with error handling)
try:
    from meal_planner import generate_meal_plan, budget_filter
except ImportError:
    logger.warning("⚠️ meal_planner module not found. Some features may not work.")
    
try:
    from firebase_service import save_user_data, get_user_data
except ImportError:
    logger.warning("⚠️ firebase_service module not found. Using fallback storage.")
    
try:
    from openai_integration import generate_recipe_suggestions, generate_grocery_list
except ImportError:
    logger.warning("⚠️ openai_integration module not found. Some features may not work.")
    
try:
    from database_service import db_service
except ImportError:
    logger.warning("⚠️ database_service module not found. Creating simple fallback.")
    
    # Simple fallback database service
    class SimpleDatabaseService:
        def __init__(self):
            self.data = {'users': [], 'meal_plans': []}
            
        def save_user_profile(self, data):
            user_id = str(uuid.uuid4())
            data['user_id'] = user_id
            self.data['users'].append(data)
            return {'status': 'success', 'user_id': user_id}
            
        def get_user_profile(self, email):
            for user in self.data['users']:
                if user.get('email') == email:
                    return user
            return None
            
        def save_meal_plan(self, user_id, meal_plan_data):
            meal_plan_data['user_id'] = user_id
            meal_plan_data['id'] = str(uuid.uuid4())
            self.data['meal_plans'].append(meal_plan_data)
            return {'status': 'success'}
            
        def get_meal_plans(self, user_id):
            return [plan for plan in self.data['meal_plans'] if plan.get('user_id') == user_id]
            
        def save_health_tracking(self, user_id, data):
            return {'status': 'success'}
            
        def get_database_stats(self):
            return {
                'users': len(self.data['users']),
                'meal_plans': len(self.data['meal_plans']),
                'status': 'connected (fallback)'
            }
    
    db_service = SimpleDatabaseService()

# Create fallback functions for missing modules
def generate_meal_plan_fallback(health_data, budget, days, cuisine_preference):
    return {
        "daily_calories": 2000,
        "days": [
            {"breakfast": "Oatmeal with fruits", "lunch": "Grilled chicken salad", "dinner": "Baked salmon with vegetables"}
            for _ in range(days)
        ],
        "message": "Sample meal plan (using fallback)"
    }

def budget_filter_fallback(meal_plan, budget):
    return meal_plan

def generate_recipe_suggestions_fallback(dietary_preferences, cuisine_type):
    return [
        {"name": "Healthy Breakfast Bowl", "description": "Nutritious morning meal"},
        {"name": "Quick Lunch Salad", "description": "Fresh and light lunch option"},
        {"name": "Dinner Delight", "description": "Satisfying evening meal"}
    ]

def generate_grocery_list_fallback(meal_plan):
    return [
        {"name": "Oats", "estimated_cost": 5},
        {"name": "Chicken breast", "estimated_cost": 12},
        {"name": "Salmon fillet", "estimated_cost": 15},
        {"name": "Mixed vegetables", "estimated_cost": 8}
    ]

def save_user_data_fallback(health_data, meal_plan, recipe_suggestions):
    return {"status": "success", "storage": "fallback", "id": str(uuid.uuid4())}

def get_user_data_fallback():
    return []

# Override missing functions with fallbacks
if 'generate_meal_plan' not in globals():
    generate_meal_plan = generate_meal_plan_fallback
if 'budget_filter' not in globals():
    budget_filter = budget_filter_fallback
if 'generate_recipe_suggestions' not in globals():
    generate_recipe_suggestions = generate_recipe_suggestions_fallback
if 'generate_grocery_list' not in globals():
    generate_grocery_list = generate_grocery_list_fallback
if 'save_user_data' not in globals():
    save_user_data = save_user_data_fallback
if 'get_user_data' not in globals():
    get_user_data = get_user_data_fallback

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')
app.permanent_session_lifetime = timedelta(days=7)

# Configure app
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/meal-planner')
def meal_planner():
    """Meal planner page"""
    return render_template('meal_planner.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        flash('Please complete your profile first', 'warning')
        return redirect(url_for('meal_planner'))
    
    user_id = session['user_id']
    user_profile = db_service.get_user_profile(session.get('email', ''))
    meal_plans = db_service.get_meal_plans(user_id)
    
    return render_template('dashboard.html', 
                         user_profile=user_profile, 
                         meal_plans=meal_plans)

@app.route('/health-tracker')
def health_tracker():
    """Health tracking page similar to Streamlit version"""
    return render_template('health_tracker.html')

@app.route('/weight-loss')
def weight_loss():
    """Weight loss tracking page"""
    return render_template('weight_loss.html')

@app.route('/motion-detection')
def motion_detection():
    """Motion detection using OpenCV"""
    return render_template('motion_detection.html')

@app.route('/recipe-generator')
def recipe_generator():
    """Recipe generator page"""
    return render_template('recipe_generator.html')

@app.route('/ai-assistant')
def ai_assistant():
    """AI Assistant chat page"""
    return render_template('ai_assistant.html')

@app.route('/family-plans')
def family_plans():
    """Family meal planning page"""
    return render_template('family_plans.html')

@app.route('/api/generate-recipe', methods=['POST'])
def api_generate_recipe():
    """API endpoint for recipe generation"""
    try:
        data = request.get_json()
        
        # Use OpenAI API if available
        if openai_client:
            try:
                prompt = f"""
                Generate a detailed recipe based on these requirements:
                - Ingredients: {', '.join(data.get('ingredients', []))}
                - Cuisine: {data.get('cuisine_type', 'any')}
                - Meal type: {data.get('meal_type', 'lunch')}
                - Dietary restrictions: {', '.join(data.get('dietary_restrictions', []))}
                - Cooking time: {data.get('cooking_time', 'no preference')}
                - Servings: {data.get('servings', 4)}
                
                Return a JSON object with:
                - name (string)
                - prep_time (string)
                - servings (number)
                - calories (number)
                - ingredients (array of strings)
                - instructions (array of strings)
                - tips (string)
                """
                
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )
                
                recipe_text = response.choices[0].message.content
                
                # Try to parse JSON from response
                try:
                    import json
                    recipe = json.loads(recipe_text)
                except:
                    # Fallback if JSON parsing fails
                    recipe = create_fallback_recipe(data)
                
                return jsonify({
                    'status': 'success',
                    'recipe': recipe
                })
                
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return jsonify({
                    'status': 'success',
                    'recipe': create_fallback_recipe(data)
                })
        else:
            # Fallback recipe generation
            return jsonify({
                'status': 'success',
                'recipe': create_fallback_recipe(data)
            })
            
    except Exception as e:
        logger.error(f"Recipe generation error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate recipe'
        }), 500

def create_fallback_recipe(data):
    """Create a fallback recipe when AI is not available"""
    ingredients = data.get('ingredients', [])
    cuisine = data.get('cuisine_type', '').title()
    meal_type = data.get('meal_type', 'dish').title()
    servings = data.get('servings', 4)
    
    recipe_name = f"{cuisine} {meal_type}" if cuisine else f"Delicious {meal_type}"
    
    return {
        'name': recipe_name.strip(),
        'prep_time': '30-45 minutes',
        'servings': servings,
        'calories': 400,
        'ingredients': [
            f"1 portion {ingredient}" for ingredient in ingredients[:6]
        ] + [
            'Salt and pepper to taste',
            'Cooking oil as needed',
            'Fresh herbs (optional)'
        ],
        'instructions': [
            'Prepare all ingredients by washing and chopping as needed.',
            'Heat oil in a large pan or pot over medium heat.',
            'Add ingredients that take longest to cook first.',
            'Season with salt and pepper.',
            'Cook until all ingredients are tender and well combined.',
            'Adjust seasoning and serve hot.',
            'Garnish with fresh herbs if desired.'
        ],
        'tips': 'Feel free to adjust seasonings to your taste. Add your favorite spices or herbs to enhance the flavor!'
    }

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """Save user profile data"""
    try:
        data = request.get_json()
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            session.permanent = True
        
        # Save user profile
        result = db_service.save_user_profile(data)
        
        if result['status'] == 'success':
            session['user_id'] = result['user_id']
            session['email'] = data.get('email', '')
            session['name'] = data.get('name', '')
            
            return jsonify({
                'status': 'success',
                'message': 'Profile saved successfully!',
                'user_id': result['user_id']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save profile'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error saving profile: {str(e)}'
        }), 500

@app.route('/api/generate-meal-plan', methods=['POST'])
def api_generate_meal_plan():
    """Generate meal plan based on user preferences"""
    try:
        data = request.get_json()
        
        # Extract parameters
        health_data = {
            'age': data.get('age', 30),
            'weight': data.get('weight', 70),
            'height': data.get('height', 170),
            'activity_level': data.get('activity_level', 'moderate'),
            'dietary_preferences': data.get('dietary_preferences', []),
            'health_goals': data.get('health_goals', [])
        }
        
        budget = data.get('budget', 100)
        days = data.get('days', 7)
        cuisine_preference = data.get('cuisine_preference', 'any')
        
        # Generate meal plan
        meal_plan = generate_meal_plan(
            health_data=health_data,
            budget=budget,
            days=days,
            cuisine_preference=cuisine_preference
        )
        
        # Apply budget filter
        filtered_plan = budget_filter(meal_plan, budget)
        
        # Generate recipe suggestions
        recipe_suggestions = generate_recipe_suggestions(
            dietary_preferences=health_data['dietary_preferences'],
            cuisine_type=cuisine_preference
        )
        
        # Generate grocery list
        grocery_list = generate_grocery_list(filtered_plan)
        
        # Save to database if user is logged in
        if 'user_id' in session:
            meal_plan_data = {
                'name': f"Meal Plan {datetime.now().strftime('%Y-%m-%d')}",
                'meal_plan': filtered_plan,
                'recipe_suggestions': recipe_suggestions,
                'grocery_list': grocery_list,
                'health_data': health_data,
                'budget': budget,
                'days': days,
                'cuisine_preference': cuisine_preference,
                'calories_target': filtered_plan.get('daily_calories', 2000),
                'budget_limit': budget
            }
            
            save_result = db_service.save_meal_plan(session['user_id'], meal_plan_data)
            
            # Also save to Firebase/JSON for backup
            save_user_data(health_data, filtered_plan, recipe_suggestions)
        
        return jsonify({
            'status': 'success',
            'meal_plan': filtered_plan,
            'recipe_suggestions': recipe_suggestions,
            'grocery_list': grocery_list,
            'message': 'Meal plan generated successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating meal plan: {str(e)}'
        }), 500

@app.route('/api/save-health-tracking', methods=['POST'])
def save_health_tracking():
    """Save daily health tracking data"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'User not logged in'
            }), 401
        
        data = request.get_json()
        user_id = session['user_id']
        
        result = db_service.save_health_tracking(user_id, data)
        
        if result['status'] == 'success':
            return jsonify({
                'status': 'success',
                'message': 'Health data saved successfully!'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save health data'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error saving health data: {str(e)}'
        }), 500

@app.route('/api/get-meal-plans')
def get_meal_plans():
    """Get user's meal plans"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'User not logged in'
            }), 401
        
        user_id = session['user_id']
        meal_plans = db_service.get_meal_plans(user_id)
        
        return jsonify({
            'status': 'success',
            'meal_plans': meal_plans
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving meal plans: {str(e)}'
        }), 500

@app.route('/api/database-stats')
def database_stats():
    """Get database statistics"""
    try:
        stats = db_service.get_database_stats()
        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting database stats: {str(e)}'
        }), 500

@app.route('/api/user-profile')
def get_user_profile():
    """Get current user profile"""
    try:
        if 'email' not in session:
            return jsonify({
                'status': 'error',
                'message': 'User not logged in'
            }), 401
        
        email = session['email']
        profile = db_service.get_user_profile(email)
        
        if profile:
            return jsonify({
                'status': 'success',
                'profile': profile
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Profile not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving profile: {str(e)}'
        }), 500

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return '', 204  # No content response for favicon

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Health utility endpoints
@app.route('/api/calculate-bmi', methods=['POST'])
def calculate_bmi():
    """Calculate BMI"""
    try:
        data = request.get_json()
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0)) / 100  # Convert cm to m
        
        if weight <= 0 or height <= 0:
            return jsonify({
                'status': 'error',
                'message': 'Invalid weight or height'
            }), 400
        
        bmi = weight / (height ** 2)
        
        # BMI categories
        if bmi < 18.5:
            category = 'Underweight'
            color = 'info'
        elif bmi < 25:
            category = 'Normal weight'
            color = 'success'
        elif bmi < 30:
            category = 'Overweight'
            color = 'warning'
        else:
            category = 'Obese'
            color = 'danger'
        
        return jsonify({
            'status': 'success',
            'bmi': round(bmi, 1),
            'category': category,
            'color': color
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error calculating BMI: {str(e)}'
        }), 500

@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    """Calculate daily calorie needs"""
    try:
        data = request.get_json()
        
        age = int(data.get('age', 30))
        weight = float(data.get('weight', 70))
        height = float(data.get('height', 170))
        gender = data.get('gender', 'male')
        activity_level = data.get('activity_level', 'moderate')
        
        # Calculate BMR using Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        daily_calories = bmr * multiplier
        
        return jsonify({
            'status': 'success',
            'bmr': round(bmr),
            'daily_calories': round(daily_calories),
            'activity_level': activity_level
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error calculating calories: {str(e)}'
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI Assistant chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': 'Message is required'
            }), 400
        
        if not openai_client:
            return jsonify({
                'status': 'error',
                'message': 'AI Assistant is not available. Please check OpenAI configuration.'
            }), 500
            
        # Generate response using OpenAI
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful AI nutritionist and meal planning assistant. Provide helpful advice about nutrition, cooking, meal planning, healthy eating, recipes, and grocery shopping. Keep responses concise and practical."
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            return jsonify({
                'status': 'success',
                'response': ai_response
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error generating AI response: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing chat request: {str(e)}'
        }), 500

@app.route('/api/generate-family-plan', methods=['POST'])
def api_generate_family_plan():
    """Generate family meal plan endpoint"""
    try:
        data = request.get_json()
        family_members = data.get('family_members', [])
        preferences = data.get('preferences', {})
        
        if not family_members:
            return jsonify({
                'status': 'error',
                'message': 'Family members information is required'
            }), 400
        
        # Generate family meal plan (simplified version)
        family_plan = {
            'family_id': str(uuid.uuid4()),
            'created_at': datetime.now().isoformat(),
            'family_members': family_members,
            'meal_plan': {
                'monday': {
                    'breakfast': 'Family pancakes with fresh fruits',
                    'lunch': 'Chicken caesar salad (adult portions) / Chicken nuggets (kids)',
                    'dinner': 'Spaghetti bolognese with garlic bread'
                },
                'tuesday': {
                    'breakfast': 'Oatmeal with honey and berries',
                    'lunch': 'Grilled chicken wraps / PB&J sandwiches',
                    'dinner': 'Baked salmon with roasted vegetables'
                },
                'wednesday': {
                    'breakfast': 'Scrambled eggs with toast',
                    'lunch': 'Soup and sandwiches',
                    'dinner': 'Taco night with various toppings'
                },
                'thursday': {
                    'breakfast': 'Yogurt parfait with granola',
                    'lunch': 'Leftover tacos / Quesadillas',
                    'dinner': 'Chicken stir-fry with rice'
                },
                'friday': {
                    'breakfast': 'French toast sticks',
                    'lunch': 'Pizza day (homemade)',
                    'dinner': 'Fish and chips with mushy peas'
                },
                'saturday': {
                    'breakfast': 'Weekend brunch (eggs benedict)',
                    'lunch': 'BBQ burgers and hotdogs',
                    'dinner': 'Family pasta night'
                },
                'sunday': {
                    'breakfast': 'Family breakfast (bacon, eggs, toast)',
                    'lunch': 'Sunday roast dinner',
                    'dinner': 'Light soup and sandwiches'
                }
            },
            'grocery_list': [
                'Eggs (2 dozen)', 'Milk (2 gallons)', 'Bread (2 loaves)',
                'Chicken breast (2 lbs)', 'Ground beef (1 lb)', 'Salmon fillets (4 pieces)',
                'Mixed vegetables (frozen)', 'Pasta (2 boxes)', 'Rice (1 bag)',
                'Fresh fruits (bananas, apples, berries)', 'Yogurt (large container)',
                'Cheese (various types)', 'Tortillas', 'Peanut butter', 'Jam'
            ]
        }
        
        return jsonify({
            'status': 'success',
            'family_plan': family_plan
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating family plan: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Smart Grocery + Recipe Planner (Flask)")
    print("🔥 Database service initialized")
    print("📱 Available at: http://localhost:5000")
    
    # Initialize database
    db_stats = db_service.get_database_stats()
    print(f"📊 Database stats: {db_stats}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
