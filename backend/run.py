"""
Simple script to run the AuroQ backend server
"""
import os
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import flask_bcrypt
        import flask_jwt_extended
        import textblob
        import google.generativeai  # Added Google Generative AI check
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def setup_environment():
    """Setup environment for the application"""
    # Create routes directory if it doesn't exist
    routes_dir = os.path.join(os.path.dirname(__file__), 'routes')
    if not os.path.exists(routes_dir):
        os.makedirs(routes_dir)
        print(f"Created routes directory at: {routes_dir}")
    
    # Create __init__.py in routes directory if it doesn't exist
    init_file = os.path.join(routes_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write("# routes package initialization\n")
        print(f"Created {init_file}")

def install_dependencies():
    """Install missing dependencies"""
    print("Installing dependencies...")
    os.system(f"{sys.executable} -m pip install flask flask-cors flask-bcrypt flask-jwt-extended textblob google-generativeai")

if __name__ == "__main__":
    print("Starting AuroQ Backend Setup")
    
    setup_environment()
    
    if not check_dependencies():
        print("Some dependencies are missing. Installing them now...")
        install_dependencies()
        if not check_dependencies():
            print("Failed to install all dependencies. Please install them manually.")
            print("Run: pip install flask flask-cors flask-bcrypt flask-jwt-extended textblob google-generativeai")
            sys.exit(1)
    
    # Run the Flask app
    print("Starting Flask server...")
    os.system(f"{sys.executable} app.py")
