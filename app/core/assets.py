# app/core/assets.py

from flask_assets import Environment, Bundle

def init_assets(app):
    """Initialize and configure Flask-Assets"""
    assets = Environment(app)
    assets.debug = app.config.get('ASSETS_DEBUG', False)
    
    # Define asset bundles
    css = Bundle(
        'css/style.css',
        filters='cssmin',
        output='gen/style.min.css',
        depends='css/*.css'
    )
    
    # Register bundles
    assets.register('css_all', css)
    
    return assets





from flask_assets import Bundle, Environment

assets = Environment()

# CSS Bundle
css = Bundle(
    'css/vendor/*.css',
    'css/main.css',
    filters='cssmin',
    output='dist/css/main.min.css'
)

# JavaScript Bundle
js = Bundle(
    'js/vendor/*.js',
    'js/main.js',
    filters='jsmin',
    output='dist/js/main.min.js'
)

def init_assets(assets):
    """Initialize asset bundles."""
    assets.register('css_all', css)
    assets.register('js_all', js)

# Register bundles
init_assets(assets)