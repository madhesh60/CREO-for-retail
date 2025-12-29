
from compliance_rules import FORBIDDEN_TERMS, REQUIRED_TEXT_PATTERNS, PRICE_PATTERNS
import re

def validate_text_content(main_message, sub_message, cta_text):
    errors = []
    warnings = []
    
    combined_text = f"{main_message} {sub_message} {cta_text}".lower()
    
    # 1. Forbidden Terms Check
    for term in FORBIDDEN_TERMS:
        if term in combined_text:
            errors.append(f"Hard Fail: Forbidden term '{term}' detected. Competitions, Claims, and Greenwashing are strictly prohibited.")
            
    # 2. Price/Discount Check
    for pattern in PRICE_PATTERNS:
        if re.search(pattern, combined_text):
             errors.append("Hard Fail: Price call-outs, discounts, or money-off references are NOT allowed in this creative type (Appendix B).")
             break

    # 3. Mandatory Tags (If Tesco context implied, but for now we warn)
    # We allow 'soft' checks
    
    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

def validate_layout(fmt, width, height, elements):
    # Placeholder for geometric validation (e.g. is logo top_right?)
    # elements = [{"type": "logo", "box": (x1, y1, x2, y2)}, ...]
    return True
