def detect_bias(decision_data):
    bias_results = []

    # Overconfidence Bias
    if decision_data.get("expected_salary", 0) > 100000:
        bias_results.append("Overconfidence Bias Detected")

    # Recency Bias
    if decision_data.get("recent_event_impact") == True:
        bias_results.append("Recency Bias Detected")

    # Emotional Bias
    if decision_data.get("emotional_state") in ["angry", "excited", "fear"]:
        bias_results.append("Emotional Bias Detected")

    # Confirmation Bias
    if decision_data.get("ignored_alternative_options") == True:
        bias_results.append("Confirmation Bias Detected")

    if not bias_results:
        bias_results.append("No Significant Bias Detected")

    return bias_results
