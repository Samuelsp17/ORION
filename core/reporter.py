# core/reporter.py
import datetime

class Reporter:
    def __init__(self, target, assets):
        self.target = target
        self.assets = assets
        self.report_name = f"report_{target}_{datetime.date.today()}.html"

    def generate(self):
        html_content = f"""
        <html>
        <head>
            <title>ORION Report - {self.target}</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #eee; padding: 40px; }}
                .card {{ background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid #007bff; }}
                .high-score {{ border-left: 5px solid #ff4757; }}
                h1 {{ color: #007bff; }}
                .score {{ font-weight: bold; color: #ffa502; }}
                .tech {{ background: #444; padding: 2px 8px; border-radius: 4px; font-size: 0.9em; }}
                .ai-insight {{ font-style: italic; color: #7bed9f; margin-top: 10px; border-top: 1px solid #444; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <h1>ORION Intelligence Report: {self.target}</h1>
            <p>Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <hr>
        """

        for asset in self.assets:
            card_class = "card high-score" if asset.attack_interest_score >= 70 else "card"
            techs = " ".join([f'<span class="tech">{t}</span>' for t in asset.technologies])
            
            # Aqui pegamos a última linha que foi o insight da IA
            ai_text = getattr(asset, 'ai_insight', 'No AI analysis available.')

            html_content += f"""
            <div class="{card_class}">
                <h3>{asset.domain} <span class="score">[{asset.attack_interest_score}]</span></h3>
                <p><strong>Status:</strong> {asset.status_code} | <strong>Technologies:</strong> {techs}</p>
                <div class="ai-insight"><strong>AI Strategy:</strong> {ai_text}</div>
            </div>
            """

        html_content += "</body></html>"
        
        with open(self.report_name, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Report generated: {self.report_name}")