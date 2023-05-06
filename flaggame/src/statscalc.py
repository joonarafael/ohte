def calculate_true_statistics(all_games: list, all_streaks: list):
    player = {'total_games': 0, 'total_playtime': 0,
              'total_rounds': 0, 'total_score': 0,
              'total_streaks': 0, 'best_game_score': 0,
              'worst_game_score': float('inf'), 'average_game_score': 'N/A',
              'average_score_per_second': 'N/A', 'most_rounds_in_a_game': 0,
              'least_rounds_in_a_game': float('inf'), 'average_rounds_in_a_game': 'N/A',
              'shortest_game_duration': float('inf'), 'longest_game_duration': 0.0,
              'average_game_duration': 'N/A', 'longest_streak': 0,
              'shortest_streak': float('inf'), 'average_streak': 0,
              'average_round_score': 'N/A', 'average_round_time': 'N/A'}

    for game in all_games:
        player['total_games'] += 1
        player['total_playtime'] += float(game[1])
        player['total_rounds'] += int(game[2])
        player['total_score'] += int(game[3])
        player['total_streaks'] += int(game[7])

        if game[10] != 'n/a':
            player['average_streak'] += float(game[10])

        if float(game[1]) > player['longest_game_duration']:
            player['longest_game_duration'] = float(game[1])

        if float(game[1]) < player['shortest_game_duration']:
            player['shortest_game_duration'] = float(game[1])

        if int(game[2]) > player['most_rounds_in_a_game']:
            player['most_rounds_in_a_game'] = int(game[2])

        if int(game[2]) < player['least_rounds_in_a_game']:
            player['least_rounds_in_a_game'] = int(game[2])

        if int(game[3]) > player['best_game_score']:
            player['best_game_score'] = int(game[3])

        if int(game[3]) < player['worst_game_score']:
            player['worst_game_score'] = int(game[3])

        if game[9] != 'n/a':
            if int(game[9]) > player['longest_streak']:
                player['longest_streak'] = int(game[9])

        if game[8] != 'n/a':
            if int(game[8]) < player['shortest_streak']:
                player['shortest_streak'] = int(game[8])

    if player['total_games'] > 0:
        player['average_game_score'] = round(
            player['total_score'] / player['total_games'])

    if player['total_playtime'] > 0:
        player['average_score_per_second'] = round(
            player['total_score'] / player['total_playtime'], 1)

    if player['total_games'] > 0:
        player['average_rounds_in_a_game'] = round(
            player['total_rounds'] / player['total_games'])

    if player['total_games'] > 0:
        player['average_game_duration'] = round(
            player['total_playtime'] / player['total_games'], 1)

    if player['total_rounds'] > 0:
        player['average_round_score'] = round(
            player['total_score'] / player['total_rounds'])

    if player['total_rounds'] > 0:
        player['average_round_time'] = round(
            player['total_playtime'] / player['total_rounds'], 1)

    streak_sum = 0

    for streaks in all_streaks:
        streak_sum += sum(streaks)

    if player['total_streaks'] > 0:
        player['average_streak'] = round(
            streak_sum / player['total_streaks'], 1)

    player['total_playtime'] = str(
        round(player['total_playtime'] / 60, 1)) + "min"
    player['longest_game_duration'] = str(
        player['longest_game_duration']) + "s"
    player['shortest_game_duration'] = str(
        player['shortest_game_duration']) + "s"
    player['average_game_duration'] = str(
        player['average_game_duration']) + "s"
    player['average_round_time'] = str(
        player['average_round_time']) + "s"

    return player
