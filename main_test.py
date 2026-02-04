from rule_engine.bias_rules import detect_bias
from utils.correction_engine import suggest_corrections
from ml_model.decision_scoring import calculate_decision_score
from ml_model.predict_model import predict_decision

sample_decision = {
    "expected_salary": 150000,
    "recent_event_impact": True,
    "emotional_state": "excited",
    "ignored_alternative_options": True
}

bias_result = detect_bias(sample_decision)
suggestions = suggest_corrections(bias_result)
score = calculate_decision_score(bias_result)
prediction = predict_decision(sample_decision)

print("\nBias Analysis Result:")
for bias in bias_result:
    print("-", bias)

print("\nCorrection Suggestions:")
for suggestion in suggestions:
    print("-", suggestion)

print(f"\nDecision Quality Score: {score}/100")
print(f"\nML Decision Classification: {prediction}")
