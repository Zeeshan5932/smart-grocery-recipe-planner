// Meal Planner JavaScript Functions
let userBMI = null;
let userBMICategory = '';

// BMI Calculator Function
function calculateBMI() {
    console.log('calculateBMI function called');
    
    const height = parseFloat(document.getElementById('height').value);
    const weight = parseFloat(document.getElementById('weight').value);
    
    console.log('Height:', height, 'Weight:', weight);
    
    if (!height || !weight || height <= 0 || weight <= 0) {
        alert('Please enter valid height and weight values.');
        return;
    }
    
    // Calculate BMI
    const bmi = (weight / ((height / 100) ** 2)).toFixed(1);
    userBMI = bmi;
    
    console.log('Calculated BMI:', bmi);
    
    // Determine BMI category
    let category = '';
    let categoryClass = '';
    
    if (bmi < 18.5) {
        category = 'Underweight';
        categoryClass = 'text-warning';
    } else if (bmi >= 18.5 && bmi < 25) {
        category = 'Normal weight';
        categoryClass = 'text-success';
    } else if (bmi >= 25 && bmi < 30) {
        category = 'Overweight';
        categoryClass = 'text-warning';
    } else {
        category = 'Obese';
        categoryClass = 'text-danger';
    }
    
    userBMICategory = category;
    console.log('BMI Category:', category);
    
    // Display BMI result
    const bmiValueElement = document.getElementById('bmi-value');
    const bmiCategoryElement = document.getElementById('bmi-category');
    const bmiInstructions = document.getElementById('bmi-instructions');
    const bmiResult = document.getElementById('bmi-result');
    
    if (bmiValueElement) bmiValueElement.textContent = bmi;
    if (bmiCategoryElement) {
        bmiCategoryElement.textContent = category;
        bmiCategoryElement.className = 'fw-bold ' + categoryClass;
    }
    
    // Hide instructions and show result
    if (bmiInstructions) bmiInstructions.classList.add('d-none');
    if (bmiResult) bmiResult.classList.remove('d-none');
    
    alert('BMI calculated successfully! Your BMI is ' + bmi + ' (' + category + ')');
}

// Function to proceed to meal planning
function proceedToMealPlan() {
    if (userBMI) {
        // Hide BMI section and show meal planning section
        const mealPlanningSection = document.getElementById('meal-planning-section');
        if (mealPlanningSection) {
            mealPlanningSection.classList.remove('d-none');
            
            // Scroll to meal planning section
            mealPlanningSection.scrollIntoView({ behavior: 'smooth' });
            
            // Update profile information
            updateUserProfile();
            
            // Generate meal suggestions
            generateMealSuggestions();
        }
    } else {
        alert('Please calculate your BMI first!');
    }
}

// Update user profile in meal planning section
function updateUserProfile() {
    const profileBMI = document.getElementById('profile-bmi');
    const profileCategory = document.getElementById('profile-category');
    const healthGoal = document.getElementById('health-goal');
    
    if (profileBMI) profileBMI.textContent = userBMI;
    if (profileCategory) profileCategory.textContent = userBMICategory;
    
    // Set health goal based on BMI category
    let goal = '';
    if (userBMICategory === 'Underweight') {
        goal = 'Focus on healthy weight gain with nutrient-rich foods';
    } else if (userBMICategory === 'Normal weight') {
        goal = 'Maintain current weight with balanced nutrition';
    } else if (userBMICategory === 'Overweight') {
        goal = 'Gradual weight loss with portion control';
    } else if (userBMICategory === 'Obese') {
        goal = 'Structured weight loss with professional guidance';
    }
    
    if (healthGoal) healthGoal.textContent = goal;
}

// Generate meal suggestions based on BMI category
function generateMealSuggestions() {
    const breakfast = document.getElementById('breakfast-suggestions');
    const lunch = document.getElementById('lunch-suggestions');
    const dinner = document.getElementById('dinner-suggestions');
    
    let breakfastSuggestions, lunchSuggestions, dinnerSuggestions;
    
    if (userBMICategory === 'Underweight') {
        breakfastSuggestions = [
            '• Oatmeal with nuts and fruits',
            '• Whole grain toast with avocado',
            '• Protein smoothie with banana'
        ];
        lunchSuggestions = [
            '• Quinoa bowl with grilled chicken',
            '• Pasta with lean meat sauce',
            '• Rice with lentils and vegetables'
        ];
        dinnerSuggestions = [
            '• Salmon with sweet potato',
            '• Chicken curry with brown rice',
            '• Lean beef with quinoa'
        ];
    } else if (userBMICategory === 'Normal weight') {
        breakfastSuggestions = [
            '• Greek yogurt with berries',
            '• Eggs with whole grain toast',
            '• Smoothie bowl with granola'
        ];
        lunchSuggestions = [
            '• Grilled chicken salad',
            '• Quinoa and vegetable bowl',
            '• Turkey and avocado wrap'
        ];
        dinnerSuggestions = [
            '• Baked fish with vegetables',
            '• Lean meat with brown rice',
            '• Tofu stir-fry with quinoa'
        ];
    } else if (userBMICategory === 'Overweight' || userBMICategory === 'Obese') {
        breakfastSuggestions = [
            '• Vegetable omelet (2 eggs)',
            '• Greek yogurt with berries',
            '• Green smoothie with protein'
        ];
        lunchSuggestions = [
            '• Large mixed green salad',
            '• Grilled chicken with vegetables',
            '• Lentil soup with side salad'
        ];
        dinnerSuggestions = [
            '• Steamed fish with broccoli',
            '• Grilled chicken breast',
            '• Vegetable curry with cauliflower rice'
        ];
    }
    
    if (breakfast) breakfast.innerHTML = breakfastSuggestions.join('<br>');
    if (lunch) lunch.innerHTML = lunchSuggestions.join('<br>');
    if (dinner) dinner.innerHTML = dinnerSuggestions.join('<br>');
}

// Generate shopping list and PDF
function generateShoppingList() {
    let shoppingItems = [];
    
    if (userBMICategory === 'Underweight') {
        shoppingItems = [
            'Oats', 'Mixed nuts', 'Bananas', 'Avocados', 'Whole grain bread',
            'Quinoa', 'Chicken breast', 'Pasta', 'Lean ground meat',
            'Salmon', 'Sweet potatoes', 'Brown rice', 'Lentils'
        ];
    } else if (userBMICategory === 'Normal weight') {
        shoppingItems = [
            'Greek yogurt', 'Mixed berries', 'Eggs', 'Whole grain bread',
            'Quinoa', 'Mixed vegetables', 'Turkey slices', 'Fish fillets',
            'Brown rice', 'Tofu', 'Lean meat'
        ];
    } else {
        shoppingItems = [
            'Eggs', 'Greek yogurt', 'Mixed berries', 'Leafy greens',
            'Chicken breast', 'Mixed vegetables', 'Lentils', 'Fish fillets',
            'Broccoli', 'Cauliflower', 'Bell peppers', 'Cucumber'
        ];
    }
    
    // Create simple alert for now
    const itemsList = shoppingItems.join(', ');
    alert('Shopping List Generated!\n\nItems needed:\n' + itemsList + '\n\nMeal suggestions have been prepared based on your BMI category: ' + userBMICategory);
}

// Show nutrition tracker
function showNutritionTracker() {
    let dailyTargets = '';
    
    if (userBMICategory === 'Underweight') {
        dailyTargets = 'Calories: 2200-2500\nProtein: 1.2-1.6g per kg body weight\nCarbs: 45-65% of total calories\nFats: 20-35% of total calories';
    } else if (userBMICategory === 'Normal weight') {
        dailyTargets = 'Calories: 1800-2200\nProtein: 1.0-1.2g per kg body weight\nCarbs: 45-65% of total calories\nFats: 20-35% of total calories';
    } else {
        dailyTargets = 'Calories: 1200-1800\nProtein: 1.2-1.5g per kg body weight\nCarbs: 40-50% of total calories\nFats: 20-30% of total calories';
    }
    
    alert('Daily Nutrition Targets:\n\n' + dailyTargets + '\n\nTip: Track your meals to stay within these ranges!');
}

// Back to BMI calculator
function backToBMI() {
    const mealPlanningSection = document.getElementById('meal-planning-section');
    if (mealPlanningSection) {
        mealPlanningSection.classList.add('d-none');
        
        // Scroll back to BMI section
        const bmiSection = document.querySelector('.glass-card');
        if (bmiSection) {
            bmiSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    const bmiInstructions = document.getElementById('bmi-instructions');
    const bmiResult = document.getElementById('bmi-result');
    
    if (bmiInstructions) bmiInstructions.classList.remove('d-none');
    if (bmiResult) bmiResult.classList.add('d-none');
});
