import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load dataset
data = pd.read_csv("data/decision_dataset.csv")

# Convert emotional state to numeric
le_emotion = LabelEncoder()
data["emotional_state"] = le_emotion.fit_transform(data["emotional_state"])

# Convert True/False to 1/0
data["recent_event_impact"] = data["recent_event_impact"].astype(int)
data["ignored_alternative_options"] = data["ignored_alternative_options"].astype(int)

# Features & Target
X = data.drop("label", axis=1)
y = data["label"]

# Train Model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save Model
pickle.dump(model, open("models/decision_model.pkl", "wb"))

print("Model trained and saved successfully")
