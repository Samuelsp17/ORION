from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# =========================
# ENUMS BÁSICOS
# =========================

class ConfidenceLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SignalWeight(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RuleStatus(Enum):
    APPLIED = "applied"
    SKIPPED = "skipped"
    CONFLICT = "conflict"


# =========================
# RESULTADO PADRÃO DE REGRA
# =========================

@dataclass
class RuleResult:
    rule_name: str
    category: str
    status: RuleStatus

    interpretation: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    weight: SignalWeight = SignalWeight.LOW
    confidence: ConfidenceLevel = ConfidenceLevel.LOW

    conflicts_with: Optional[List[str]] = None


# =========================
# CLASSE BASE DE REGRA
# =========================

class BaseRule(ABC):
    


    name: str = "undefined-rule"
    category: str = "generic"
    required_signals: List[str] = []

    def __init__(self):
        if not self.name or self.name == "undefined-rule":
            raise ValueError("Rule must define a unique 'name'")
        if not self.category:
            raise ValueError("Rule must define a 'category'")

    def can_apply(self, signals: Dict[str, Any]) -> bool:
        """
        Verifica se os sinais necessários estão presentes.
        """
        return all(signal in signals for signal in self.required_signals)

    @abstractmethod
    def apply(self, signals: Dict[str, Any]) -> RuleResult:
        """
        Aplica a regra sobre os sinais e retorna um RuleResult.
        """
        pass