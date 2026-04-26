def calculate_score(detection_result: dict) -> dict:
    """
    Calculates a risk score (0-100) and assigns a category based on detection results.
    Categories: Low (0-20), Medium (21-60), High (61-80), Critical (81-100)
    """
    score = 0
    category = "Low"
    
    if detection_result["is_malicious"]:
        patterns_count = len(detection_result["patterns_detected"])
        score = min(100, 50 + (patterns_count * 20))
        
    if score <= 20:
        category = "Low"
    elif score <= 60:
        category = "Medium"
    elif score <= 80:
        category = "High"
    else:
        category = "Critical"
        
    return {
        "score": score,
        "category": category
    }
