from flask import Blueprint, render_template, redirect, url_for, flash, request

polls_bp = Blueprint('polls', __name__, url_prefix='/polls')

@polls_bp.route('/list_all')
def list_all():
    return render_template('')