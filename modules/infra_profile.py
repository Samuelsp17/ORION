# =========================================================
# MODULE: INFRASTRUCTURE PROFILE 
# =========================================================

def analyze_infrastructure(normalized_data):
    """
    Analyzes passive indicators to infer infrastructure profile.
    Returns a probabilistic infrastructure characterization.
    """

    indicators = []
    profile = "Unknown"
    confidence = 0.0

    web = normalized_data.get("web", {})
    ip = normalized_data.get("network", {}).get("ip")

    # --- Indicators ---
    if web.get("server") and web["server"] != "Unknown":
        indicators.append("Identified web server")

    if web.get("powered_by"):
        indicators.append("Application technology disclosure")

    if ip:
        indicators.append("Single public IP observed")

    # --- Simple heuristic profiling ---
    if len(indicators) >= 3:
        profile = "Generic hosting or simple cloud infrastructure"
        confidence = 0.7
    elif len(indicators) == 2:
        profile = "Possibly shared or moderately customized infrastructure"
        confidence = 0.5
    elif len(indicators) == 1:
        profile = "Low visibility infrastructure"
        confidence = 0.3
    else:
        profile = "Minimal observable infrastructure"
        confidence = 0.2

    return {
        "profile": profile,
        "confidence": confidence,
        "indicators": indicators
    }