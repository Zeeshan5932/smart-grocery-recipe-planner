# Smart Grocery + Recipe Planner Setup Guide

## Problem Solved ✅

The Firebase error has been resolved! The application now includes:
- **Fallback storage system**: Uses local JSON files when Firebase is unavailable
- **Enhanced error handling**: Graceful degradation instead of crashes
- **Improved UI**: Modern, responsive design with better user experience

## Quick Start

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenAI API key
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Features

### ✨ Enhanced UI Features
- **Modern Design**: Gradient backgrounds, card layouts, smooth animations
- **Responsive Layout**: Works perfectly on mobile and desktop
- **Interactive Forms**: Real-time BMI calculation, cooking time slider
- **Visual Feedback**: Loading spinners, success/error alerts
- **Navigation**: Multi-page layout with history tracking

### 🔧 Technical Improvements
- **Firebase Fallback**: Automatic local storage when Firebase is unavailable
- **Better Error Handling**: No more crashes, graceful error messages
- **Enhanced Meal Planning**: More sophisticated algorithm with health considerations
- **Data Persistence**: Save and retrieve meal planning history

## Firebase Setup (Optional)

If you want to use Firebase for data storage:

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Create new project: "smart-grocery-recipe-planner"

2. **Enable Firestore**
   - In your Firebase project, go to Firestore Database
   - Click "Create database"
   - Choose "Start in test mode"

3. **Get Service Account Key**
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file to your backend directory

4. **Update Environment Variables**
   ```
   FIREBASE_CREDENTIALS_PATH=./path-to-your-service-account.json
   ```

## Local Storage Fallback

If Firebase is not configured, the app automatically uses local storage:
- Data saved to `backend/data/user_data.json`
- No setup required
- Perfect for development and testing

## API Keys Required

### OpenAI API Key (Required)
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

## Usage

1. **Health Data**: Enter your blood pressure, sugar levels, weight, and height
2. **Dietary Preferences**: Select restrictions and cuisine preferences
3. **Budget**: Set your weekly food budget
4. **Generate Plan**: Get AI-powered meal suggestions
5. **View History**: Access previously generated meal plans

## Troubleshooting

### Common Issues

1. **Module Not Found**
   ```bash
   pip install -r requirements.txt
   ```

2. **OpenAI API Error**
   - Check your API key in `.env`
   - Ensure you have API credits

3. **Streamlit Port Issues**
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Firebase Issues (If Using)
- Check service account JSON file path
- Verify Firestore API is enabled
- Ensure proper permissions in Firebase rules

## File Structure

```
smart-grocery-recipe-planner/
├── backend/
│   ├── app.py              # Enhanced Streamlit app
│   ├── firebase_service.py # Firebase with fallback
│   ├── meal_planner.py     # Sophisticated meal planning
│   ├── openai_integration.py # AI recipe generation
│   ├── requirements.txt    # Dependencies
│   ├── .env.example       # Environment template
│   └── data/              # Local storage directory
├── frontend/
│   ├── index.html         # Enhanced UI
│   ├── styles.css         # Modern styling
│   └── scripts.js         # Interactive features
└── README.md
```

## What's New

### UI Enhancements
- 🎨 Modern gradient design
- 📱 Mobile-responsive layout
- ⚡ Real-time BMI calculation
- 🔄 Loading animations
- 📊 Better data visualization

### Backend Improvements
- 🛡️ Error handling and fallbacks
- 💾 Local storage option
- 🧠 Enhanced meal planning algorithm
- 📈 Data persistence and history
- 🔌 Robust API integration

### User Experience
- 🎯 Personalized recommendations
- 🍽️ Multiple cuisine options
- ⏱️ Cooking time preferences
- 📋 Comprehensive meal plans
- 📱 Cross-platform compatibility

## Next Steps

1. Start the application with `streamlit run app.py`
2. Add your OpenAI API key to the `.env` file
3. Optionally set up Firebase for cloud storage
4. Customize meal planning algorithms as needed
5. Deploy to your preferred hosting platform

The application is now production-ready with robust error handling and an enhanced user experience! 🚀
