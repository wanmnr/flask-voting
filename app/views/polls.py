# app/views/polls

from flask import Blueprint, render_template, redirect, url_for, flash, request

polls_bp = Blueprint('polls', __name__, url_prefix='/polls')

@polls_bp.route('/list_all')
def list_all():
    return render_template('polls/list.html')

@polls_bp.route('/detail')
def detail():
    return render_template('polls/detail.html')

@polls_bp.route('/results')
def results():
    return render_template('polls/results.html')

@polls_bp.route('/vote')
def vote():
    return render_template('polls/vote.html')
