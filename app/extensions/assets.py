# app/extensions/assets.py

import logging
from flask_assets import Environment, Bundle

class FlaskAssets:
    def __init__(self):
        self.assets = Environment()
        self.logger = logging.getLogger(__name__)

    def init_app(self, app):
        """Initialize assets with application"""
        try:
            self.assets.init_app(app)
            self.assets.debug = app.config.get('ASSETS_DEBUG', False)
            self._register_bundles()
        except Exception as e:
            self.logger.critical(f"Fatal error in asset initialization: {str(e)}", exc_info=True)
            raise

    def _register_bundles(self):
        """Register all asset bundles"""
        self._register_css_bundles()
        self._register_js_bundles()
        self._register_scss_bundles()

    def _register_css_bundles(self):
        """Register CSS bundles with fallback to unminified files"""
        try:
            css = Bundle(
                'css/vendor/*.css',
                'css/style.css',
                filters='cssmin',
                output='dist/css/style.min.css'
            )
            self.assets.register('css_all', css)
            self.logger.info("CSS bundle registered successfully")
        except Exception as e:
            self.logger.warning(
                f"CSS bundle registration failed: {str(e)}. Falling back to unminified CSS.",
                exc_info=True
            )
            # Fallback to unminified CSS
            self._register_unminified_css()

    def _register_js_bundles(self):
        """Register JS bundles with strict error handling"""
        try:
            js = Bundle(
                'js/vendor/*.js',
                'js/main.js',
                filters='jsmin',
                output='dist/js/main.min.js'
            )
            self.assets.register('js_all', js)
            self.logger.info("JavaScript bundle registered successfully")
        except Exception as e:
            self.logger.critical(
                f"JavaScript bundle registration failed: {str(e)}. Application functionality may be impaired!",
                exc_info=True
            )
            raise  # JS is often critical for app functionality

    def _register_scss_bundles(self):
        """Register SCSS bundles with compilation error handling"""
        try:
            scss = Bundle(
                'scss/layout/_sidebar.scss',
                filters='libsass',
                output='css/style.css',
                depends=['scss/_variables.scss']
            )
            self.assets.register('scss_all', scss)
            self.logger.info("SCSS bundle registered successfully")
        except Exception as e:
            self.logger.error(
                f"SCSS compilation failed: {str(e)}. Falling back to pre-compiled CSS.",
                exc_info=True
            )
            self._register_fallback_scss()

    def _register_unminified_css(self):
        """Fallback method for CSS when minification fails"""
        try:
            css = Bundle(
                'css/vendor/*.css',
                'css/style.css',
                output='dist/css/style.css'
            )
            self.assets.register('css_all', css)
            self.logger.info("Unminified CSS fallback registered")
        except Exception as e:
            self.logger.critical(f"Even fallback CSS registration failed: {str(e)}", exc_info=True)
            raise

    def _register_fallback_scss(self):
        """Fallback method for SCSS when compilation fails"""
        try:
            # Fallback to pre-compiled CSS
            css = Bundle(
                'css/precompiled-style.css',
                output='css/style.css'
            )
            self.assets.register('scss_all', css)
            self.logger.info("Pre-compiled CSS fallback registered")
        except Exception as e:
            self.logger.critical(f"SCSS fallback registration failed: {str(e)}", exc_info=True)
            raise

assets = FlaskAssets()


