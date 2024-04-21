# quiz.py
from flask import Blueprint, render_template

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')

@quiz_blueprint.route('/quiz')
def quiz_home():
    # Předání seznamu kvízů do šablony, můžete je načítat z databáze nebo konfiguračního souboru
    quizzes = [
        {'id': 1, 'name': 'Zeměpisný kvíz'},
        {'id': 2, 'name': 'Historický kvíz'},
        {'id': 3, 'name': 'Vědecký kvíz'}
    ]
    return render_template('quiz.html', quizzes=quizzes)
