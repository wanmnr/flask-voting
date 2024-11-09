# run.py

import os
from pathlib import Path
from dotenv import load_dotenv
from app.config import configs
from app import create_app
from app.utils.logger import setup_logging, get_logger

# Load environment variables
def load_environment():
    # Get logger inside the function
    logger = get_logger()

    env_path = Path('.') / '.env'
    flask_env_path = Path('.') / '.flaskenv'

    logger.debug(f"Loading environment from: {env_path} and {flask_env_path}")
    load_dotenv(env_path)
    load_dotenv(flask_env_path)
    logger.info("Environment variables loaded successfully")

def get_app_settings():
    # Get logger inside the function
    logger = get_logger()

    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    
    settings = {
        'host': host,
        'port': port,
        'debug': debug
    }

    logger.info(f"Application settings: {settings}")
    return settings

def initialize_app():
    # Setup logging first
    setup_logging()
    
    # Get logger after setup
    logger = get_logger()
    logger.info("Starting application initialization")
    
    # Load environment variables
    load_environment()
    
    # Get environment name
    env = os.getenv("FLASK_ENV", "development")
    logger.info(f"Running in {env} environment")
    
    # Create app with appropriate config
    logger.debug(f"Creating Flask app with {env} configuration")
    app = create_app(configs[env])
    logger.info("Flask application created successfully")

    return app

# Initialize the application
app = initialize_app()

if __name__ == "__main__":
    try:
        # Get runtime settings
        settings = get_app_settings()

        # Get logger for main execution
        logger = get_logger()
        
        # Run the application
        logger.info(f"Starting Flask application on {settings['host']}:{settings['port']}")
        app.run(**settings)
    
    except Exception as e:
        # Get logger for exception handling
        logger = get_logger()
        logger.exception("Failed to start the application")
        raise
