import re
import requests
import json
from config import Config

# Universal safety disclaimer required by rules
SAFETY_DISCLAIMER = (
    "Disclaimer: This detector provides a risk assessment based on automated pattern analysis "
    "and AI analysis. A Low risk score does NOT guarantee that a message is 100% safe. Always verify "
    "unknown senders, avoid clicking untrusted links, and never share confidential personal or financial credentials."
)

# Common scam indicators and patterns
SUSPICIOUS_PATTERNS = [
    {
        "category": "Urgency & Threats",
        "pattern": r"(urgent|immediately|within \d+ hours?|account (will be|has been) (suspended|blocked|terminated|closed)|action required|immediate attention)",
        "weight": 20,
        "description": "Uses pressure tactics or urgent threats to induce panic and force hasty decisions."
    },
    {
        "category": "Financial Lures & Prizes",
        "pattern": r"(won|congratulations|lottery|prize|\$\d+[\d,]*|claim your|cash reward|free gift|unclaimed funds|gift card|crypto|guaranteed returns|earn \$\d+)",
        "weight": 25,
        "description": "Promises unrealistic financial gains, rewards, or free gifts to deceive victims."
    },
    {
        "category": "Banking & Payment Security",
        "pattern": r"(bank|verify your account|update billing|unauthorized transaction|login details|cvv|otp|pin|wire transfer|zelle|venmo|cashapp|payment failed)",
        "weight": 25,
        "description": "Requests verification of sensitive financial accounts, OTPs, or payment details."
    },
    {
        "category": "Impersonation & Official Claims",
        "pattern": r"(customer support|helpdesk|amazon|whatsapp team|fedex|dhl|usps|irs|tax department|security alert|official notice)",
        "weight": 15,
        "description": "Impersonates well-known services, government entities, or official support teams."
    },
    {
        "category": "Suspicious Links & Domains",
        "pattern": r"(https?://[^\s]+|bit\.ly|[a-zA-Z0-9-]+\.(xyz|top|club|info|live|online|tk|gq|ml|work|site|click))",
        "weight": 25,
        "description": "Contains links or suspicious top-level domains often used in phishing campaigns."
    },
    {
        "category": "Job & Remote Work Scams",
        "pattern": r"(work from home|part-time job|daily payout|\$\d+/hour|no experience needed|hr manager|telegram|whatsapp chat)",
        "weight": 15,
        "description": "Promotes suspicious easy work-from-home jobs requiring upfront contact via chat apps."
    }
]


def analyze_with_rules(text: str, platform: str = "general") -> dict:
    """
    Performs deterministic pattern matching on the message text.
    Calculates a risk score from 0 to 100, identifies suspicious patterns,
    and returns safety recommendations.
    """
    if not text or not text.strip():
        return {
            "score": 0,
            "level": "Low",
            "suspicious_patterns": [],
            "found_words": [],
            "recommendations": ["No content provided to analyze."],
            "disclaimer": SAFETY_DISCLAIMER,
            "source": "Rule Engine"
        }

    lowered_text = text.lower()
    score = 0
    matched_patterns = []
    found_words = set()

    for item in SUSPICIOUS_PATTERNS:
        matches = re.findall(item["pattern"], lowered_text, flags=re.IGNORECASE)
        if matches:
            # Add score for match
            score += item["weight"]
            matched_patterns.append({
                "category": item["category"],
                "description": item["description"]
            })
            for m in matches:
                if isinstance(m, tuple):
                    for part in m:
                        if part and len(part) > 2:
                            found_words.add(part.strip())
                elif isinstance(m, str) and len(m) > 2:
                    found_words.add(m.strip())

    # Adjust score based on platform specific heuristics
    if platform.lower() == "whatsapp" and re.search(r"unknown number|send code|verification code", lowered_text):
        score += 15
    elif platform.lower() == "email" and re.search(r"dear customer|undisclosed-recipients|invoice", lowered_text):
        score += 10
    elif platform.lower() == "sms" and re.search(r"click here|reply stop|call now", lowered_text):
        score += 10

    # Cap score between 0 and 100
    risk_score = min(100, max(0, score))

    # Risk level classification
    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    recommendations = generate_recommendations(risk_level, matched_patterns, platform)

    return {
        "score": risk_score,
        "level": risk_level,
        "suspicious_patterns": matched_patterns,
        "found_words": sorted(list(found_words)),
        "recommendations": recommendations,
        "disclaimer": SAFETY_DISCLAIMER,
        "source": "Rule Engine"
    }


def analyze_with_ai(text: str, platform: str = "general") -> dict:
    """
    Attempts to call an external AI API (e.g., OpenAI/Gemini/Groq/generic endpoint)
    if AI_API_KEY is configured. Fallback to rule engine if API fails or key is missing.
    """
    api_key = Config.AI_API_KEY
    if not api_key:
        # Fall back to rule-based engine if no API key present
        return analyze_with_rules(text, platform)

    prompt = (
        f"You are a cybersecurity expert analyzing a potential scam message on platform '{platform}'.\n"
        f"Analyze this message:\n\"\"\"{text}\"\"\"\n\n"
        "Return ONLY a JSON object with the following keys:\n"
        "- score: integer from 0 to 100 representing scam risk score\n"
        "- level: string, strictly one of 'Low', 'Medium', or 'High'\n"
        "- suspicious_patterns: list of objects with 'category' and 'description'\n"
        "- found_words: list of suspicious words/phrases found\n"
        "- recommendations: list of actionable safety recommendations\n"
    )

    try:
        provider = Config.AI_PROVIDER
        if provider == "openai":
            url = Config.AI_API_URL or "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "response_format": {"type": "json_object"}
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                parsed["disclaimer"] = SAFETY_DISCLAIMER
                parsed["source"] = "AI Engine (OpenAI)"
                return parsed

        elif provider == "gemini":
            url = Config.AI_API_URL or f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt + "\nRespond with valid JSON."}]}]
            }
            resp = requests.post(url, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                clean_text = re.sub(r"```json|```", "", raw_text).strip()
                parsed = json.loads(clean_text)
                parsed["disclaimer"] = SAFETY_DISCLAIMER
                parsed["source"] = "AI Engine (Gemini)"
                return parsed

    except Exception:
        # Fallback to rule engine seamlessly on any API failure
        pass

    # Fallback to rule engine
    return analyze_with_rules(text, platform)


def analyze_message(text: str, platform: str = "general") -> dict:
    """
    Main entry point for message analysis. Uses AI if configured, otherwise rule engine.
    """
    rule_result = analyze_with_rules(text, platform)

    # If API Key exists, attempt AI analysis
    if Config.AI_API_KEY:
        ai_result = analyze_with_ai(text, platform)
        if ai_result:
            return ai_result

    return rule_result


def generate_recommendations(risk_level: str, patterns: list, platform: str) -> list:
    """Generates user recommendations based on risk classification and context."""
    recs = []

    if risk_level == "High":
        recs.append("DO NOT click any links or download attachments in this message.")
        recs.append("DO NOT share OTPs, passwords, PINs, or personal identity information.")
        recs.append(f"Block and report the sender immediately on {platform.title() if platform != 'general' else 'your app'}.")
        recs.append("If a bank or official entity is claimed, contact them directly through their official website or phone number on your bank card.")
    elif risk_level == "Medium":
        recs.append("Exercise caution before replying or interacting with links in this message.")
        recs.append("Verify the sender's identity using an independent contact channel.")
        recs.append("Check if the website URL matches the official domain exactly (watch for typos squatting).")
    else:
        recs.append("While this message displays low risk indicators, always remain vigilant.")
        recs.append("Never enter login credentials on websites reached via unsolicited links.")
        recs.append("Verify unexpected notices directly with the sender or official organization.")

    return recs
