def generate_mitigation(score_result: dict, detection_result: dict) -> str:
    """
    Generates an actionable fix based on the risk score and detected patterns.
    """
    if score_result["category"] == "Low":
        return "No immediate action required. Prompt appears safe."
    
    if score_result["category"] in ["High", "Critical"]:
        patterns = ", ".join(detection_result.get("patterns_detected", []))
        return f"Block the prompt immediately. Detected potential jailbreak attempts: {patterns}. Consider implementing strict input sanitization or filtering these keywords."
        
    return "Monitor the prompt closely. There are minor signs of suspicious behavior. Ensure the system prompt is strictly enforcing guardrails."
