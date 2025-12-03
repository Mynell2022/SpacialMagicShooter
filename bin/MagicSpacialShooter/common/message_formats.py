


def create_input_message(player_id, inputs, timestamp):
    return {
        'type': 'input',
        'player_id': player_id,
        'inputs': inputs,
        'timestamp': timestamp
    }

def create_state_message(players, bullets, powerups, scores, game_time):
    return {
        'type': 'state',
        'players': players,
        'bullets': bullets,
        'powerups': powerups,
        'scores': scores,
        'game_time': game_time
    }
