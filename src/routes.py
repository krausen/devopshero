from src import app
from json import loads
from flask import request

from src.game import try_to_start_game, try_to_stop_game, try_to_claim


@app.route('/start', methods=['POST'])
def start():
  start_data = loads(request.data)
  result = try_to_start_game(start_data['channel_id'])
  return result


@app.route('/stop', methods=['POST'])
def stop():
  stop_data = loads(request.data)
  result = try_to_stop_game(stop_data['channel_id'])
  return result


@app.route('/claim', methods=['POST'])
def claim():
  claim_data = loads(request.data)
  try_to_claim(claim_data['username'], claim_data['channel_id'])
  return ''
