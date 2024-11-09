# app/views/main.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    search_query = request.args.get('q', '')
    if search_query:
        # Implement your search logic here
        # For example: search_results = perform_search(search_query)
        return render_template('pages/index.html', search_query=search_query)
    sidebar_data = {
        'current_section': 'home',
        'announcements': [
            {'title': 'New Feature Released', 'link': '#'},
            {'title': 'Upcoming Maintenance', 'link': '#'},
        ]
    }
    return render_template('pages/index.html', 
                         sidebar_data=sidebar_data, 
                         search_query=search_query)

@main_bp.route('/hello')
def hello():
    return 'Hello World!'

@main_bp.route('/about')
def about():
    sidebar_data = {
        'current_section': 'about',
        'team_links': [
            {'name': 'Leadership', 'link': '#'},
            {'name': 'Careers', 'link': '#'},
        ]
    }
    return render_template('pages/about.html', sidebar_data=sidebar_data)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    return render_template('terms.html')