def find_gamemode(game_mode: int):
    """
    determine the game mode name from the given integer value

    Args:
        game_mode (int): game mode as an integer

    Returns:
        string: game mode as a string
    """

    if game_mode == 0:
        return "Classic"

    if game_mode == 1:
        return "Advanced"

    if game_mode == 2:
        return "Time Trial"

    if game_mode == 3:
        return "One Life"

    return "Free"


def calculate_game_statistics(game_mode: int, rounds: list, streaks: list, game_time: float):
    """
    calculate the statistics for a finished game

    Args:
        game_mode (int): game mode as an integer,
        rounds (list): list of every single round,
        streaks (list): list of all completed streaks,
        game_time (float): complete game time as an float value

    Returns:
        list: list containing all the appropriate game statistics ready for file writing
    """

    rounds_total = len(rounds)
    scores = []
    non_zero_scores = []
    times = []

    for i_round in rounds:
        scores.append(i_round[0])

        if i_round[0] > 0:
            non_zero_scores.append(i_round[0])

        times.append(round(i_round[1], 2))

    if len(non_zero_scores) > 0:
        avg_earned_score = round(
            sum(non_zero_scores) / len(non_zero_scores), 1)

    else:
        avg_earned_score = "n/a"

    streaks_total = len(streaks)

    if streaks_total > 0:
        average_streak = round(sum(streaks) / streaks_total, 1)

    else:
        average_streak = "n/a"

    full_stats_row = [find_gamemode(game_mode), game_time, rounds_total, sum(scores),
                      min(non_zero_scores, default='n/a'),
                      max(non_zero_scores, default='n/a'), avg_earned_score,
                      streaks_total, min(streaks, default='n/a'),
                      max(streaks, default='n/a'),
                      average_streak, min(times, default='n/a'),
                      max(times, default='n/a'), round(sum(times) / rounds_total, 2)]

    return full_stats_row
