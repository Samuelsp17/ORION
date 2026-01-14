def generate_narrative_report(
    domain,
    infra_profile,
    exposure_context,
    human_context
):
    """
    Generates a human-readable narrative intelligence report.
    """

    story = []

    # --- Opening ---
    story.append(
        f"The target '{domain}' presents an infrastructure profile "
        f"classified as '{infra_profile['profile']}', "
        f"with a confidence level of {infra_profile['confidence']:.2f}."
    )

    # --- Exposure context ---
    story.append(
        f"From an exposure standpoint, the system operates under a "
        f"'{exposure_context['exposure_level']}' exposure level, "
        f"suggesting a '{exposure_context['posture']}' operational posture."
    )

    # --- Human interpretation ---
    if human_context["human_signals"]:
        story.append(
            "Behavioral indicators suggest the following human factors:"
        )
        for signal in human_context["human_signals"]:
            story.append(f"- {signal}.")
    else:
        story.append(
            "No strong behavioral indicators were identified at this stage."
        )

    # --- Interpretation layer ---
    if human_context["interpretation"]:
        story.append(
            "Interpretation of these signals indicates:"
        )
        for item in human_context["interpretation"]:
            story.append(f"- {item}.")
    
    # --- Risk bias ---
    story.append(
        f"Overall, the contextual risk bias is assessed as "
        f"'{human_context['risk_bias']}'."
    )

    # --- Closing ---
    story.append(
        "This analysis is based solely on passive intelligence and contextual "
        "correlation, without active probing or exploitation."
    )

    return "\n".join(story)