from src import app
from flask import request

from src.game import try_to_start_game, try_to_stop_game, try_to_claim, try_to_get_high_score


@app.route('/start', methods=['POST'])
def start():
  result = try_to_start_game(request.form['channel_id'])
  return result


@app.route('/stop', methods=['POST'])
def stop():
  result = try_to_stop_game(request.form['channel_id'])
  return result


@app.route('/claim', methods=['POST'])
def claim():
  try_to_claim(request.form['user_name'], request.form['channel_id'])
  return ''

@app.route('/high_score', methods=['POST'])
def high_score():
  result = try_to_get_high_score(request.form['channel_id'])
  return result