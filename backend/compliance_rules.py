# ============================================================
# Compliance Rules derived from Tesco Appendix A & Appendix B
# ============================================================

# -------------------------------
# REQUIRED TEXT PATTERNS
# -------------------------------
REQUIRED_TEXT_PATTERNS = {
    # Only these exact phrases are allowed for Tesco tags
    "tags_allowlist": [
        "only at tesco",
        "available at tesco",
        "selected stores. while stocks last.",
        "available in selected stores",
        "clubcard/app required",
        "ends dd/mm"
    ],

    "clubcard_mandatory": "available in selected stores. clubcard/app required. ends dd/mm."
}

# -------------------------------
# CLUBCARD CONSTRAINTS
# -------------------------------
CLUBCARD_CONSTRAINTS = {
    "no_cta": True,
    "no_promotional_text": True,
    "disclaimer_template": "Available in selected stores. Clubcard/app required. Ends {date}",
    "disclaimer_must_match_exactly": True,
    "date_format": "DD/MM"
}

# -------------------------------
# TESCO TAG TEXT (ALLOWLIST)
# -------------------------------
TESCO_TAGS = [
    "Only at Tesco",
    "Available at Tesco",
    "Selected stores. While stocks last."
]

# -------------------------------
# TESCO TAG PRESENCE RULES (NEW)
# -------------------------------
TAG_RULES = {
    "mandatory_if_tesco_linked": True,
    "mandatory_platforms": ["pinterest"],
    "allowed_texts": TESCO_TAGS
}

# -------------------------------
# PLATFORM RULES
# -------------------------------
PLATFORM_RULES = {
    "pinterest": {"tag_required": True},
    "instagram_story": {"tag_required": False},
    "facebook_feed": {"tag_required": False},
    "landscape": {"tag_required": False},
    "all_tesco_linked": {"tag_required": True}
}

# -------------------------------
# VALUE TILE TYPES
# -------------------------------
VALUE_TILE_TYPES = [
    "New",
    "White Value Tile",
    "Clubcard Value Tile"
]

# -------------------------------
# TILE SCHEMAS (LOCKED COMPONENTS)
# -------------------------------
TILE_SCHEMAS = {
    "New": {
        "editable": False,
        "default_text": "New",
        "color": "red"
    },
    "White Value Tile": {
        "editable_fields": ["price"],
        "style": "white_standard"
    },
    "Clubcard Value Tile": {
        "editable_fields": ["offer_price", "regular_price"],
        "mandatory_text": "Clubcard Price"
    }
}

# -------------------------------
# TILE TEXT VALIDATION (NEW)
# -------------------------------
TILE_TEXT_RULES = {
    "apply_forbidden_terms": True,
    "apply_price_patterns": True
}

# -------------------------------
# MANDATORY STRUCTURE
# -------------------------------
MANDATORY_STRUCTURE = {
    "headline": True,
    "subhead": True,
    "logo": True,
    "packshot": True
}

# -------------------------------
# FORBIDDEN TERMS (HARD FAIL)
# -------------------------------
FORBIDDEN_TERMS = {
    "competitions": [
        "competition", "winner", "win a", "chance to win", "prize", "enter now",
        "contest", "scan to participate", "lucky draw", "top 100 customers get", "giveaway"
    ],
    "financial": [
        "money back", "money-back", "guarantee", "refund", "return", "risk-free",
        "no questions asked"
    ],
    "claims": [
        "*", "survey", "voted", "rated", "best in class", "no.1 brand", "no. 1 brand",
        "clinically proven", "customer favourite", "rated highest", "proven"
    ],
    "sustainability": [
        "green", "sustainable", "eco-friendly", "environmentally", "planet", "earth",
        "carbon neutral", "better for the planet", "organic"
    ],
    "charity": [
        "charity", "donate", "partnership", "proceeds", "supporting local", "foundation"
    ],
    "tcs": [
        "terms", "conditions", "t&cs", "t&c", "apply", "see website", "check website"
    ],
    "tesco_bad_tags": [
        "exclusive at tesco", "only available here", "tesco special", "available nationwide"
    ]
}

# -------------------------------
# PRICE PATTERNS (REGEX)
# -------------------------------
PRICE_PATTERNS = [
    r"(\$|£|€|₹)\s?\d+",
    r"\d+(\.\d{1,2})?%",
    r"\d+p\b",
    r"\bfree\b",
    r"\bdiscount\b",
    r"\bdeal\b",
    r"\boffer\b",
    r"\bsale\b",
    r"\bsave\b",
    r"\bcheaper\b",
    r"\bspecial\b",
    r"\blimited time\b"
]

# -------------------------------
# SAFE ZONES
# -------------------------------
SAFE_ZONES = {
    "instagram_story": {"top": 200, "bottom": 250},
    "facebook_feed": {"top": 0, "bottom": 0},
    "landscape": {"top": 0, "bottom": 0}
}

# -------------------------------
# FONT & ACCESSIBILITY
# -------------------------------
FONT_CONSTRAINTS = {
    "brand_double": 20,
    "checkout_single": 10,
    "says": 12,
    "contrast_ratio": 4.5  # WCAG AA
}

# -------------------------------
# ALCOHOL RULES
# -------------------------------
ALCOHOL_RULES = {
    "lockup_min_height": 20,
    "lockup_min_height_says": 12,
    "contrast_colors": ["black", "white"]
}

ALCOHOL_KEYWORDS = [
    "alcohol", "wine", "beer", "vodka", "gin", "spirit", "whisky", "whiskey",
    "champagne", "prosecco", "ale", "cider", "lager", "drink", "bottle"
]

ALCOHOL_DETECTION = {
    "stage": "pre_generation",
    "mandatory": True
}

# -------------------------------
# DESIGN & LAYOUT RULES
# -------------------------------
DESIGN_RULES = {
    "packshot_spacing_double": 24,
    "packshot_spacing_single": 12,
    "visual_priority_cta": True
}

# -------------------------------
# LOW EVERYDAY PRICE (LEP)
# -------------------------------
LEP_TEMPLATE_RULES = {
    "background_color": "#FFFFFF",
    "font_color": "#00539F",
    "alignment": "left",
    "required_tag": "Selected stores. While stocks last.",
    "logo_position": "right_of_packshot",
    "cleaning_mode": "no_branded_content"
}

# -------------------------------
# TEMPLATE → CTA PERMISSION (NEW)
# -------------------------------
TEMPLATE_RULES = {
    "LEP": {"cta_allowed": False},
    "PRODUCT_LED": {"cta_allowed": False},
    "CLUBCARD": {"cta_allowed": False},
    "BRAND_AWARENESS": {"cta_allowed": True}
}

# -------------------------------
# CTA RULES (NEW)
# -------------------------------
CTA_RULES = {
    "default_allowed": False,
    "allowed_templates": ["BRAND_AWARENESS"],
    "allowed_texts": [
        "learn more",
        "view range",
        "discover more"
    ],
    "forbidden_texts": [
        "shop now", "buy now", "save now", "offer", "deal"
    ]
}

# -------------------------------
# PEOPLE DETECTION RULES (NEW)
# -------------------------------
PEOPLE_RULES = {
    "require_confirmation": True,
    "auto_fail": False
}

# -------------------------------
# FAIL FAST POLICY (NEW)
# -------------------------------
FAIL_FAST_POLICY = {
    "auto_fix": False,
    "silent_ignore": False,
    "reject_on_violation": True
}

# -------------------------------
# ERROR CODES
# -------------------------------
ERROR_CODES = {
    "ALCOHOL_LOCKUP": "E001",
    "FORBIDDEN_TERM": "E002",
    "STRUCTURE_MISSING": "E003",
    "TILE_CONSTRAINT": "E004",
    "LEP_VIOLATION": "E005",
    "SAFE_ZONE_VIOLATION": "E006",
    "PEOPLE_DETECTED": "W001",
    "ACCESSIBILITY_FONT": "E007",
    "ACCESSIBILITY_CONTRAST": "E008",
    "TAG_COLLISION": "E009",
    "TAG_MISSING": "E010",
    "PACKSHOT_DISTANCE": "E011",
    "CTA_NOT_ALLOWED": "E012"
}
