class Constants:
    MIN_SHARE = 0.0
    MAX_SHARE = 1.0
    SHARE_EPSILON = 1e-9

    MIN_CONSTRUCTION_YEAR = 1800
    MIN_DEPRECIATION = 0
    MAX_DEPRECIATION = 100

    DEPRECIATION_EXCELLENT = 10
    DEPRECIATION_GOOD = 25
    DEPRECIATION_SATISFACTORY = 40
    DEPRECIATION_POOR = 60

    JSON_INDENT = 2
    CADASTRAL_NUMBER_DIGITS = 3

    DEFAULT_MIN_POSITIVE = 1

    REGION = "77"
    RAYON = "01"
    CADASTRAL_NUMBER_TEMPLATE = "{region}:{rayon}:{kvartal}:{unikalny}"
    DEFAULT_STATUS = "aktivnyy"
    ALLOWED_STATUSES = {"aktivnyy", "zarezervirovannyy", "annulirovannyy"}