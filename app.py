from flask import Flask, render_template, request, redirect, session
from game_logic import NBAStatsGame
import random

app = Flask(__name__)

stat_categories = ['PTS', 'AST', 'REB', 'STL', 'BLK']
game = NBAStatsGame(stat_categories)
game.get_selection_pool_and_all_ranks()

total_score = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    remaining_categories = [cat for cat in stat_categories if cat not in session.get('selected_categories', [])]
    player = random.choice(game.selection_pool)
    if request.method == 'POST':
        category = request.form['category']
        guessed_rank = game.all_ranks[player['PLAYER_ID']][f'{category}_RANK']
        session.setdefault('selected_categories', []).append(category)
        session['total_score'] = session.get('total_score', 0) + guessed_rank
        return redirect('/')
    return render_template('index.html', player=player['PLAYER'], remaining_categories=remaining_categories)

@app.route('/results')
def results():
    total_score = session.get('total_score', 0)
    result_message = ""
    if total_score <= 150:
        result_message = "We have a winner!"
    elif total_score <= 200:
        result_message = "So close... yet so far"
    else:
        result_message = "Yikes. Don't quit your day job!"
    selected_categories = session.get('selected_categories', [])
    results = [{'player': player['PLAYER'], 'category': category, 'guessed_rank': game.all_ranks[player['PLAYER_ID']][f'{category}_RANK']} for player in game.selection_pool for category in selected_categories if f'{category}_RANK' in game.all_ranks[player['PLAYER_ID']]]
    game_over = len(selected_categories) == len(stat_categories)
    return render_template('results.html', results=results, total_score=total_score, result_message=result_message, game_over=game_over)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
