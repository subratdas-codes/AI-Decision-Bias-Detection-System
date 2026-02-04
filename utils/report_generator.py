from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(decision_data, bias_result, suggestions, score, prediction, risk):

    file_name = "decision_report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)
    y = 750

    c.setFont("Helvetica", 12)

    c.drawString(200, y, "AI Decision Analysis Report")
    y -= 40

    c.drawString(50, y, f"Expected Salary: {decision_data['expected_salary']}")
    y -= 20

    c.drawString(50, y, f"Emotional State: {decision_data['emotional_state']}")
    y -= 20

    c.drawString(50, y, f"Recent Event Impact: {decision_data['recent_event_impact']}")
    y -= 20

    c.drawString(50, y, f"Ignored Alternatives: {decision_data['ignored_alternative_options']}")
    y -= 40

    c.drawString(50, y, "Bias Analysis:")
    y -= 20
    for b in bias_result:
        c.drawString(70, y, f"- {b}")
        y -= 20

    y -= 20
    c.drawString(50, y, "Correction Suggestions:")
    y -= 20
    for s in suggestions:
        c.drawString(70, y, f"- {s}")
        y -= 20

    y -= 20
    c.drawString(50, y, f"Decision Score: {score}/100")
    y -= 20

    c.drawString(50, y, f"ML Classification: {prediction}")
    y -= 20

    c.drawString(50, y, f"Risk Level: {risk}")

    c.save()

    return file_name
