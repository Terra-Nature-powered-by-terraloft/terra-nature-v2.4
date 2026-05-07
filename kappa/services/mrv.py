"""
MRV (Monitoring, Reporting, Verification) Validation Service
Ensures compliance with regulatory and carbon credit standards
"""

import re
from typing import Tuple, List, Dict
from dataclasses import dataclass
from datetime import datetime

from ..utils.logging import logger


@dataclass
class MRVCheckResult:
    """Result of MRV compliance check"""
    compliant: bool
    confidence: float
    issues: List[str]
    requirements: List[str]
    recommendations: List[str]


class MRVValidator:
    """MRV compliance validation"""

    def __init__(self):
        """Initialize MRV validator"""
        logger.info("mrv_validator_init")

    async def check_co2_statement(self, statement: str) -> MRVCheckResult:
        """
        Check CO₂-related statements for MRV compliance

        Requirements:
        - Datentimestamp erforderlich
        - Quelle des Messwerts dokumentiert
        - Audit-Trail verfügbar
        - EU-ETS/UN-Standard kompatibel
        """
        issues = []
        requirements = []
        confidence = 1.0

        # Check for CO₂ quantity
        co2_match = re.search(r"(\d+\.?\d*)\s*t(onne)?s?\s*co[2₂]", statement, re.IGNORECASE)
        if not co2_match:
            issues.append("Keine CO₂-Menge angegeben")
            confidence -= 0.3
        else:
            co2_value = float(co2_match.group(1))
            if co2_value < 0:
                issues.append("Negative CO₂-Menge nicht plausibel")
                confidence -= 0.5
            elif co2_value > 10000:
                issues.append("CO₂-Menge über 10.000t sollte belegt sein")
                confidence -= 0.1

        # Check for timestamp
        date_pattern = r"\d{4}-\d{2}-\d{2}|(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})"
        if not re.search(date_pattern, statement):
            issues.append("Zeitstempel / Messdatum fehlt")
            requirements.append("Angabe von Messdatum im Format YYYY-MM-DD erforderlich")
            confidence -= 0.4
        else:
            confidence += 0.1

        # Check for measurement source/method
        method_keywords = ["messung", "berechnung", "monitoring", "sensor", "meter"]
        if not any(kw in statement.lower() for kw in method_keywords):
            issues.append("Messmethode nicht dokumentiert")
            requirements.append("Beschreibung der Messmethode erforderlich (z.B. 'direkte Messung', 'Berechnung')")
            confidence -= 0.3

        # Check for data quality indicators
        quality_keywords = ["genauigkeit", "unsicherheit", "fehler", "toleranz", "kalibrierung"]
        if not any(kw in statement.lower() for kw in quality_keywords):
            issues.append("Datenqualität / Genauigkeit nicht angegeben")
            requirements.append("Angabe der Messunsicherheit oder Genauigkeitsklasse erforderlich")
            confidence -= 0.2

        # Check for audit trail capability
        audit_keywords = ["audit", "prüfung", "dokumentation", "nachvollziehbar", "rückverfolgbar"]
        if not any(kw in statement.lower() for kw in audit_keywords):
            issues.append("Audit-Trail nicht erwähnt")
            requirements.append("Dokumentation muss Third-Party Audit ermöglichen")
            confidence -= 0.1

        compliant = len(issues) == 0

        logger.info(
            "mrv_co2_check",
            compliant=compliant,
            confidence=confidence,
            issue_count=len(issues),
        )

        return MRVCheckResult(
            compliant=compliant,
            confidence=max(0.0, confidence),
            issues=issues,
            requirements=requirements,
            recommendations=self._get_mrv_recommendations("co2", issues),
        )

    async def check_energy_statement(self, statement: str) -> MRVCheckResult:
        """
        Check energy-related statements for MRV compliance
        """
        issues = []
        requirements = []
        confidence = 1.0

        # Check for energy quantity with unit
        energy_match = re.search(
            r"(\d+\.?\d*)\s*(kWh|MWh|kW|MW|joule|kJ|MJ)",
            statement,
            re.IGNORECASE
        )
        if not energy_match:
            issues.append("Keine Energiemenge mit Einheit angegeben")
            confidence -= 0.4
        else:
            confidence += 0.1

        # Check for time period
        if not re.search(r"(pro|per|täglich|daily|stündlich|hourly|jährlich|yearly)", statement, re.IGNORECASE):
            issues.append("Zeitraum für Energiemenge nicht angegeben")
            requirements.append("Angabe der zeitlichen Bezug erforderlich (täglich, monatlich, jährlich)")
            confidence -= 0.3

        # Check for efficiency claims
        if "effizienz" in statement.lower():
            eff_match = re.search(r"(\d+\.?\d*)\s*%", statement)
            if eff_match:
                eff_value = float(eff_match.group(1))
                if eff_value > 100:
                    issues.append("Effizienz >100% ist physikalisch unmöglich")
                    confidence -= 0.5
                elif eff_value > 50 and "ORC" in statement:
                    issues.append("ORC-Effizienz >50% sehr unwahrscheinlich")
                    requirements.append("Test-Daten oder externe Validierung erforderlich")
                    confidence -= 0.3

        compliant = len(issues) == 0

        logger.info(
            "mrv_energy_check",
            compliant=compliant,
            confidence=confidence,
            issue_count=len(issues),
        )

        return MRVCheckResult(
            compliant=compliant,
            confidence=max(0.0, confidence),
            issues=issues,
            requirements=requirements,
            recommendations=self._get_mrv_recommendations("energy", issues),
        )

    async def check_additionality(self, statement: str) -> MRVCheckResult:
        """
        Check whether CO₂-reduction is additional (not baseline)
        """
        issues = []
        requirements = []
        confidence = 1.0

        # Check for baseline comparison
        baseline_keywords = ["baseline", "referenz", "geschäftsüblich", "business-as-usual"]
        if not any(kw in statement.lower() for kw in baseline_keywords):
            issues.append("Baseline / Referenzszenario nicht definiert")
            requirements.append("Detaillierte Baseline-Dokumentation erforderlich (BAU-Szenario)")
            confidence -= 0.4
        else:
            confidence += 0.2

        # Check for additionality evidence
        additionality_keywords = ["zusätzlich", "additional", "ohne", "würde nicht", "barriere"]
        if not any(kw in statement.lower() for kw in additionality_keywords):
            issues.append("Additionality nicht nachgewiesen")
            requirements.append("Dokumentation, dass die Reduktion ohne Projekt nicht stattgefunden hätte")
            confidence -= 0.3

        compliant = len(issues) == 0

        logger.info(
            "mrv_additionality_check",
            compliant=compliant,
            confidence=confidence,
        )

        return MRVCheckResult(
            compliant=compliant,
            confidence=max(0.0, confidence),
            issues=issues,
            requirements=requirements,
            recommendations=self._get_mrv_recommendations("additionality", issues),
        )

    async def check_leakage(self, statement: str) -> MRVCheckResult:
        """
        Check whether leakage (emissions shifts) are accounted for
        """
        issues = []
        requirements = []
        confidence = 1.0

        # Check for leakage consideration
        leakage_keywords = ["leakage", "leckage", "verschiebung", "versatz", "indirekt"]
        if not any(kw in statement.lower() for kw in leakage_keywords):
            issues.append("Leakage nicht berücksichtigt")
            requirements.append("Dokumentation der Leakage-Betrachtung erforderlich")
            confidence -= 0.2
        else:
            confidence += 0.15

        compliant = len(issues) == 0

        logger.info(
            "mrv_leakage_check",
            compliant=compliant,
            confidence=confidence,
        )

        return MRVCheckResult(
            compliant=compliant,
            confidence=max(0.0, confidence),
            issues=issues,
            requirements=requirements,
            recommendations=self._get_mrv_recommendations("leakage", issues),
        )

    def _get_mrv_recommendations(self, check_type: str, issues: List[str]) -> List[str]:
        """Generate MRV recommendations based on issues found"""
        recommendations = []

        if not issues:
            recommendations.append("✓ MRV-Konformität hergestellt")
            return recommendations

        if check_type == "co2":
            if any("Zeitstempel" in issue for issue in issues):
                recommendations.append("Nutze ISO 8601 Format: YYYY-MM-DD")
            if any("Messmethode" in issue for issue in issues):
                recommendations.append("Dokumentiere Sensor-Typ und Messgenauigkeit")
            if any("Datenqualität" in issue for issue in issues):
                recommendations.append("Angabe der Messunsicherheit (z.B. ±5%)")

        elif check_type == "energy":
            if any("Zeitraum" in issue for issue in issues):
                recommendations.append("Nutze konsistente Zeiteinheiten (kWh/Tag oder kWh/Jahr)")
            if any("Effizienz" in issue for issue in issues):
                recommendations.append("Laborprotokolle oder Feldmessungen beilegen")

        elif check_type == "additionality":
            recommendations.append("Dokumentiere Investment Barriers und Profit Margin Analysis")
            recommendations.append("Vergleich mit Marktüblichem Standard (TA-Luft, beste Praxis)")

        elif check_type == "leakage":
            recommendations.append("Systembegrenzung klar definieren")
            recommendations.append("Indirekte Effekte (z.B. Strombezug) einbeziehen")

        return recommendations


# Global MRV validator instance
mrv_validator = MRVValidator()
