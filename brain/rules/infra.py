from typing import Dict, Any

from .base import (
    BaseRule,
    RuleResult,
    RuleStatus,
    SignalWeight,
    ConfidenceLevel
)


class InfraTypeInferenceRule(BaseRule):
    """
    Inferência básica do tipo de infraestrutura:
    cloud vs on-prem vs indefinido.
    """

    name = "infra_type_inference"
    category = "infra"
    required_signals = ["asn", "isp"]

    CLOUD_KEYWORDS = [
        "amazon",
        "aws",
        "google",
        "gcp",
        "azure",
        "microsoft",
        "digitalocean",
        "oracle",
        "alibaba"
    ]

    def apply(self, signals: Dict[str, Any]) -> RuleResult:
        if not self.can_apply(signals):
            return RuleResult(
                rule_name=self.name,
                category=self.category,
                status=RuleStatus.SKIPPED
            )

        isp = str(signals.get("isp", "")).lower()
        asn = str(signals.get("asn", "")).lower()

        infra_type = "unknown"
        confidence = ConfidenceLevel.LOW

        for keyword in self.CLOUD_KEYWORDS:
            if keyword in isp or keyword in asn:
                infra_type = "cloud"
                confidence = ConfidenceLevel.HIGH
                break

        if infra_type == "unknown":
            infra_type = "on-prem"
            confidence = ConfidenceLevel.MEDIUM

        return RuleResult(
            rule_name=self.name,
            category=self.category,
            status=RuleStatus.APPLIED,
            interpretation=f"Infrastructure type inferred as '{infra_type}'",
            details={
                "infra_type": infra_type,
                "isp": isp,
                "asn": asn
            },
            weight=SignalWeight.MEDIUM,
            confidence=confidence
        )


class InfraStandardizationInferenceRule(BaseRule):
    """
    Inferência de padronização da infraestrutura:
    padronizada vs fragmentada vs indefinida.
    """

    name = "infra_standardization_inference"
    category = "infra"
    required_signals = ["hosting_providers"]

    def apply(self, signals: Dict[str, Any]) -> RuleResult:
        if not self.can_apply(signals):
            return RuleResult(
                rule_name=self.name,
                category=self.category,
                status=RuleStatus.SKIPPED
            )

        providers: List[str] = signals.get("hosting_providers", [])

        # Normalização defensiva
        providers = [str(p).lower() for p in providers if p]

        unique_providers = set(providers)
        provider_count = len(unique_providers)

        infra_pattern = "unknown"
        confidence = ConfidenceLevel.LOW

        if provider_count == 0:
            infra_pattern = "unknown"
            confidence = ConfidenceLevel.LOW

        elif provider_count == 1:
            infra_pattern = "standardized"
            confidence = ConfidenceLevel.HIGH

        elif provider_count <= 3:
            infra_pattern = "mostly-standardized"
            confidence = ConfidenceLevel.MEDIUM

        else:
            infra_pattern = "fragmented"
            confidence = ConfidenceLevel.MEDIUM

        return RuleResult(
            rule_name=self.name,
            category=self.category,
            status=RuleStatus.APPLIED,
            interpretation=f"Infrastructure pattern inferred as '{infra_pattern}'",
            details={
                "infra_pattern": infra_pattern,
                "unique_providers": list(unique_providers),
                "provider_count": provider_count
            },
            weight=SignalWeight.MEDIUM,
            confidence=confidence
        )


class InfraExternalDependencyInferenceRule(BaseRule):
    """
    Inferência de dependência de serviços externos / terceiros.
    """

    name = "infra_external_dependency_inference"
    category = "infra"
    required_signals = ["third_party_services"]

    def apply(self, signals: Dict[str, Any]) -> RuleResult:
        if not self.can_apply(signals):
            return RuleResult(
                rule_name=self.name,
                category=self.category,
                status=RuleStatus.SKIPPED
            )

        third_party_services: List[str] = signals.get("third_party_services", [])

        # Normalização defensiva
        third_party_services = [
            str(s).lower() for s in third_party_services if s
        ]

        dependency_level = "unknown"
        confidence = ConfidenceLevel.LOW

        service_count = len(set(third_party_services))

        if service_count == 0:
            dependency_level = "low"
            confidence = ConfidenceLevel.MEDIUM

        elif service_count <= 2:
            dependency_level = "moderate"
            confidence = ConfidenceLevel.MEDIUM

        else:
            dependency_level = "high"
            confidence = ConfidenceLevel.HIGH

        return RuleResult(
            rule_name=self.name,
            category=self.category,
            status=RuleStatus.APPLIED,
            interpretation=f"External dependency inferred as '{dependency_level}'",
            details={
                "dependency_level": dependency_level,
                "services": list(set(third_party_services)),
                "service_count": service_count
            },
            weight=SignalWeight.MEDIUM,
            confidence=confidence
        )