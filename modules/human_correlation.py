def analyze_human_correlation(infra_profile, exposure_context):
    """
    Performs non-technical, human-oriented correlation.
    Focuses on behavior, posture and operational maturity.
    """

    signals = []
    interpretation = []
    risk_bias = "neutral"

    profile = infra_profile.get("profile", "")
    confidence = infra_profile.get("confidence", 0)
    exposure_level = exposure_context.get("exposure_level", "")
    posture = exposure_context.get("posture", "")

    # --- Human signals inference ---

    if confidence < 0.4:
        signals.append("Low infrastructure visibility")
        interpretation.append(
            "Target may not prioritize external exposure awareness"
        )

    if "shared" in profile.lower():
        signals.append("Shared infrastructure usage")
        interpretation.append(
            "Cost-saving decisions may override security isolation concerns"
        )

    if exposure_level in ["medium", "high"]:
        signals.append("Elevated exposure posture")
        interpretation.append(
            "Exposure likely accepted for operational convenience"
        )

    if posture == "reactive":
        signals.append("Reactive security posture")
        interpretation.append(
            "Security actions likely occur after incidents, not before"
        )

    # --- Bias adjustment ---
    if len(signals) >= 3:
        risk_bias = "optimistic_for_attacker"
    elif len(signals) == 2:
        risk_bias = "balanced"
    else:
        risk_bias = "defensive_or_mature"

    return {
        "human_signals": signals,
        "interpretation": interpretation,
        "risk_bias": risk_bias
    }
