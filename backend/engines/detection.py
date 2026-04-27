import re

# Simple heuristic-based detection for V1
JAILBREAK_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt override",
    r"you are a developer mode",
    r"do anything now",
    r"bypass safety",
]

# RAG Injection patterns
RAG_PATTERNS = [
    r"\[end of text\]",
    r"\[system\]",
    r"new instructions:",
    r"disregard the above document",
    r"document content ending",
]

# Malicious Tool Calling / Secret File Access Patterns
MALICIOUS_TOOL_PATTERNS = [
    r"/etc/passwd",
    r"\.env",
    r"read_file",
    r"os\.system",
    r"subprocess",
    r"ssh_key",
    r"id_rsa",
    r"system file",
]

def detect_risks(prompt: str) -> dict:
    """
    Analyzes the prompt and returns detection results.
    """
    prompt_lower = prompt.lower()
    detected_patterns = []
    
    # 1. Large Prompt Injection (Context Overflow)
    if len(prompt) > 5000:
        detected_patterns.append("large_prompt_context_overflow")
    
    # 2. Jailbreak Patterns
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt_lower):
            detected_patterns.append(f"jailbreak_pattern: {pattern}")
            
    # 3. RAG Based Injection
    for pattern in RAG_PATTERNS:
        if re.search(pattern, prompt_lower):
            detected_patterns.append(f"rag_injection: {pattern}")
            
    # 4. Malicious Tool Calling
    for pattern in MALICIOUS_TOOL_PATTERNS:
        if re.search(pattern, prompt_lower):
            detected_patterns.append(f"malicious_tool_call: {pattern}")
            
    is_malicious = len(detected_patterns) > 0
    
    return {
        "is_malicious": is_malicious,
        "patterns_detected": detected_patterns
    }
