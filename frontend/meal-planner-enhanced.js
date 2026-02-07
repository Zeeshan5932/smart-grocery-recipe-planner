// Enhanced Meal Planner JavaScript

class MealPlannerWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.userData = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateProgress();
        this.initHealthTracking();
    }

    bindEvents() {
        // Navigation buttons
        document.getElementById('nextBtn').addEventListener('click', () => this.nextStep());
        document.getElementById('prevBtn').addEventListener('click', () => this.prevStep());

        // Health inputs for real-time calculation
        document.getElementById('weight').addEventListener('input', () => this.calculateBMI());
        document.getElementById('height').addEventListener('input', () => this.calculateBMI());
        document.getElementById('bloodSugar').addEventListener('input', () => this.updateHealthIndicators());
        document.getElementById('bpSystolic').addEventListener('input', () => this.updateHealthIndicators());
        document.getElementById('bpDiastolic').addEventListener('input', () => this.updateHealthIndicators());

        // Step indicators
        document.querySelectorAll('.step-indicator').forEach(indicator => {
            indicator.addEventListener('click', (e) => {
                const step = parseInt(e.currentTarget.getAttribute('data-step'));
                if (step <= this.currentStep) {
                    this.goToStep(step);
                }
            });
        });

        // Form validation
        this.setupValidation();
    }

    calculateBMI() {
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);

        if (weight && height) {
            const bmi = weight / ((height / 100) ** 2);
            this.displayBMI(bmi);
            this.updateUserData('bmi', bmi);
        }
    }

    displayBMI(bmi) {
        const bmiDisplay = document.getElementById('bmiDisplay');
        const bmiValue = document.getElementById('bmiValue');
        const bmiStatus = document.getElementById('bmiStatus');

        bmiValue.textContent = bmi.toFixed(1);
        
        let status, color;
        if (bmi < 18.5) {
            status = 'Underweight';
            color = '#17a2b8';
        } else if (bmi < 25) {
            status = 'Normal Weight';
            color = '#28a745';
        } else if (bmi < 30) {
            status = 'Overweight';
            color = '#ffc107';
        } else {
            status = 'Obese';
            color = '#dc3545';
        }

        bmiStatus.textContent = status;
        bmiDisplay.style.background = `linear-gradient(135deg, ${color}, ${this.lightenColor(color, 20)})`;
        bmiDisplay.style.display = 'block';
        bmiDisplay.classList.add('animate__animated', 'animate__bounceIn');
    }

    updateHealthIndicators() {
        const bloodSugar = parseFloat(document.getElementById('bloodSugar').value);
        const systolic = parseFloat(document.getElementById('bpSystolic').value);
        const diastolic = parseFloat(document.getElementById('bpDiastolic').value);

        // Blood sugar indicator
        if (bloodSugar) {
            const sugarIndicator = document.getElementById('sugarIndicator');
            if (bloodSugar < 100) {
                sugarIndicator.className = 'health-indicator normal';
            } else if (bloodSugar < 140) {
                sugarIndicator.className = 'health-indicator warning';
            } else {
                sugarIndicator.className = 'health-indicator danger';
            }
        }

        // Blood pressure validation
        if (systolic && diastolic) {
            this.validateBloodPressure(systolic, diastolic);
        }
    }

    validateBloodPressure(systolic, diastolic) {
        const isNormal = systolic <= 120 && diastolic <= 80;
        const isElevated = systolic <= 139 && diastolic <= 89;
        
        // Visual feedback could be added here
        if (!isNormal && !isElevated) {
            this.showAlert('warning', 'Blood pressure readings seem high. Consider consulting a healthcare provider.');
        }
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.updateWizard();
            } else {
                this.generateMealPlan();
            }
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateWizard();
        }
    }

    goToStep(step) {
        this.currentStep = step;
        this.updateWizard();
    }

    updateWizard() {
        this.updateProgress();
        this.updateStepVisibility();
        this.updateNavigation();
    }

    updateProgress() {
        // Update step indicators
        document.querySelectorAll('.step-indicator').forEach((indicator, index) => {
            const stepNumber = index + 1;
            indicator.classList.remove('active', 'completed');
            
            if (stepNumber === this.currentStep) {
                indicator.classList.add('active');
            } else if (stepNumber < this.currentStep) {
                indicator.classList.add('completed');
                indicator.innerHTML = '<i class="fas fa-check"></i><span>' + indicator.querySelector('span').textContent + '</span>';
            }
        });
    }

    updateStepVisibility() {
        document.querySelectorAll('.wizard-step').forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'slide-in-left', 'slide-in-right');
            
            if (stepNumber === this.currentStep) {
                step.classList.add('active');
                
                // Add appropriate slide animation
                if (stepNumber > 1) {
                    step.classList.add('slide-in-right');
                } else {
                    step.classList.add('slide-in-left');
                }
            }
        });
    }

    updateNavigation() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        // Previous button
        if (this.currentStep === 1) {
            prevBtn.style.visibility = 'hidden';
        } else {
            prevBtn.style.visibility = 'visible';
        }

        // Next button
        if (this.currentStep === this.totalSteps) {
            nextBtn.innerHTML = '<i class="fas fa-utensils"></i> Generate Meal Plan';
            nextBtn.classList.add('btn-success');
            nextBtn.classList.remove('btn-primary');
        } else {
            nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
            nextBtn.classList.add('btn-primary');
            nextBtn.classList.remove('btn-success');
        }
    }

    validateCurrentStep() {
        switch (this.currentStep) {
            case 1:
                return this.validateHealthStep();
            case 2:
                return this.validatePreferencesStep();
            case 3:
                return this.validateGoalsStep();
            default:
                return true;
        }
    }

    validateHealthStep() {
        const required = ['weight', 'height', 'bloodSugar', 'bpSystolic', 'bpDiastolic'];
        const missing = required.filter(id => !document.getElementById(id).value);

        if (missing.length > 0) {
            this.showAlert('error', 'Please fill in all health information fields.');
            this.highlightMissingFields(missing);
            return false;
        }

        // Validate ranges
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const bloodSugar = parseFloat(document.getElementById('bloodSugar').value);

        if (weight < 30 || weight > 200) {
            this.showAlert('error', 'Please enter a valid weight between 30-200 kg.');
            return false;
        }

        if (height < 100 || height > 250) {
            this.showAlert('error', 'Please enter a valid height between 100-250 cm.');
            return false;
        }

        if (bloodSugar < 70 || bloodSugar > 400) {
            this.showAlert('error', 'Please enter a valid blood sugar level between 70-400 mg/dL.');
            return false;
        }

        // Store health data
        this.updateUserData('health', {
            weight: weight,
            height: height,
            bloodSugar: bloodSugar,
            bloodPressure: {
                systolic: document.getElementById('bpSystolic').value,
                diastolic: document.getElementById('bpDiastolic').value
            },
            dietaryRestrictions: this.getDietaryRestrictions()
        });

        return true;
    }

    validatePreferencesStep() {
        // This would validate step 2 when implemented
        return true;
    }

    validateGoalsStep() {
        // This would validate step 3 when implemented
        return true;
    }

    highlightMissingFields(fields) {
        fields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            field.classList.add('is-invalid');
            field.addEventListener('input', () => {
                field.classList.remove('is-invalid');
            }, { once: true });
        });
    }

    getDietaryRestrictions() {
        const restrictions = [];
        document.querySelectorAll('.pill-input:checked').forEach(input => {
            restrictions.push(input.value || input.id);
        });
        return restrictions;
    }

    updateUserData(key, value) {
        this.userData[key] = value;
        console.log('User data updated:', this.userData);
    }

    generateMealPlan() {
        this.showLoadingOverlay();
        
        // Simulate API call
        setTimeout(() => {
            this.hideLoadingOverlay();
            this.displayMealPlan(this.generateSamplePlan());
        }, 2000);
    }

    generateSamplePlan() {
        const { health } = this.userData;
        const bmi = health.weight / ((health.height / 100) ** 2);
        
        return {
            summary: {
                bmi: bmi.toFixed(1),
                healthScore: this.calculateHealthScore(),
                recommendations: this.getHealthRecommendations()
            },
            meals: this.generateWeeklyMeals()
        };
    }

    calculateHealthScore() {
        const { health } = this.userData;
        let score = 100;
        
        // BMI impact
        const bmi = health.weight / ((health.height / 100) ** 2);
        if (bmi < 18.5 || bmi > 30) score -= 20;
        else if (bmi > 25) score -= 10;
        
        // Blood sugar impact
        if (health.bloodSugar > 140) score -= 20;
        else if (health.bloodSugar > 100) score -= 10;
        
        // Blood pressure impact
        if (health.bloodPressure.systolic > 140 || health.bloodPressure.diastolic > 90) score -= 20;
        else if (health.bloodPressure.systolic > 120 || health.bloodPressure.diastolic > 80) score -= 10;
        
        return Math.max(score, 0);
    }

    getHealthRecommendations() {
        const recommendations = [];
        const { health } = this.userData;
        const bmi = health.weight / ((health.height / 100) ** 2);
        
        if (bmi > 25) {
            recommendations.push('Focus on portion control and low-calorie options');
        }
        
        if (health.bloodSugar > 100) {
            recommendations.push('Choose low-glycemic index foods');
        }
        
        if (health.bloodPressure.systolic > 120) {
            recommendations.push('Reduce sodium intake');
        }
        
        return recommendations;
    }

    generateWeeklyMeals() {
        // This would generate actual meal plans based on user data
        const sampleMeals = {
            monday: {
                breakfast: 'Oatmeal with berries and nuts',
                lunch: 'Grilled chicken salad',
                dinner: 'Baked salmon with vegetables'
            },
            tuesday: {
                breakfast: 'Greek yogurt with fruits',
                lunch: 'Quinoa bowl with vegetables',
                dinner: 'Lean beef stir-fry'
            }
            // ... more days
        };
        
        return sampleMeals;
    }

    displayMealPlan(plan) {
        // Create and show meal plan modal or redirect to results page
        console.log('Generated meal plan:', plan);
        this.showAlert('success', 'Your personalized meal plan has been generated!');
    }

    showLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
                <h4 class="mt-3">Generating Your Meal Plan</h4>
                <p>Analyzing your health data and preferences...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    hideLoadingOverlay() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.remove();
        }
    }

    showAlert(type, message) {
        // Remove existing alerts
        document.querySelectorAll('.alert-custom').forEach(alert => alert.remove());
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-custom alert-dismissible fade show`;
        alertDiv.style.cssText = `
            position: fixed;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
        `;
        
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    setupValidation() {
        // Add real-time validation styles
        const style = document.createElement('style');
        style.textContent = `
            .is-invalid {
                border-color: #dc3545 !important;
                box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
            }
            
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            
            .loading-content {
                background: white;
                padding: 3rem;
                border-radius: 20px;
                text-align: center;
                max-width: 400px;
            }
        `;
        document.head.appendChild(style);
    }

    initHealthTracking() {
        // Set up real-time health tracking
        this.calculateBMI();
        this.updateHealthIndicators();
    }

    lightenColor(color, percent) {
        const num = parseInt(color.replace("#", ""), 16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) + amt;
        const B = (num >> 8 & 0x00FF) + amt;
        const G = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (B < 255 ? B < 1 ? 0 : B : 255) * 0x100 + (G < 255 ? G < 1 ? 0 : G : 255)).toString(16).slice(1);
    }
}

// Global functions for external access
window.fillSampleData = function() {
    document.getElementById('weight').value = 70;
    document.getElementById('height').value = 170;
    document.getElementById('bloodSugar').value = 95;
    document.getElementById('bpSystolic').value = 120;
    document.getElementById('bpDiastolic').value = 80;
    
    // Trigger calculations
    wizard.calculateBMI();
    wizard.updateHealthIndicators();
    
    wizard.showAlert('info', 'Sample data filled! You can modify the values as needed.');
};

window.saveAsDraft = function() {
    const draftData = {
        ...wizard.userData,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('mealPlannerDraft', JSON.stringify(draftData));
    wizard.showAlert('success', 'Progress saved as draft!');
};

window.clearForm = function() {
    if (confirm('Are you sure you want to clear all form data?')) {
        document.querySelectorAll('input').forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        
        document.getElementById('bmiDisplay').style.display = 'none';
        wizard.currentStep = 1;
        wizard.userData = {};
        wizard.updateWizard();
        
        wizard.showAlert('info', 'Form cleared successfully!');
    }
};

// Initialize the wizard when the page loads
let wizard;
document.addEventListener('DOMContentLoaded', function() {
    wizard = new MealPlannerWizard();
    
    // Load draft if exists
    const draft = localStorage.getItem('mealPlannerDraft');
    if (draft) {
        const draftData = JSON.parse(draft);
        if (confirm('Found a saved draft. Would you like to load it?')) {
            // Load draft data (implementation would go here)
            wizard.showAlert('info', 'Draft loaded successfully!');
        }
    }
});
