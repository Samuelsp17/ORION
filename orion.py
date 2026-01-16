# orion.py
import os
import sys
import argparse
from dotenv import load_dotenv

from core.models import Asset
from core.scorer import Scorer
from core.parsers import HttpxParser
from core.ai_assistant import AIAssistant
from core.orchestrator import Orchestrator 
from core.reporter import Reporter

load_dotenv()



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
    
    # 1. Obtenção dos Dados (Orquestração ou Arquivo)
    if args.file:
        results_path = args.file
    else:
        # Se não passou arquivo, o ORION assume o comando e faz o scan real
        orchestrator = Orchestrator(args.target)
        success = orchestrator.run_full_scan()
        if not success:
            sys.exit(1)
        results_path = "results.json"

    # 2. Parsing (Lê o que foi gerado ou o que já existia)
    parser_engine = HttpxParser()
    raw_assets = parser_engine.parse(results_path)

    if not raw_assets:
        print("[!] No assets discovered. Try a different target.")
        return

    # 3. Scoring e IA
    scorer = Scorer()
    assistant = AIAssistant()
    
    processed_assets = [scorer.calculate_score(a) for a in raw_assets]
    sorted_assets = sorted(processed_assets, key=lambda x: x.attack_interest_score, reverse=True)
    scorer = Scorer()
    
    # Decidindo a fonte dos dados
    # Se o usuário não passou um arquivo pronto (-f), o Orquestrador roda
    if not args.file:
        orchestrator = Orchestrator(args.target)
        success = orchestrator.run_full_scan() # Isso cria o results.json
        if not success:
            print("[!] Orchestration failed.")
            sys.exit(1)
        
        # Definimos que o arquivo a ser lido é o que acabou de ser criado
        results_path = "results.json"
    else:
        # Se o usuário usou -f, usamos o arquivo que ele indicou
        results_path = args.file

    # AGORA: Tentamos carregar os dados reais
    if os.path.exists(results_path):
        print(f"[*] Parsing discovered assets from: {results_path}")
        parser_engine = HttpxParser()
        raw_assets = parser_engine.parse(results_path)
    else:
        # Só cai aqui se o arquivo sumir ou o scan falhar totalmente
        print("[!] Target file not found. Using sample mock data...")
        raw_assets = [
            Asset(domain=f"dev-api.{args.target}", technologies=["Node.js"], status_code=200),
            Asset(domain=f"jenkins.{args.target}", technologies=["Jenkins"], status_code=403)
        ]
    
    if args.file:
        results_path = args.file
    else:
        orchestrator = Orchestrator(args.target)
        # Alterado de run_httpx para run_full_scan
        success = orchestrator.run_full_scan() 
        if not success:
            sys.exit(1)
        results_path = "results.json"

    # Processamento e Display (o resto permanece igual)
    processed_assets = [scorer.calculate_score(a) for a in raw_assets]
    sorted_assets = sorted(processed_assets, key=lambda x: x.attack_interest_score, reverse=True)

    # Inicializa o assistente (pode pegar a chave de uma variável de ambiente)
    assistant = AIAssistant(api_key=os.getenv("ORION_AI_KEY"))

    print(f"[*] Analyzing {len(processed_assets)} assets...")
    print("-" * 75)
    
    for asset in sorted_assets:
        print(asset.summary())
        
        # Se o score for alto e o verbose estiver ativo, chama a IA
        if args.verbose and asset.attack_interest_score >= 70:
            if assistant.enabled:
                explanation = assistant.explain_asset(asset)
                print(f"   \033[94m└── {explanation}\033[0m")
            
            for reason in asset.score_reasons:
                print(f"   └── \033[2m{reason}\033[0m")
        
        reporter = Reporter(args.target, sorted_assets)
        reporter.generate()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(0)