# orion.py
import sys
import argparse
from core.models import Asset

def banner():
    print("""
    █▀█ █▀█ █ █▀█ █▄░█
    █▄█ █▀▄ █ █▄█ █░▀█  Offensive Recon Intelligence Engine
    """)
def main():
    banner()
    
    # Configuração do Argument Parser
    parser = argparse.ArgumentParser(description="ORION - Offensive Recon Intelligence Engine")
    parser.add_argument("target", help="Target domain to analyze (e.g., target.com)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    target_domain = args.target

    print(f"[*] Starting intelligent analysis for: \033[1m{target_domain}\033[0m")
    print("-" * 65)
    print(f"{'SCORE':<5} | {'DOMAIN':<30} | {'TECHNOLOGIES'}")
    print("-" * 65)

    # SIMULAÇÃO: Dados mockados para testar a interface (Etapa 1.1)
    # Na Etapa 1.3, esses dados virão de ferramentas de recon reais
    mock_assets = [
        Asset(domain=f"dev-api.{target_domain}", technologies=["Node.js", "Express"], attack_interest_score=85),
        Asset(domain=f"staging.{target_domain}", technologies=["PHP 7.4", "Laravel"], attack_interest_score=92),
        Asset(domain=f"www.{target_domain}", technologies=["Cloudflare", "React"], attack_interest_score=15),
        Asset(domain=f"internal-docs.{target_domain}", technologies=["WordPress"], attack_interest_score=65),
    ]

    # Ordenar por Score (maior primeiro)
    sorted_assets = sorted(mock_assets, key=lambda x: x.attack_interest_score, reverse=True)

    for asset in sorted_assets:
        print(asset.summary())

    print("-" * 65)
    print(f"[*] Analysis complete. {len(mock_assets)} assets processed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(0)