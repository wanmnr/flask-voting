# app/views/main.py

from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    search_query = request.args.get('q', '')
    if search_query:
        # Implement your search logic here
        # For example: search_results = perform_search(search_query)
        return render_template('index.html', search_query=search_query)
    return render_template('index.html')

@main_bp.route('/hello')
def hello():
    return 'Hello World!'

@main_bp.route('/about')
def about():
    return render_template('about.html')
