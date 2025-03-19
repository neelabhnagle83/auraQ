"""
Simple script to run the AuroQ backend server
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import flask_bcrypt
        import flask_jwt_extended
        import textblob
        import google.generativeai
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install missing dependencies from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please install them manually.")
        sys.exit(1)

def setup_environment():
    """Setup environment for the application"""
    routes_dir = os.path.join(os.path.dirname(__file__), 'routes')
    if not os.path.exists(routes_dir):
        os.makedirs(routes_dir)
        print(f"Created routes directory at: {routes_dir}")
    
    init_file = os.path.join(routes_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write("# routes package initialization\n")
        print(f"Created {init_file}")

if __name__ == "__main__":
    print("Starting AuroQ Backend Setup")
    
    if not check_dependencies():
        print("Dependencies missing. Installing now...")
        install_dependencies()

    setup_environment()
    
    print("Starting Flask server...")
    subprocess.run([sys.executable, "app.py"], check=True)

def handler(event, context):
    from run import app
    return app(event, context)
