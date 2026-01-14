# core/models.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Asset:
    domain: str
    ip: Optional[str] = None
    status_code: Optional[int] = None
    technologies: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    attack_interest_score: float = 0.0
    score_reasons: List[str] = field(default_factory=list)

    def summary(self):
        # Cores para o Score: Vermelho (Alto), Amarelo (Médio), Verde (Baixo)
        if self.attack_interest_score >= 80:
            color = "\033[91m"  # Red
        elif self.attack_interest_score >= 50:
            color = "\033[93m"  # Yellow
        else:
            color = "\033[92m"  # Green
            
        reset = "\033[0m"
        techs = ", ".join(self.technologies) if self.technologies else "no tech detected"
        
        return f"[{color}{self.attack_interest_score:>3}{reset}] {self.domain:30} | Tech: {techs}"