# Firebase integration (for storing user data)
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase with error handling
db = None
firebase_enabled = False

try:
    # Check if service account file exists
    credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./service.json")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Firebase credentials file not found: {credentials_path}")
    
    cred = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(cred, {
        'projectId': 'smart-grocery-recipe-planner',
    })
    db = firestore.client()
    firebase_enabled = True
    print("✅ Firebase initialized successfully")
    print(f"📁 Project ID: smart-grocery-recipe-planner")
    
    # Test connection
    test_doc = db.collection('test').document('connection_test')
    test_doc.set({'timestamp': datetime.now(), 'status': 'connected'})
    print("✅ Firebase connection test successful")
    
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    print("📝 Falling back to local JSON storage")
    print("💡 To fix Firebase:")
    print("   1. Go to https://console.firebase.google.com/")
    print("   2. Select your project: smart-grocery-recipe-planner")
    print("   3. Enable Firestore Database in the console")
    firebase_enabled = False

def save_user_data(health_data, meal_plan, recipe_suggestions):
    """Save user data to Firebase or local storage as fallback"""
    data = {
        'health_data': health_data,
        'meal_plan': meal_plan,
        'recipe_suggestions': recipe_suggestions,
        'timestamp': datetime.now().isoformat()
    }
    
    if firebase_enabled and db:
        try:
            # Save to Firebase
            doc_ref = db.collection('user_data').add(data)
            print(f"Data saved to Firebase with ID: {doc_ref[1].id}")
            return {"status": "success", "storage": "firebase", "id": doc_ref[1].id}
        except Exception as e:
            print(f"Firebase save failed: {e}")
            print("Falling back to local storage")
            return save_to_local_storage(data)
    else:
        return save_to_local_storage(data)

def save_to_local_storage(data):
    """Save data to local JSON file as fallback"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Load existing data or create new list
        file_path = 'data/user_data.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Add new data
        data['id'] = len(existing_data) + 1
        existing_data.append(data)
        
        # Save back to file
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        print(f"Data saved to local storage with ID: {data['id']}")
        return {"status": "success", "storage": "local", "id": data['id']}
    except Exception as e:
        print(f"Local storage save failed: {e}")
        return {"status": "error", "message": str(e)}

def get_user_data():
    """Retrieve all user data from Firebase or local storage"""
    if firebase_enabled and db:
        try:
            docs = db.collection('user_data').stream()
            return [{"id": doc.id, **doc.to_dict()} for doc in docs]
        except Exception as e:
            print(f"Firebase read failed: {e}")
            return get_from_local_storage()
    else:
        return get_from_local_storage()

def get_from_local_storage():
    """Get data from local JSON file"""
    try:
        file_path = 'data/user_data.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Local storage read failed: {e}")
        return []
