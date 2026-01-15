# core/scorer.py

class Scorer:
    def __init__(self):
        # Palavras-chave que indicam alvos de alto valor
        self.high_value_keywords = {
            "dev": 25, "staging": 20, "test": 15, "api": 15,
            "vpn": 30, "admin": 25, "jenkins": 30, "jira": 20,
            "grafana": 20, "internal": 25, "git": 20, "backup": 25
        }
        
        # Tecnologias que geralmente possuem mais vetores de ataque ou são críticas
        self.critical_techs = {
            "WordPress": 10, "php": 15, "IIS": 10, "Jenkins": 25,
            "Docker": 5, "Kubernetes": 10
        }

    def calculate_score(self, asset):
        """Calcula o Attack Interest Score e armazena os motivos."""
        score = 10.0  # Pontuação base para qualquer ativo encontrado
        reasons = []

        # 1. Análise de Keywords no Domínio
        for word, points in self.high_value_keywords.items():
            if word in asset.domain.lower():
                score += points
                reasons.append(f"Keyword '{word}' detected in domain")

        # 2. Análise de Tecnologias
        for tech in asset.technologies:
            for crit_tech, points in self.critical_techs.items():
                if crit_tech.lower() in tech.lower():
                    score += points
                    reasons.append(f"Critical technology '{crit_tech}' detected")

        # 3. Análise de Status Code
        if asset.status_code == 403:
            score += 15
            reasons.append("Forbidden (403) may indicate protected interesting content")
        elif asset.status_code == 401:
            score += 20
            reasons.append("Unauthorized (401) indicates an authentication barrier")

        # Limitar o score a 100
        asset.attack_interest_score = min(score, 100)
        asset.score_reasons = reasons
        return asset