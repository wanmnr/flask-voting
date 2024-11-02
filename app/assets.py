# assets.py

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