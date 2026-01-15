# core/parsers.py
import json
from core.models import Asset

class HttpxParser:
    def parse(self, filepath):
        """Lê um arquivo JSON gerado pelo httpx (comando: httpx -json)"""
        assets = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    
                    # Mapeando os campos do HTTPX para o nosso modelo Asset
                    asset = Asset(
                        domain=data.get("input", data.get("url")),
                        ip=data.get("host"),
                        status_code=data.get("status_code"),
                        technologies=data.get("tech", []),
                        # Pegamos alguns headers úteis se existirem
                        headers=data.get("header", {})
                    )
                    assets.append(asset)
            return assets
        except FileNotFoundError:
            print(f"[!] Error: File {filepath} not found.")
            return []
        except Exception as e:
            print(f"[!] Error parsing HTTPX data: {e}")
            return []