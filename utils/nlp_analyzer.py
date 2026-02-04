import spacy

nlp = spacy.load("en_core_web_sm")


def analyze_text_decision(text):

    doc = nlp(text.lower())

    detected_bias = []

    emotional_keywords = ["fear", "angry", "excited", "stress", "panic"]
    confirmation_keywords = ["always", "never", "only", "definitely"]
    herd_keywords = ["everyone", "friends", "people", "others"]

    for token in doc:
        if token.text in emotional_keywords:
            detected_bias.append("Emotional Bias Detected")

        if token.text in confirmation_keywords:
            detected_bias.append("Confirmation Bias Detected")

        if token.text in herd_keywords:
            detected_bias.append("Herd Mentality Bias Detected")

    if not detected_bias:
        detected_bias.append("No Significant Text Bias Detected")

    return list(set(detected_bias))
