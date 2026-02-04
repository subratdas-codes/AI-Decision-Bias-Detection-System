from utils.nlp_analyzer import analyze_text_decision


def generate_chat_response(user_text):

    detected_bias = analyze_text_decision(user_text)

    response = "🧠 AI Decision Assistant:\n\n"

    for bias in detected_bias:

        if "Emotional" in bias:
            response += "• Your decision seems emotionally influenced. Try evaluating logical pros and cons.\n"

        elif "Confirmation" in bias:
            response += "• You may be favoring information that confirms your belief. Consider alternative viewpoints.\n"

        elif "Herd" in bias:
            response += "• Your decision seems influenced by others. Ensure it matches your personal goals.\n"

        else:
            response += "• Your decision appears balanced and rational.\n"

    return response
