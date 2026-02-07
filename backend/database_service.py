# Enhanced Database Service with multiple database support
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class DatabaseService:
    def __init__(self, db_path: str = "data/smart_grocery.db"):
        """Initialize database service with SQLite as primary and JSON as fallback"""
        self.db_path = db_path
        self.json_path = "data/user_data.json"
        self.init_sqlite_db()
    
    def init_sqlite_db(self):
        """Initialize SQLite database with required tables"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        age INTEGER,
                        weight REAL,
                        height REAL,
                        activity_level TEXT,
                        dietary_preferences TEXT,
                        health_goals TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create meal_plans table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS meal_plans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        plan_name TEXT,
                        plan_data TEXT,  -- JSON string
                        calories_target INTEGER,
                        budget_limit REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Create recipes table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        ingredients TEXT,  -- JSON string
                        instructions TEXT,
                        calories_per_serving INTEGER,
                        prep_time INTEGER,
                        cook_time INTEGER,
                        difficulty_level TEXT,
                        cuisine_type TEXT,
                        dietary_tags TEXT,  -- JSON string
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create grocery_lists table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS grocery_lists (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        meal_plan_id INTEGER,
                        items TEXT,  -- JSON string
                        estimated_cost REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (meal_plan_id) REFERENCES meal_plans (id)
                    )
                ''')
                
                # Create health_tracking table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS health_tracking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        date DATE,
                        weight REAL,
                        calories_consumed INTEGER,
                        exercise_minutes INTEGER,
                        water_intake REAL,
                        sleep_hours REAL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                conn.commit()
                print("✅ SQLite database initialized successfully")
                print(f"📁 Database location: {self.db_path}")
                
        except Exception as e:
            print(f"❌ SQLite initialization failed: {e}")
            print("📝 Falling back to JSON storage")
    
    def save_user_profile(self, user_data: Dict) -> Dict:
        """Save or update user profile"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.get('email', ''),))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    # Update existing user
                    cursor.execute('''
                        UPDATE users SET 
                        name=?, age=?, weight=?, height=?, activity_level=?, 
                        dietary_preferences=?, health_goals=?, updated_at=?
                        WHERE email=?
                    ''', (
                        user_data.get('name', ''),
                        user_data.get('age', 0),
                        user_data.get('weight', 0),
                        user_data.get('height', 0),
                        user_data.get('activity_level', ''),
                        json.dumps(user_data.get('dietary_preferences', [])),
                        json.dumps(user_data.get('health_goals', [])),
                        datetime.now(),
                        user_data.get('email', '')
                    ))
                    user_id = existing_user[0]
                else:
                    # Insert new user
                    cursor.execute('''
                        INSERT INTO users (name, email, age, weight, height, activity_level, 
                                         dietary_preferences, health_goals)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_data.get('name', ''),
                        user_data.get('email', ''),
                        user_data.get('age', 0),
                        user_data.get('weight', 0),
                        user_data.get('height', 0),
                        user_data.get('activity_level', ''),
                        json.dumps(user_data.get('dietary_preferences', [])),
                        json.dumps(user_data.get('health_goals', []))
                    ))
                    user_id = cursor.lastrowid
                
                conn.commit()
                return {"status": "success", "user_id": user_id, "storage": "sqlite"}
                
        except Exception as e:
            print(f"SQLite save failed: {e}")
            return self._save_to_json(user_data)
    
    def save_meal_plan(self, user_id: int, meal_plan_data: Dict) -> Dict:
        """Save meal plan to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO meal_plans (user_id, plan_name, plan_data, calories_target, budget_limit)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    meal_plan_data.get('name', f"Plan_{datetime.now().strftime('%Y%m%d_%H%M')}"),
                    json.dumps(meal_plan_data),
                    meal_plan_data.get('calories_target', 0),
                    meal_plan_data.get('budget_limit', 0)
                ))
                
                plan_id = cursor.lastrowid
                conn.commit()
                
                return {"status": "success", "plan_id": plan_id, "storage": "sqlite"}
                
        except Exception as e:
            print(f"SQLite meal plan save failed: {e}")
            return self._save_to_json(meal_plan_data)
    
    def get_user_profile(self, email: str) -> Optional[Dict]:
        """Retrieve user profile by email"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable dict-like access
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()
                
                if user:
                    user_dict = dict(user)
                    # Parse JSON fields
                    user_dict['dietary_preferences'] = json.loads(user_dict.get('dietary_preferences', '[]'))
                    user_dict['health_goals'] = json.loads(user_dict.get('health_goals', '[]'))
                    return user_dict
                
                return None
                
        except Exception as e:
            print(f"SQLite user retrieval failed: {e}")
            return self._get_from_json()
    
    def get_meal_plans(self, user_id: int) -> List[Dict]:
        """Get all meal plans for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM meal_plans 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                plans = cursor.fetchall()
                result = []
                
                for plan in plans:
                    plan_dict = dict(plan)
                    plan_dict['plan_data'] = json.loads(plan_dict.get('plan_data', '{}'))
                    result.append(plan_dict)
                
                return result
                
        except Exception as e:
            print(f"SQLite meal plans retrieval failed: {e}")
            return self._get_from_json()
    
    def save_health_tracking(self, user_id: int, health_data: Dict) -> Dict:
        """Save daily health tracking data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if entry exists for today
                today = datetime.now().date()
                cursor.execute('''
                    SELECT id FROM health_tracking 
                    WHERE user_id = ? AND date = ?
                ''', (user_id, today))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing entry
                    cursor.execute('''
                        UPDATE health_tracking SET 
                        weight=?, calories_consumed=?, exercise_minutes=?, 
                        water_intake=?, sleep_hours=?, notes=?
                        WHERE user_id=? AND date=?
                    ''', (
                        health_data.get('weight'),
                        health_data.get('calories_consumed'),
                        health_data.get('exercise_minutes'),
                        health_data.get('water_intake'),
                        health_data.get('sleep_hours'),
                        health_data.get('notes', ''),
                        user_id,
                        today
                    ))
                else:
                    # Insert new entry
                    cursor.execute('''
                        INSERT INTO health_tracking 
                        (user_id, date, weight, calories_consumed, exercise_minutes, 
                         water_intake, sleep_hours, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id,
                        today,
                        health_data.get('weight'),
                        health_data.get('calories_consumed'),
                        health_data.get('exercise_minutes'),
                        health_data.get('water_intake'),
                        health_data.get('sleep_hours'),
                        health_data.get('notes', '')
                    ))
                
                conn.commit()
                return {"status": "success", "storage": "sqlite"}
                
        except Exception as e:
            print(f"SQLite health tracking save failed: {e}")
            return self._save_to_json(health_data)
    
    def _save_to_json(self, data: Dict) -> Dict:
        """Fallback JSON storage"""
        try:
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            data['id'] = len(existing_data) + 1
            data['timestamp'] = datetime.now().isoformat()
            existing_data.append(data)
            
            with open(self.json_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            return {"status": "success", "storage": "json", "id": data['id']}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_from_json(self) -> List[Dict]:
        """Fallback JSON retrieval"""
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"JSON retrieval failed: {e}")
            return []
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                tables = ['users', 'meal_plans', 'recipes', 'grocery_lists', 'health_tracking']
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats[table] = count
                
                stats['database_size'] = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                stats['status'] = "connected"
                
                return stats
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global database instance
db_service = DatabaseService()
