from brain.hypotheses import Hypothesis


class Rule:
    """
    Regra abstrata.
    Nunca contém lógica concreta de mundo real.
    """
    name = "base_rule"
    category = None

    def apply(self, signals):
        """
        Recebe uma lista de Signal
        Retorna Hypothesis ou None
        """
        raise NotImplementedError