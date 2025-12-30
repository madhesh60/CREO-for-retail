
# Compliance Rules derived from Appendix A & B

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

# New Mandatory Rule: Pinterest -> Tesco Tag Required
# This logic will be handled in Validator/Composer, but rule is defined here.
PLATFORM_RULES = {
    "pinterest": {"tag_required": True},
    "all_tesco_linked": {"tag_required": True}
}

VALUE_TILE_TYPES = [
    "New", 
    "White Value Tile", 
    "Clubcard Value Tile"
]

MANDATORY_STRUCTURE = {
    "headline": True,
    "subhead": True,
    "logo": True,
    "packshot": True
}

# All of these trigger a HARD FAIL
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

PRICE_PATTERNS = [
    r"(\$|£|€|₹)\s?\d+",    # Currency
    r"\d+(\.\d{1,2})?%",    # Percentages
    r"\d+p\b",              # Pence
    r"\bfree\b",            # Free
    r"\bdiscount\b",
    r"\bdeal\b",
    r"\boffer\b",
    r"\bsale\b",
    r"\bsave\b",
    r"\bcheaper\b",
    r"\bspecial\b",
    r"\blimited time\b"
]

SAFE_ZONES = {
    # 9x16 Format (1080x1920)
    "instagram_story": {"top": 200, "bottom": 250}, 
    # 1:1 Format (1080x1080)
    "facebook_feed": {"top": 0, "bottom": 0},      
    # 16:9 Format
    "landscape": {"top": 0, "bottom": 0}           
}

FONT_CONSTRAINTS = {
    "brand_double": 20,         # Brand / Checkout Double Density / Social
    "checkout_single": 10,      # Checkout Single Density
    "says": 12,                # SAYS
    "contrast_ratio": 4.5      # WCAG AA
}

ALCOHOL_RULES = {
    "lockup_min_height": 20,
    "lockup_min_height_says": 12,
    "contrast_colors": ["black", "white"]
}

DESIGN_RULES = {
    "packshot_spacing_double": 24,
    "packshot_spacing_single": 12,
    "visual_priority_cta": True # Check distance: Packshot < other elements
}

ALCOHOL_KEYWORDS = [
    "alcohol", "wine", "beer", "vodka", "gin", "spirit", "whisky", "whiskey",
    "champagne", "prosecco", "ale", "cider", "lager", "drink", "bottle"
]

LEP_TEMPLATE_RULES = {
    "background_color": "#FFFFFF", # White
    "font_color": "#00539F",      # Tesco Blue
    "alignment": "left",
    "required_tag": "Selected stores. While stocks last.",
    "logo_position": "right_of_packshot",
    "cleaning_mode": "no_branded_content"
}

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
    "PACKSHOT_DISTANCE": "E011"
}
