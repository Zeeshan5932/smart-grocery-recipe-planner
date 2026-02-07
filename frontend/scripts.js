// Enhanced JavaScript for Smart Grocery + Recipe Planner

// Update cooking time display
document.getElementById('cookingTime').addEventListener('input', function() {
    document.getElementById('timeValue').textContent = this.value;
});

// Calculate and display BMI
function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    
    if (weight && height) {
        const bmi = weight / ((height / 100) ** 2);
        const bmiDisplay = document.getElementById('bmiDisplay');
        
        if (!bmiDisplay) {
            // Create BMI display element
            const bmiDiv = document.createElement('div');
            bmiDiv.id = 'bmiDisplay';
            bmiDiv.className = 'alert alert-info mt-2';
            document.getElementById('weight').parentNode.appendChild(bmiDiv);
        }
        
        let bmiCategory = '';
        let alertClass = 'alert-info';
        
        if (bmi < 18.5) {
            bmiCategory = 'Underweight';
            alertClass = 'alert-warning';
        } else if (bmi < 25) {
            bmiCategory = 'Normal weight';
            alertClass = 'alert-success';
        } else if (bmi < 30) {
            bmiCategory = 'Overweight';
            alertClass = 'alert-warning';
        } else {
            bmiCategory = 'Obese';
            alertClass = 'alert-danger';
        }
        
        document.getElementById('bmiDisplay').className = `alert ${alertClass} mt-2`;
        document.getElementById('bmiDisplay').innerHTML = 
            `<strong>BMI: ${bmi.toFixed(1)}</strong> - ${bmiCategory}`;
    }
}

// Add event listeners for BMI calculation
document.getElementById('weight').addEventListener('input', calculateBMI);
document.getElementById('height').addEventListener('input', calculateBMI);

// Form submission handler
document.getElementById('generateBtn').addEventListener('click', function(event) {
    event.preventDefault();
    
    // Show loading spinner
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    
    // Collect form data
    const formData = collectFormData();
    
    // Validate form data
    if (!validateFormData(formData)) {
        document.getElementById('loading').style.display = 'none';
        return;
    }
    
    // Simulate API call (replace with actual backend integration)
    simulateAPICall(formData);
});

function collectFormData() {
    // Health data
    const bpSystolic = document.getElementById('bpSystolic').value;
    const bpDiastolic = document.getElementById('bpDiastolic').value;
    const bloodSugar = document.getElementById('bloodSugar').value;
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;
    
    // Dietary restrictions
    const dietaryRestrictions = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
        if (['vegetarian', 'vegan', 'glutenFree', 'diabetic'].includes(checkbox.id)) {
            dietaryRestrictions.push(checkbox.value);
        }
    });
    
    // Meal preferences
    const budget = document.getElementById('budget').value;
    const cuisine = document.getElementById('cuisine').value;
    const cookingTime = document.getElementById('cookingTime').value;
    
    // Meal types
    const mealTypes = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
        if (['breakfast', 'lunch', 'dinner', 'snacks'].includes(checkbox.id)) {
            mealTypes.push(checkbox.value);
        }
    });
    
    return {
        healthData: {
            bloodPressure: `${bpSystolic}/${bpDiastolic}`,
            bloodSugar: bloodSugar,
            weight: weight,
            height: height,
            bmi: weight && height ? (weight / ((height / 100) ** 2)).toFixed(1) : null,
            dietaryRestrictions: dietaryRestrictions
        },
        preferences: {
            budget: budget,
            cuisine: cuisine,
            cookingTime: cookingTime,
            mealTypes: mealTypes
        }
    };
}

function validateFormData(data) {
    const errors = [];
    
    // Check required fields
    if (!data.healthData.weight) errors.push('Weight is required');
    if (!data.healthData.height) errors.push('Height is required');
    if (!data.preferences.budget) errors.push('Budget is required');
    if (data.preferences.mealTypes.length === 0) errors.push('Select at least one meal type');
    
    // Check value ranges
    if (data.healthData.bloodSugar && (data.healthData.bloodSugar < 70 || data.healthData.bloodSugar > 400)) {
        errors.push('Blood sugar should be between 70-400 mg/dL');
    }
    
    if (errors.length > 0) {
        showAlert('error', 'Please fix the following errors:<br>• ' + errors.join('<br>• '));
        return false;
    }
    
    return true;
}

function simulateAPICall(formData) {
    // Simulate API processing time
    setTimeout(() => {
        // Hide loading spinner
        document.getElementById('loading').style.display = 'none';
        
        // Generate sample meal plan (in real app, this would come from backend)
        const mealPlan = generateSampleMealPlan(formData);
        
        // Display results
        displayResults(mealPlan);
        
        // Show success message
        showAlert('success', 'Your personalized meal plan has been generated successfully!');
        
        // Scroll to results
        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
        
    }, 2000); // 2 second delay to simulate processing
}

function generateSampleMealPlan(formData) {
    const { healthData, preferences } = formData;
    
    // Sample meal plan based on preferences
    let plan = `
        <div class="result-card">
            <h3><i class="fas fa-utensils"></i> Your Personalized 7-Day Meal Plan</h3>
            <p><strong>Based on:</strong> BMI ${healthData.bmi}, Budget $${preferences.budget}/week, ${preferences.cuisine} cuisine</p>
            
            <div class="row">
                <div class="col-md-6">
                    <h5>Health Considerations:</h5>
                    <ul>
                        ${healthData.bmi > 25 ? '<li>Weight management focus</li>' : ''}
                        ${healthData.bloodSugar > 140 ? '<li>Low sugar options</li>' : ''}
                        ${healthData.dietaryRestrictions.map(r => `<li>${r} meals</li>`).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5>Meal Schedule:</h5>
                    <ul>
                        ${preferences.mealTypes.map(meal => `<li>${meal}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    // Add daily meal suggestions
    for (let day = 1; day <= 7; day++) {
        plan += `
            <div class="meal-plan-item">
                <h6><i class="fas fa-calendar-day"></i> Day ${day}</h6>
                ${preferences.mealTypes.includes('Breakfast') ? `<p><strong>Breakfast:</strong> ${getSampleMeal('breakfast', preferences.cuisine)}</p>` : ''}
                ${preferences.mealTypes.includes('Lunch') ? `<p><strong>Lunch:</strong> ${getSampleMeal('lunch', preferences.cuisine)}</p>` : ''}
                ${preferences.mealTypes.includes('Dinner') ? `<p><strong>Dinner:</strong> ${getSampleMeal('dinner', preferences.cuisine)}</p>` : ''}
                ${preferences.mealTypes.includes('Snacks') ? `<p><strong>Snack:</strong> ${getSampleMeal('snack', preferences.cuisine)}</p>` : ''}
            </div>
        `;
    }
    
    // Add budget tips
    plan += `
        <div class="result-card">
            <h5><i class="fas fa-lightbulb"></i> Budget Tips</h5>
            <p>${getBudgetTip(preferences.budget)}</p>
        </div>
    `;
    
    return plan;
}

function getSampleMeal(type, cuisine) {
    const meals = {
        'Mediterranean': {
            breakfast: ['Greek yogurt with honey and nuts', 'Whole grain toast with olive oil', 'Mediterranean omelet'],
            lunch: ['Greek salad with grilled chicken', 'Hummus and vegetable wrap', 'Lentil soup'],
            dinner: ['Grilled fish with roasted vegetables', 'Chicken souvlaki', 'Mediterranean pasta'],
            snack: ['Mixed nuts', 'Greek yogurt', 'Fresh fruit']
        },
        'Asian': {
            breakfast: ['Congee with vegetables', 'Miso soup with tofu', 'Green tea and rice cakes'],
            lunch: ['Stir-fried vegetables with brown rice', 'Miso glazed salmon', 'Vegetable sushi'],
            dinner: ['Steamed fish with ginger', 'Vegetable curry', 'Grilled chicken teriyaki'],
            snack: ['Edamame', 'Green tea', 'Seaweed snacks']
        },
        'No Preference': {
            breakfast: ['Oatmeal with fresh fruits', 'Scrambled eggs with vegetables', 'Whole grain cereal'],
            lunch: ['Grilled chicken salad', 'Quinoa bowl', 'Turkey wrap'],
            dinner: ['Baked salmon with sweet potato', 'Lean beef stir-fry', 'Vegetable pasta'],
            snack: ['Apple with almond butter', 'Greek yogurt', 'Handful of nuts']
        }
    };
    
    const cuisineMeals = meals[cuisine] || meals['No Preference'];
    const mealOptions = cuisineMeals[type] || cuisineMeals.breakfast;
    
    return mealOptions[Math.floor(Math.random() * mealOptions.length)];
}

function getBudgetTip(budget) {
    if (budget < 50) {
        return 'Focus on affordable proteins like eggs, beans, and chicken. Buy seasonal vegetables for better prices.';
    } else if (budget < 100) {
        return 'You have flexibility for variety including fish, lean meats, and diverse vegetables.';
    } else {
        return 'Consider organic options and premium ingredients for optimal nutrition.';
    }
}

function displayResults(mealPlan) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = mealPlan;
    resultDiv.style.display = 'block';
}

function showAlert(type, message) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.custom-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} custom-alert`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Insert alert at the top of the container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set default values
    document.getElementById('bpSystolic').value = 120;
    document.getElementById('bpDiastolic').value = 80;
    document.getElementById('bloodSugar').value = 100;
    document.getElementById('weight').value = 70;
    document.getElementById('height').value = 170;
    document.getElementById('budget').value = 100;
    
    // Calculate initial BMI
    calculateBMI();
    
    // Show welcome message
    setTimeout(() => {
        showAlert('info', 'Welcome! Fill in your health data and preferences to get a personalized meal plan.');
    }, 1000);
});
