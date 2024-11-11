from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP errors."""
        if app.debug:
            raise error

        if request.is_json:
            response = {
                'error': error.name,
                'message': error.description,
                'status_code': error.code
            }
            return jsonify(response), error.code

        return render_template('errors/{}.html'.format(error.code)), error.code

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle non-HTTP exceptions."""
        logger.exception("An unexpected error occurred")
        if app.debug:
            raise error

        if request.is_json:
            response = {
                'error': 'Internal Server Error',
                'message': str(error),
                'status_code': 500
            }
            return jsonify(response), 500

        return render_template('errors/500.html'), 500
