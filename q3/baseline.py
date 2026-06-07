"""
Q3(b) - Rule-based baseline classifier for ESG operational messages.
Compares against the LLM (ChatGPT) outputs.
No external libraries required.
"""
import json

# (keywords, issue_category, recommended_team) - first match wins
RULES = [
    (["leak", "water", "flood", "tap", "pipe", "burst"], "WATER", "FACILITIES"),
    (["energy", "lights", "air conditioning", "aircon", "hvac", "heating", "power"], "ENERGY", "FACILITIES"),
    (["recycl", "bin", "waste", "contaminat", "rubbish", "disposal"], "WASTE_RECYCLING", "SUSTAINABILITY"),
    (["supplier", "procurement", "vendor", "purchas"], "PROCUREMENT_SUPPLIER", "PROCUREMENT"),
    (["accessible", "accessibility", "ramp", "wheelchair", "disab"], "ACCESSIBILITY", "ACCESSIBILITY_INCLUSION"),
    (["conduct", "harassment", "governance", "misconduct", "policy breach"], "GOVERNANCE_CONDUCT", "GOVERNANCE_COMPLIANCE"),
]

URGENCY_KEYWORDS = {
    "CRITICAL": ["fire", "gas", "injur", "danger", "hazard", "emergency"],
    "HIGH": ["leak", "blocked", "all morning", "two days", "overnight", "broken"],
}

def classify(message):
    m = message.lower()
    category, team = "OTHER", "TRIAGE_HUMAN"   # default when no rule matches
    for keywords, cat, tm in RULES:
        if any(k in m for k in keywords):
            category, team = cat, tm
            break
    urgency = "MEDIUM"
    for level, kws in URGENCY_KEYWORDS.items():
        if any(k in m for k in kws):
            urgency = level
            break
    return {"issue_category": category, "urgency": urgency, "recommended_team": team}

# The three official assessment messages
messages = [
    "There is a water leak in Building C that has been running all morning.",
    "I want to report that one of our suppliers may not meet our sustainability policy.",
    "The accessible entrance near the main building has been blocked for two days.",
]

# Robustness checks - same issues, paraphrased without obvious keywords
robustness = [
    "Moisture keeps coming through the ceiling on level 2.",
    "There's a step at the side door that someone in a chair can't get past.",
]

print("=== Baseline classifications (3 assessment messages) ===")
for msg in messages:
    print(json.dumps({"message": msg, **classify(msg)}))

print("\n=== Robustness check (paraphrased, keyword-free) ===")
for msg in robustness:
    print(json.dumps({"message": msg, **classify(msg)}))
