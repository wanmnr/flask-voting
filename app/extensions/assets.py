# app/extensions/assets.py

from flask_assets import Environment, Bundle
from ..utils.logger import get_logger

assets = Environment()
logger = get_logger(__name__)

def init_assets(app):
    """Initialize and configure Flask-Assets"""
    try:
        # Initialize assets with the app
        assets.init_app(app)  # Add this line

        # Log debug information about configuration
        logger.debug(f"Initializing assets with debug mode: {app.config.get('ASSETS_DEBUG', False)}")

        assets.debug = app.config.get('ASSETS_DEBUG', False)

        try:
            # Define asset bundles
            css = Bundle(
                'css/vendor/*.css',
                'css/main.css',
                'css/style.css',
                filters='cssmin',
                output='dist/css/main.min.css',
                depends='css/*.css'
            )
            logger.info("CSS bundle created successfully")

        except Exception as e:
            logger.warning(f"CSS bundle creation issue: {str(e)}. Falling back to unminified CSS.")
            # Implement fallback behavior here

        try:
            # Define SCSS bundle
            scss = Bundle(
                'scss/layout/_sidebar.scss',
                filters='libsass',
                output='css/sidebar.css',
                depends=['scss/_variables.scss']
            )
            logger.info("SCSS bundle created successfully")

        except Exception as e:
            logger.error(f"SCSS bundle creation failed: {str(e)}", exc_info=True)
            # Critical functionality might be affected

        try:
            # Define JS bundle
            js = Bundle(
                'js/vendor/*.js',
                'js/main.js',
                filters='jsmin',
                output='dist/js/main.min.js'
            )
            logger.info("JS bundle created successfully")

        except Exception as e:
            logger.critical(f"JS bundle creation failed: {str(e)}. Application may not function correctly!", exc_info=True)
            raise  # Re-raise if this is truly critical

        # Register bundles
        assets.register('css_all', css)
        assets.register('scss_all', scss)
        assets.register('js_all', js)

        logger.info("All asset bundles registered successfully")

    except Exception as e:
        logger.critical(f"Fatal error in asset initialization: {str(e)}", exc_info=True)
        raise

    return assets


