"""
Proxy Access Portal - A secure web application for agents to access IPRoyal proxy service
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for sessions
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Proxy configuration from things.txt
PROXY_CONFIG = {
    'host': 'geo.iproyal.com',
    'port': 12321,
    'username': 'TmwjTsVQHgTiXElI',
    'password': 'hcu5CmUJHFJqSRFY_country-us',
    'country': 'United States',
    'rotation': 'Randomize IP'
}

# User database (in production, use a real database)
# Password: Each agent can have their own password
USERS = {
    'agent1': generate_password_hash('password123'),
    'agent2': generate_password_hash('password123'),
    'agent3': generate_password_hash('password123'),
    'admin': generate_password_hash('admin123'),
}

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_proxy_dict():
    """Generate proxy dictionary for requests library"""
    proxy_url = f"http://{PROXY_CONFIG['username']}:{PROXY_CONFIG['password']}@{PROXY_CONFIG['host']}:{PROXY_CONFIG['port']}"
    return {
        'http': proxy_url,
        'https': proxy_url
    }

@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for agents"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['username'] = username
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session.permanent = True
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout current user"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for authenticated users"""
    return render_template('dashboard.html', 
                         username=session.get('username'),
                         login_time=session.get('login_time'),
                         proxy_config=PROXY_CONFIG)

@app.route('/api/test-proxy', methods=['POST'])
@login_required
def test_proxy():
    """API endpoint to test the proxy connection"""
    try:
        url = request.json.get('url', 'https://ipv4.icanhazip.com')
        
        # Make request through proxy
        proxies = get_proxy_dict()
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        
        return jsonify({
            'success': True,
            'ip_address': response.text.strip(),
            'status_code': response.status_code,
            'message': 'Proxy connection successful!'
        })
    
    except requests.exceptions.ProxyError as e:
        return jsonify({
            'success': False,
            'error': 'Proxy connection failed',
            'details': str(e)
        }), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': 'Request failed',
            'details': str(e)
        }), 500

@app.route('/api/proxy-request', methods=['POST'])
@login_required
def proxy_request():
    """API endpoint to make custom requests through the proxy"""
    try:
        data = request.json
        url = data.get('url')
        method = data.get('method', 'GET').upper()
        headers = data.get('headers', {})
        body = data.get('body')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Make request through proxy
        proxies = get_proxy_dict()
        
        if method == 'GET':
            response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, proxies=proxies, headers=headers, json=body, timeout=10)
        else:
            return jsonify({
                'success': False,
                'error': f'Method {method} not supported'
            }), 400
        
        return jsonify({
            'success': True,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.text[:1000],  # Limit response size
            'message': 'Request completed successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/proxy-info')
@login_required
def proxy_info():
    """API endpoint to get proxy configuration info"""
    return jsonify({
        'host': PROXY_CONFIG['host'],
        'port': PROXY_CONFIG['port'],
        'username': PROXY_CONFIG['username'],
        'country': PROXY_CONFIG['country'],
        'rotation': PROXY_CONFIG['rotation'],
        # Don't expose the full password in API responses
        'password_hint': PROXY_CONFIG['password'][:4] + '...' + PROXY_CONFIG['password'][-10:]
    })

@app.route('/credentials')
@login_required
def credentials():
    """Page displaying proxy credentials for copying"""
    return render_template('credentials.html',
                         username=session.get('username'),
                         proxy_config=PROXY_CONFIG)

@app.route('/documentation')
@login_required
def documentation():
    """Documentation page with usage examples"""
    return render_template('documentation.html',
                         username=session.get('username'),
                         proxy_config=PROXY_CONFIG)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("Proxy Access Portal Starting...")
    print("="*60)
    print(f"\nProxy Service: {PROXY_CONFIG['host']}:{PROXY_CONFIG['port']}")
    print(f"Location: {PROXY_CONFIG['country']} ({PROXY_CONFIG['rotation']})")
    print("\nAvailable Users:")
    for user in USERS.keys():
        print(f"   - {user}")
    print("\nDefault password for all users: 'password123'")
    print("   (Admin password: 'admin123')")
    print("\nAccess the portal at: http://localhost:5000")
    print("="*60 + "\n")
    
    # Get port from environment variable for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

