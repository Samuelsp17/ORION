#!/usr/bin/env python3
import sys
import argparse
import socket
import subprocess 
import requests

# =========================================================
# MODULE: COLLECTION (RECON)
# =========================================================
def recon_module(domain):
    print("[RECON] Starting information collection...")
    # Placeholder: no real collection yet
    recon_data = {
        "domain": domain,
        "dns": {},
        "ip": None,
        "http_hearders": {},
    }

    # DNS / IP resolution
    try:
        ip = socket.gethostbyname(domain)
        recon_data["ip"] = ip
    except Exception as e:
        recon_data["ip"] = None

    # Basic DNS records via system (nslookup)
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
            "server": recon_data["http_headers"].get("Server", "Unknown")
        }
    }

    print("[PROCESSING] Data organized.")
    return processed


# =========================================================
# MODULE: ANALYSIS (HEURISTIC)
# =========================================================
def ai_analysis_module(processed_data):
    print("[AI] Starting intelligent analysis...")

    observations = []
    headers = processed_data["web"]["headers"]

    if processed_data["web"]["server"] != "Unknown":
        observations.append(
            f"Web server identified: {processed_data['web']['server']}"
        )

    if "X-Powered-By" in headers:
        observations.append(
            f"Technology disclosure via X-Powered-By: {headers['X-Powered-By']}"
        )

    if not observations:
        observations.append("No obvious surface indicators detected yet.")

    analysis = {
        "summary": "Passive surface observation completed.",
        "observations": observations,
        "next_steps": [
            "Expand DNS record parsing",
            "Add subdomain enumeration (passive)",
            "Introduce port discovery (light scan)"
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

    print("\nObservations:")
    for obs in analysis["observations"]:
        print(f"- {obs}")

    print("\nSuggested next steps:")
    for step in analysis["next_steps"]:
        print(f"- {step}")

    print("=================================\n")


# =========================================================
# ORION CORE
# =========================================================
def main():
    parser = argparse.ArgumentParser(
        description="ORION Framework - Passive Attack Surface Mapping"
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
    analysis = ai_analysis_module(processed_data)
    output_module(processed_data, analysis)


if __name__ == "__main__":
    main()