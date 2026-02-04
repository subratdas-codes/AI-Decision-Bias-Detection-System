import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load model
model = pickle.load(open("models/decision_model.pkl", "rb"))

# Prepare encoder (same as training)
le_emotion = LabelEncoder()
le_emotion.fit(["calm", "excited", "fear", "angry"])


def predict_decision(decision_data):

    # Convert emotional state
    emotion_encoded = le_emotion.transform([decision_data["emotional_state"]])[0]

    input_data = pd.DataFrame([{
        "expected_salary": decision_data["expected_salary"],
        "recent_event_impact": int(decision_data["recent_event_impact"]),
        "emotional_state": emotion_encoded,
        "ignored_alternative_options": int(decision_data["ignored_alternative_options"])
    }])

    prediction = model.predict(input_data)

    return prediction[0]
