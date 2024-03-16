import random
import string
import secrets

from flask import Flask, render_template, request, session, redirect, url_for
from game_logic import NBAStatsGame

app = Flask(__name__)
app.secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

game = NBAStatsGame(['PTS', 'AST', 'REB', 'STL', 'BLK'])
game.get_selection_pool_and_all_ranks()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'total_score' not in session:
        session['total_score'] = 0
    if 'remaining_categories' not in session:
        session['remaining_categories'] = list(game.stat_categories) 
    if 'player_results' not in session:
        session['player_results'] = []

    if request.method == 'POST':
        category = request.form['category']
        player_name = session['player']
        player_id = session['player_id']
        guessed_rank = game.all_ranks[player_id][f'{category}_RANK']
        session['total_score'] += guessed_rank
        session['remaining_categories'].remove(category)
        session['player_results'].append({'player': player_name, 'category': category, 'guessed_rank': guessed_rank})
        if not session['remaining_categories']:
            return redirect('/result')

    if session['remaining_categories']:
        category_to_guess = random.choice(session['remaining_categories']) 
        player = random.choice(game.selection_pool)
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']
        session['player'] = player_name
        session['player_id'] = player_id
        session['category'] = category_to_guess
        return render_template('index.html', player=player_name, category=session['category'],
                               remaining_categories=session['remaining_categories'])
    else:
        return redirect('/result')


@app.route('/reset')
def reset():
    session.pop('total_score', None)
    session.pop('remaining_categories', None)
    session.pop('player_results', None)
    return redirect(url_for('index'))


@app.route('/result')
def result():
    total_score = session.get('total_score', 0)
    result_message = ""
    if total_score <= 150:
        result_message = "We have a winner!"
    elif total_score <= 200:
        result_message = "So close... yet so far"
    else:
        result_message = "Yikes. Don't quit your day job!"
    return render_template('results.html', results=session['player_results'], total_score=total_score, result_message=result_message, game_over=True)


if __name__ == '__main__':
    app.run()
