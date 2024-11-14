# app/extensions/babel.py
from flask_babel import Babel

babel = Babel()

# def get_locale():
#     if 'language' in session:
#         return session['language']
#     return request.accept_languages.best_match(['en', 'es', 'fr'])
