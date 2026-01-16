# core/orchestrator.py
import subprocess
import os
import sys

class Orchestrator:
    def __init__(self, target_domain):
        self.target = target_domain
        self.output_file = "results.json"

    def run_full_scan(self):
        """Roda Subfinder e passa a saída para o HTTPX com saída limpa."""
        print(f"[*] Starting full orchestration for: {self.target}")
        
        try:
            # 1. Subfinder: -silent garante que ele SÓ envie os domínios pelo pipe (|)
            subfinder_cmd = f"subfinder -d {self.target} -silent"
            
            # 2. HTTPX: 
            # -json -o: Salva tudo detalhado no arquivo para a IA e o Scorer
            # -silent: Não mostra o JSON bruto na tela
            # No final, usamos uma técnica de "echo" ou apenas deixamos o httpx mostrar o status
            httpx_cmd = f"httpx -json -silent -o {self.output_file} -status-code -ip -no-color"

            full_command = f"{subfinder_cmd} | {httpx_cmd}"
            
            print(f"[*] Reconnaissance started. Finding and probing assets...")
            print("-" * 60)
            
            # Executa o comando. Agora a saída no terminal será limpa: "URL [PORT] [IP] [STATUS]"
            subprocess.run(full_command, shell=True, check=True)
            
            print("-" * 60)
            print(f"[+] Data saved to {self.output_file}")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"[!] Error during tool execution: {e}")
            return False
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            return False