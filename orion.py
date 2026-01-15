# orion.py
import sys
import argparse
from core.models import Asset
from core.scorer import Scorer # inmportando o novo motor
from core.parsers import HttpxParser


def banner():
    print("""
    █▀█ █▀█ █ █▀█ █▄░█
    █▄█ █▀▄ █ █▄█ █░▀█  Offensive Recon Intelligence Engine
    """)
def main():
    banner()
    parser = argparse.ArgumentParser(description="ORION - Offensive Recon Intelligence Engine")
    parser.add_argument("target", help="Target domain (for reference)")
    parser.add_argument("-f", "--file", help="Path to httpx JSON output file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show scoring reasons")
    
    args = parser.parse_args()
    scorer = Scorer()
    
    # Decidindo a fonte dos dados
    if args.file:
        print(f"[*] Loading data from: {args.file}")
        parser_engine = HttpxParser()
        raw_assets = parser_engine.parse(args.file)
    else:
        # Mantém o mock apenas se nenhum arquivo for passado, para fins de teste
        print("[!] No input file provided. Using sample mock data...")
        raw_assets = [
            Asset(domain=f"dev-api.{args.target}", technologies=["Node.js"], status_code=200),
            Asset(domain=f"jenkins.{args.target}", technologies=["Jenkins"], status_code=403)
        ]

    # Processamento e Display (o resto permanece igual)
    processed_assets = [scorer.calculate_score(a) for a in raw_assets]
    sorted_assets = sorted(processed_assets, key=lambda x: x.attack_interest_score, reverse=True)

    print(f"[*] Analyzing {len(processed_assets)} assets...")
    print("-" * 75)
    for asset in sorted_assets:
        print(asset.summary())
        if args.verbose:
            for reason in asset.score_reasons:
                print(f"   └── \033[2m{reason}\033[0m")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(0)