class IntelligenceExpansionEngine:
    def __init__(self, rules):
        self.rules = rules

    def run(self, signals, meta):
        eim = ExpandedIntelligenceMap(meta)

        for rule in self.rules:
            hypothesis = rule.apply(signals)
            if hypothesis:
                eim.add_hypothesis(hypothesis)

        return eim