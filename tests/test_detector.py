import pytest
from detector import analyze_message, analyze_with_rules, SAFETY_DISCLAIMER

def test_analyze_empty_message():
    res = analyze_message("")
    assert res["score"] == 0
    assert res["level"] == "Low"
    assert res["disclaimer"] == SAFETY_DISCLAIMER

def test_high_risk_scam_message():
    scam_text = "URGENT: Your bank account will be blocked! Verify your PIN immediately at http://bit.ly/bank-fake to claim your $10,000 cash reward!"
    res = analyze_message(scam_text, "sms")
    assert res["score"] >= 60
    assert res["level"] == "High"
    assert len(res["suspicious_patterns"]) > 0
    assert len(res["recommendations"]) > 0
    assert "DO NOT click" in res["recommendations"][0]

def test_medium_risk_message():
    text = "Congratulations! You have won a $50 gift card. Contact helpdesk for details."
    res = analyze_message(text, "email")
    assert 25 <= res["score"] <= 100
    assert res["level"] in ["Medium", "High"]

def test_low_risk_safe_message():
    safe_text = "Hi Sarah, are we still meeting tomorrow at 2pm for coffee?"
    res = analyze_message(safe_text, "whatsapp")
    assert res["score"] < 25
    assert res["level"] == "Low"
    assert res["disclaimer"] == SAFETY_DISCLAIMER
