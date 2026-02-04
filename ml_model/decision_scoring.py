def calculate_decision_score(bias_list):
    score = 100   # Start with perfect score

    # Deduct points based on bias severity
    for bias in bias_list:

        if "Overconfidence" in bias:
            score -= 25

        if "Recency" in bias:
            score -= 20

        if "Emotional" in bias:
            score -= 25

        if "Confirmation" in bias:
            score -= 20

    # Score limits
    if score < 0:
        score = 0

    return score
