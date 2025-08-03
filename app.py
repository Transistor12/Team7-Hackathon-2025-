from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import requests
import os
from functools import wraps

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SECRET_KEY'] = 'harvestnet-secret-key-2024'

# Database initialization
def init_db():
    conn = sqlite3.connect('harvestnet.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'farmer',
            location TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Weather cache table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            weather_data TEXT NOT NULL,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Platform analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value INTEGER NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin user
    admin_password = hashlib.sha256('password123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, name, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin@harvestnet.com', admin_password, 'Admin User', 'administrator'))
    
    # Insert default farmer user
    farmer_password = hashlib.sha256('password123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, name, role)
        VALUES (?, ?, ?, ?)
    ''', ('farmer@harvestnet.com', farmer_password, 'Farmer User', 'farmer'))
    
    # Insert sample analytics data
    cursor.execute('INSERT OR IGNORE INTO analytics (metric_name, metric_value) VALUES (?, ?)', ('total_users', 1247))
    cursor.execute('INSERT OR IGNORE INTO analytics (metric_name, metric_value) VALUES (?, ?)', ('active_farmers', 892))
    cursor.execute('INSERT OR IGNORE INTO analytics (metric_name, metric_value) VALUES (?, ?)', ('data_ambassadors', 45))
    
    conn.commit()
    conn.close()

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# API Health endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check database connectivity
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check user credentials
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, email, name, role FROM users 
            WHERE email = ? AND password_hash = ? AND is_active = 1
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            
            # Generate JWT token
            token = jwt.encode({
                'user_id': user[0],
                'email': user[1],
                'role': user[3],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            conn.close()
            
            return jsonify({
                'token': token,
                'user': {
                    'id': user[0],
                    'email': user[1],
                    'name': user[2],
                    'role': user[3]
                }
            }), 200
        else:
            conn.close()
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

# User management endpoints
@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    try:
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, email, name, role, location, phone, created_at, last_login, is_active
            FROM users ORDER BY created_at DESC
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'email': row[1],
                'name': row[2],
                'role': row[3],
                'location': row[4],
                'phone': row[5],
                'created_at': row[6],
                'last_login': row[7],
                'is_active': bool(row[8])
            })
        
        conn.close()
        return jsonify({'users': users}), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch users', 'error': str(e)}), 500

# Analytics endpoints
@app.route('/api/analytics/dashboard', methods=['GET'])
@token_required
def get_dashboard_analytics(current_user_id):
    try:
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        
        # Get user counts
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = "farmer" AND is_active = 1')
        active_farmers = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = "data_ambassador" AND is_active = 1')
        data_ambassadors = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_users': total_users,
            'active_farmers': active_farmers,
            'data_ambassadors': data_ambassadors,
            'growth_metrics': {
                'users_growth': '+12% from last month',
                'farmers_growth': '+8% from last month',
                'ambassadors_growth': '+15% from last month'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch analytics', 'error': str(e)}), 500

# Weather API integration
@app.route('/api/weather', methods=['GET'])
@token_required
def get_weather(current_user_id):
    try:
        lat = request.args.get('lat', '-1.2921')  # Default to Nairobi
        lon = request.args.get('lon', '36.8219')
        
        # Check cache first
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT weather_data FROM weather_cache 
            WHERE latitude = ? AND longitude = ? 
            AND datetime(cached_at) > datetime('now', '-1 hour')
        ''', (float(lat), float(lon)))
        
        cached_data = cursor.fetchone()
        
        if cached_data:
            conn.close()
            import json
            return jsonify(json.loads(cached_data[0])), 200
        
        # Fetch from Norwegian Meteorological Institute API
        headers = {
            'User-Agent': 'HarvestNet/1.0 (contact@harvestnet.com)'
        }
        
        url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            weather_data = response.json()
            
            # Cache the data
            import json
            cursor.execute('''
                INSERT INTO weather_cache (latitude, longitude, weather_data)
                VALUES (?, ?, ?)
            ''', (float(lat), float(lon), json.dumps(weather_data)))
            conn.commit()
            conn.close()
            
            return jsonify(weather_data), 200
        else:
            conn.close()
            return jsonify({'message': 'Weather service unavailable'}), 503
            
    except Exception as e:
        return jsonify({'message': 'Failed to fetch weather data', 'error': str(e)}), 500

# Data management endpoints
@app.route('/api/data/export', methods=['GET'])
@token_required
def export_data(current_user_id):
    try:
        data_type = request.args.get('type', 'users')
        
        conn = sqlite3.connect('harvestnet.db')
        cursor = conn.cursor()
        
        if data_type == 'users':
            cursor.execute('SELECT * FROM users')
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
        
        conn.close()
        
        return jsonify({
            'type': data_type,
            'data': data,
            'exported_at': datetime.datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Data export failed', 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

