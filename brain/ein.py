class ExpandedIntelligenceMap:
    """
    Mapa de inteligência expandida da FASE 3.1
    """

    def __init__(self, meta):
        self.meta = meta
        self.hypotheses = []

    def add_hypothesis(self, hypothesis):
        if hypothesis:
            self.hypotheses.append(hypothesis)

    def get_by_category(self, category):
        return [h for h in self.hypotheses if h.category == category]

    def __repr__(self):
        return f"<EIM hypotheses={len(self.hypotheses)}>"