# core/ai_assistant.py
from groq import Groq
import os

class AIAssistant:
    def __init__(self, api_key: str = None):
        # 1. Tenta a chave passada por argumento
        # 2. Se não houver, tenta pegar do ambiente (carregado pelo .env)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                self.enabled = True
            except Exception as e:
                print(f"[!] Error initializing Groq client: {e}")
                self.enabled = False
        else:
            self.enabled = False

    def explain_asset(self, asset):
        """Usa o Llama-3 para gerar insights ofensivos curtos."""
        if not self.enabled:
            return "AI analysis disabled. (Check your GROQ_API_KEY)"

        # Prompt otimizado para ser curto e técnico
        prompt = f"""
        Analyze this recon data as a Red Teamer:
        Asset: {asset.domain}
        Status: {asset.status_code}
        Tech: {', '.join(asset.technologies)}
        
        In one short sentence, what is the most likely attack vector or reason to prioritize this?
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a concise offensive security assistant. Provide only technical insights."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1, # Menos criatividade, mais precisão técnica
                max_tokens=100   # Economiza sua cota da API
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error: {e}"