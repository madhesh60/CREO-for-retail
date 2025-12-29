
# Compliance Rules derived from Appendix A & B

REQUIRED_TEXT_PATTERNS = {
    "tags": [
        "Only at Tesco",
        "Available at Tesco",
        "Selected stores. While stocks last",
        "Available in selected stores",
        "Clubcard/app required",
        "Ends DD/MM"
    ]
}

FORBIDDEN_TERMS = [
    # Competitions
    "competition", "winner", "win a", "chance to win", "prize", "enter now",
    # Financial / Claims
    "money back", "money-back", "guarantee", "best price", "cheapest",
    # Claims
    "*", "survey", "voted", "rated",
    # Greenwashing (Sustainability)
    "green", "sustainable", "eco-friendly", "environmentally", "planet", "earth", "charity", "donate", "partnership"
]

PRICE_PATTERNS = [
    r"(\$|£|€)\d+",         # Currency
    r"\d+(\.\d{1,2})?%",    # Percentages
    r"\d+p",                # Pence
    r"\bfree\b",            # Free (unless text context is checked, usually sensitive)
    r"\bdiscount\b",
    r"\bdeal\b",
    r"\boffer\b",
    r"\bsale\b"
]

SAFE_ZONES = {
    "instagram_story": {"top": 200, "bottom": 250}, # 9x16
    "facebook_feed": {"top": 0, "bottom": 0},      # 1:1
    "landscape": {"top": 0, "bottom": 0}           # 16:9
}

FONT_CONSTRAINTS = {
    "min_size_brand": 20,
    "min_size_social": 10,
    "contrast_ratio": 4.5 # WCAG AA
}

FONT_CONSTRAINTS = {
    "min_size_brand": 20,
    "min_size_social": 10
}
