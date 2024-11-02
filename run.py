# run.py

from app import create_app
from config import DevelopmentConfig, ProductionConfig
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Use environment variable to switch between configurations
env = os.environ.get('FLASK_ENV', 'development')
config = DevelopmentConfig if env == 'development' else ProductionConfig

app = create_app()
app.config.from_object(config)

if __name__ == '__main__':
    app.run()
