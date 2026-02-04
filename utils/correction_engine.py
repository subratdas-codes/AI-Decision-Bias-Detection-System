def suggest_corrections(bias_list):
    suggestions = []

    for bias in bias_list:

        if "Overconfidence" in bias:
            suggestions.append(
                "Consider researching market salary trends before final decision."
            )

        if "Recency" in bias:
            suggestions.append(
                "Review long-term data instead of recent events only."
            )

        if "Emotional" in bias:
            suggestions.append(
                "Take a cooling period before making final decision."
            )

        if "Confirmation" in bias:
            suggestions.append(
                "Evaluate alternative options objectively."
            )

    if not suggestions:
        suggestions.append("Decision appears balanced.")

    return suggestions
