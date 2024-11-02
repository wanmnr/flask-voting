# run.py

from app import create_app
from config import DevelopmentConfig, ProductionConfig
import os
from dotenv import load_dotenv
from app.cli import build_assets_command

load_dotenv()  # Load environment variables from .env file

# Use environment variable to switch between configurations
env = os.environ.get('FLASK_ENV', 'development')
config = DevelopmentConfig if env == 'development' else ProductionConfig

app = create_app(config)

if __name__ == '__main__':
    # Build assets when running the app directly
    with app.app_context():
        build_assets_command()
    app.run()
