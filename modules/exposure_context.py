# =========================================================
# MODULE: EXPOSURE CONTEXT
# =========================================================

def analyze_exposure_context(infra_profile, correlations):
    """
    Interprets exposure signals in a human-oriented context.
    Returns an exposure posture assessment.
    """

    exposure_level = "Unknown"
    posture = "Undefined"
    interpretation = ""
    implications = []

    confidence = infra_profile.get("confidence", 0)

    # --- Exposure level inference ---
    if confidence >= 0.6:
        exposure_level = "Moderate"
    elif confidence >= 0.4:
        exposure_level = "Low"
    else:
        exposure_level = "Minimal"

    # --- Posture & interpretation ---
    if exposure_level == "Minimal":
        posture = "Highly Controlled"
        interpretation = (
            "The target exposes very limited technical information, "
            "suggesting deliberate exposure minimization."
        )
        implications.extend([
            "Passive reconnaissance yields limited results",
            "Target likely applies layered defensive strategies",
            "Higher effort required for further intelligence gathering"
        ])

    elif exposure_level == "Low":
        posture = "Controlled"
        interpretation = (
            "The target exposes a small amount of technical information, "
            "consistent with a controlled and managed posture."
        )
        implications.extend([
            "Some fingerprinting possible",
            "Exposure appears intentional rather than accidental",
            "Moderate reconnaissance cost"
        ])

    else:
        posture = "Partially Exposed"
        interpretation = (
            "The target exposes noticeable technical information, "
            "which may indicate convenience-driven or legacy configurations."
        )
        implications.extend([
            "Passive fingerprinting is feasible",
            "Potential misalignment between exposure and risk",
            "Further analysis recommended"
        ])

    return {
        "exposure_level": exposure_level,
        "posture": posture,
        "interpretation": interpretation,
        "implications": implications
    }