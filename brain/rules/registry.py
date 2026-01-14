import inspect
from typing import List, Dict, Type

from .base import BaseRule


class RuleRegistry:
    """
    Registro central de regras do ORION.
    Responsável apenas por descobrir e instanciar regras.
    """

    def __init__(self):
        self._rules: List[BaseRule] = []

    def register(self, rule: BaseRule):
        """
        Registra manualmente uma regra.
        """
        self._rules.append(rule)

    def load_from_module(self, module):
        """
        Carrega automaticamente regras de um módulo (infra, exposure, etc).
        """
        for _, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseRule)
                and obj is not BaseRule
            ):
                self.register(obj())

    def get_all(self) -> List[BaseRule]:
        return self._rules

    def get_by_category(self, category: str) -> List[BaseRule]:
        return [r for r in self._rules if r.category == category]

    def summary(self) -> Dict[str, int]:
        """
        Retorna um resumo simples das regras carregadas.
        """
        result = {}
        for rule in self._rules:
            result.setdefault(rule.category, 0)
            result[rule.category] += 1
        return result