from typing import Dict, Any, List

from brain.ein import ExpandedIntelligenceMap
from rules.registry import RuleRegistry
from rules.base import RuleResult

from rules import infra
# futuramente: exposure, stability, similarity


class IntelligenceExpansionEngine:
    """
    Motor de expansão de inteligência (FASE 3.1)

    Responsável apenas por:
    - aplicar regras
    - coletar interpretações
    """

    def __init__(self):
        self.registry = RuleRegistry()
        self._load_rules()

    def _load_rules(self):
        self.registry.load_from_module(infra)

    def run(self, signals: Dict[str, Any], meta: Dict[str, Any]) -> ExpandedIntelligenceMap:
        eim = ExpandedIntelligenceMap(meta)

        for rule in self.registry.get_all():
            result: RuleResult = rule.apply(signals)

            # FASE 3.1: só adicionamos resultados válidos
            if result and result.status.name != "SKIPPED":
                eim.add_interpretation(result)

        return eim
