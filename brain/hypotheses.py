class Signal:
    """
    Representa um fato observável ou ausência relevante.
    Não contém interpretação.
    """

    def __init__(self, name, value, signal_type, strength):
        self.name = name                  # ex: "asn_type", "subdomain_count"
        self.value = value                # ex: "public_cloud", 0
        self.signal_type = signal_type    # structural, behavioral, residual, absence
        self.strength = strength          # weak, medium, strong

    def __repr__(self):
        return f"<Signal {self.name}={self.value} ({self.signal_type})>"