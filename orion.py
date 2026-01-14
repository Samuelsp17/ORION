#!/usr/bin/env python3
import sys
import argparse
import socket
import subprocess 
import requests
from modules.infra_profile import analyze_infrastructure
from modules.exposure_context import analyze_exposure_context
from modules.human_correlation import analyze_human_correlation
from reports.templates import generate_narrative_report

# =========================================================
# MODULE: COLLECTION (RECON)
# =========================================================
def recon_module(domain):
    print("[RECON] Starting information collection...")

    recon_data = {
        "domain": domain,
        "dns": {},
        "ip": None,
        "http_headers": {},
    }

    # DNS / IP resolution
    try:
        recon_data["ip"] = socket.gethostbyname(domain)
    except Exception:
        recon_data["ip"] = None

    # Basic DNS records (raw)
    try:
        result = subprocess.check_output(
            ["nslookup", domain],
            stderr=subprocess.DEVNULL,
            text=True
        )
        recon_data["dns"]["raw"] = result
    except Exception:
        recon_data["dns"]["raw"] = None

    # HTTP Headers (passive)
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        recon_data["http_headers"] = dict(response.headers)
    except Exception:
        recon_data["http_headers"] = {}

    print("[RECON] Collection finished.")
    return recon_data

# =========================================================
# MODULE: PROCESSING
# =========================================================
def processing_module(recon_data):
    print("[PROCESSING] Organizing collected data...")

    processed = {
        "domain": recon_data["domain"],
        "network": {
            "ip": recon_data["ip"]
        },
        "dns": recon_data["dns"],
        "web": {
            "headers": recon_data["http_headers"],
            "server": recon_data["http_headers"].get("Server", "Unknown"),
            "powered_by": recon_data["http_headers"].get("X-Powered-By")
        }
    }

    print("[PROCESSING] Data organized.")
    return processed


# =========================================================
# MODULE: NORMALIZATION 
# =========================================================
def normalization_module(processed_data):
    print("[NORMALIZATION] Normalizing data...")

    normalized = processed_data.copy()

    server = normalized["web"]["server"]
    if server:
        normalized["web"]["server"] = server.split("/")[0].strip()

    powered = normalized["web"]["powered_by"]
    if powered:
        normalized["web"]["powered_by"] = powered.split(" ")[0].strip()

    print("[NORMALIZATION] Normalization completed.")
    return normalized


# =========================================================
# MODULE: CORRELATION 
# =========================================================
def correlation_module(normalized_data):
    print("[CORRELATION] Correlating information...")

    correlations = []

    web = normalized_data["web"]

    if web["server"] != "Unknown" and web["powered_by"]:
        correlations.append({
            "type": "tech_stack",
            "description": "Web server and application technology both exposed",
            "confidence": 0.7
        })

    if web["server"] != "Unknown":
        correlations.append({
            "type": "service_exposure",
            "description": f"Identified web server: {web['server']}",
            "confidence": 0.5
        })

    if not correlations:
        correlations.append({
            "type": "low_visibility",
            "description": "Low technology disclosure detected",
            "confidence": 0.3
        })

    print("[CORRELATION] Correlation completed.")
    return correlations


# =========================================================
# MODULE: RISK ANALYSIS 
# =========================================================
def risk_analysis_module(normalized_data, correlations):
    print("[AI] Starting contextual risk analysis...")

    findings = []

    for item in correlations:
        if item["confidence"] >= 0.7:
            severity = "Medium"
        elif item["confidence"] >= 0.4:
            severity = "Low"
        else:
            severity = "Informational"

        findings.append({
            "severity": severity,
            "description": item["description"],
            "confidence": item["confidence"]
        })

    analysis = {
        "summary": "Contextual passive analysis completed.",
        "findings": findings,
        "next_steps": [
            "Improve DNS parsing and structuring",
            "Introduce passive subdomain intelligence",
            "Add infrastructure pattern analysis"
        ]
    }

    print("[AI] Analysis completed.")
    return analysis


# =========================================================
# MODULE: OUTPUT (REPORT) 
# =========================================================
def output_module(processed_data, analysis):
    print("\n========== ORION REPORT ==========")
    print(f"Target: {processed_data['domain']}")
    print(f"IP Address: {processed_data['network']['ip']}")

    print("\nFindings:")
    for finding in analysis["findings"]:
        print(
            f"- [{finding['severity']}] "
            f"{finding['description']} "
            f"(confidence: {finding['confidence']})"
        )

    print("\nSuggested next steps:")
    for step in analysis["next_steps"]:
        print(f"- {step}")

    print("=================================\n")


# =========================================================
# ORION CORE
# =========================================================
def main():
    parser = argparse.ArgumentParser(
        description="ORION Framework - Passive Intelligence & Analysis"
    )
    parser.add_argument(
        "domain",
        help="Target domain (e.g. example.com)"
    )

    args = parser.parse_args()
    domain = args.domain

    print(f"[CORE] Domain received: {domain}")

    recon_data = recon_module(domain)
    processed_data = processing_module(recon_data)

    normalized_data = normalization_module(processed_data)
    correlations = correlation_module(normalized_data)

    infra_profile = analyze_infrastructure(normalized_data)

    exposure_context = analyze_exposure_context(infra_profile, correlations)

    human_context = analyze_human_correlation(
    infra_profile,
    exposure_context
    )

    narrative_report = generate_narrative_report(
    domain=domain,
    infra_profile=infra_profile,
    exposure_context=exposure_context,
    human_context=human_context
    )

    analysis = risk_analysis_module(normalized_data, correlations)

    # OUTPUT
    output_module(normalized_data, analysis)
    
    #DEBUG TEMPORÁRIO DENTRO DO MAIN
    print("\n[DEBUG] Exposure Context:")
    print(f"  Level: {exposure_context['exposure_level']}")
    print(f"  Posture: {exposure_context['posture']}")
    print(f"  Interpretation: {exposure_context['interpretation']}")

    print("\n[DEBUG] Human Correlation Analysis:")
    for signal in human_context["human_signals"]:
        print(f"- Signal: {signal}")

    print(f"Risk Bias: {human_context['risk_bias']}")

    print("\n========== ORION NARRATIVE REPORT ==========\n")
    print(narrative_report)
    print("\n===========================================")

if __name__ == "__main__":
    main()
