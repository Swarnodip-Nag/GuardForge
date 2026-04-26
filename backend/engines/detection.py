import re

# Simple heuristic-based detection for V1
JAILBREAK_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt override",
    r"you are a developer mode",
    r"do anything now",
    r"bypass safety",
]

def detect_risks(prompt: str) -> dict:
    """
    Analyzes the prompt and returns detection results.
    """
    prompt_lower = prompt.lower()
    detected_patterns = []
    
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt_lower):
            detected_patterns.append(pattern)
            
    is_malicious = len(detected_patterns) > 0
    
    return {
        "is_malicious": is_malicious,
        "patterns_detected": detected_patterns
    }
