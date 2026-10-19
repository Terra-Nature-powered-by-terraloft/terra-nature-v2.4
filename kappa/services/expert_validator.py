"""
Expert Validator Service
Multi-perspective expert validation framework with Claude integration
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

from ..config import config
from ..utils.logging import logger


# Fail-Closed-Grundsatz: Eine Aussage gilt nur dann als "approved", wenn sie
# tatsächlich von den angefragten Experten geprüft wurde. Fehlt die Prüfung
# (kein API-Schlüssel, Timeout, Modellfehler, unlesbare Antwort), lautet das
# Ergebnis "not_validated" bzw. bei Teilausfall "requires_review" – nie "approved".
NOT_VALIDATED = "not_validated"

# Maximale Wartezeit pro Expertenanfrage in Sekunden
EXPERT_REQUEST_TIMEOUT_S = 60.0


@dataclass
class ExpertOpinion:
    """Single expert's validation result"""
    expert: str
    name: str
    approved: bool
    confidence: float
    feedback: str
    suggestions: List[str]
    conditions: List[str]
    reasoning: str
    # False, wenn keine echte Prüfung stattgefunden hat (Fehler, Timeout,
    # fehlender API-Schlüssel, unlesbare Modellantwort)
    validated: bool = True


@dataclass
class ValidationResult:
    """Complete validation across all experts"""
    statement: str
    timestamp: str
    expert_opinions: Dict[str, ExpertOpinion]
    overall_approved: bool
    approval_level: str  # "approved", "conditional", "requires_review", "not_validated"
    suggestions: List[str]
    conditions: List[str]


class ExpertValidator:
    """Multi-expert validation engine using Claude"""

    def __init__(self):
        """Initialize expert validator"""
        self.api_key = config.anthropic_api_key
        self.available = bool(self.api_key)
        logger.info("expert_validator_init", available=self.available)

        # Expert definitions (9 perspectives)
        self.experts = {
            "professorale": {
                "name": "Akademische Bewertung",
                "description": "Wissenschaftliche Plausibilität und akademische Standards",
            },
            "cto": {
                "name": "Technische Realität (Dr.-Ing.)",
                "description": "Umsetzbarkeit, Ingenieursstandards, Praxis",
            },
            "mrv": {
                "name": "MRV-Konformität",
                "description": "Monitoring, Reporting, Verification für regulatorische Anforderungen",
            },
            "bank": {
                "name": "Bankfähigkeit",
                "description": "Finanzierbarkeit, KfW-Standards, Bonitätssicherung",
            },
            "funding": {
                "name": "Fördermittel-Eligibilität",
                "description": "Innovativität, EXIST/WIPANO/BayStartUP Kriterien",
            },
            "industrial": {
                "name": "Industriekundennutzen",
                "description": "Praktische Anwendbarkeit, ROI für Stadtwerke/MHKW",
            },
            "ip": {
                "name": "IP & Governance",
                "description": "Schutzrechte, Lizenzen, Governance-Struktur",
            },
            "communication": {
                "name": "Kommunikationseignung",
                "description": "Verständlichkeit, Marketing-Tauglichkeit, Glaubwürdigkeit",
            },
            "business": {
                "name": "Business Development",
                "description": "Marktpotential, Wachstumschancen, Strategische Positionierung",
            },
        }

    async def validate_statement(
        self,
        statement: str,
        modes: Optional[List[str]] = None,
        timestamp: str = ""
    ) -> ValidationResult:
        """
        Validate a statement against multiple expert perspectives

        Args:
            statement: The statement to validate
            modes: List of expert modes to validate against (None = all)
            timestamp: ISO timestamp of validation

        Returns:
            ValidationResult with all expert opinions
        """
        if not self.available:
            logger.warning("validation_attempted_without_api_key")
            return self._not_validated_result(
                statement,
                modes or list(self.experts.keys()),
                timestamp,
                reason="Kein API-Schlüssel konfiguriert – keine Prüfung durchgeführt",
            )

        # Determine which experts to consult
        expert_modes = modes or list(self.experts.keys())
        expert_opinions = {}

        # Gather opinions from each expert
        for expert_id in expert_modes:
            if expert_id not in self.experts:
                logger.warning("unknown_expert_mode", mode=expert_id)
                continue

            expert_info = self.experts[expert_id]
            opinion = await self._get_expert_opinion(
                expert_id, expert_info, statement
            )
            expert_opinions[expert_id] = opinion

        # Calculate aggregate approval (fail-closed)
        validated_count = sum(1 for op in expert_opinions.values() if op.validated)
        approved_count = sum(
            1 for op in expert_opinions.values() if op.validated and op.approved is True
        )
        approval_rate = approved_count / len(expert_opinions) if expert_opinions else 0

        if not expert_opinions or validated_count == 0:
            # Keine einzige echte Prüfung -> nie freigeben
            overall_approved = False
            approval_level = NOT_VALIDATED
        elif validated_count < len(expert_opinions):
            # Teilausfall: unvollständig geprüft -> menschliche Prüfung erforderlich
            overall_approved = False
            approval_level = "requires_review"
        elif approval_rate >= 0.8:
            overall_approved = True
            approval_level = "approved"
        elif approval_rate >= 0.5:
            overall_approved = False
            approval_level = "conditional"
        else:
            overall_approved = False
            approval_level = "requires_review"

        # Aggregate suggestions and conditions
        all_suggestions = []
        all_conditions = []
        for opinion in expert_opinions.values():
            all_suggestions.extend(opinion.suggestions)
            all_conditions.extend(opinion.conditions)

        result = ValidationResult(
            statement=statement,
            timestamp=timestamp,
            expert_opinions=expert_opinions,
            overall_approved=overall_approved,
            approval_level=approval_level,
            suggestions=list(set(all_suggestions)),  # Deduplicate
            conditions=list(set(all_conditions)),
        )

        logger.info(
            "validation_complete",
            approval_level=approval_level,
            approval_rate=approval_rate,
            experts_consulted=len(expert_opinions),
            experts_validated=validated_count,
        )

        return result

    async def _get_expert_opinion(
        self,
        expert_id: str,
        expert_info: Dict,
        statement: str
    ) -> ExpertOpinion:
        """Get a single expert's opinion on the statement"""
        try:
            import anthropic

            client = anthropic.Anthropic(
                api_key=self.api_key, timeout=EXPERT_REQUEST_TIMEOUT_S
            )

            prompt = f"""Du bist ein Experte für '{expert_info['name']}':
{expert_info['description']}

Bitte bewerte folgende Aussage aus Deiner Perspektive:

"{statement}"

Antworte mit einem JSON-Objekt mit:
{{
  "approved": true|false,
  "confidence": 0.0-1.0,
  "feedback": "Detailliertes Feedback",
  "suggestions": ["Verbesserungsvorschlag 1", "Vorschlag 2"],
  "conditions": ["Bedingung 1 für Genehmigung", "Bedingung 2"],
  "reasoning": "Ausführliche Begründung"
}}

Sei kritisch und konstruktiv. Identifiziere sowohl Stärken als auch Schwächen."""

            logger.info(
                "expert_opinion_requested",
                expert=expert_id,
                statement_length=len(statement),
            )

            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Parse JSON response – ohne gültiges JSON gibt es keine Prüfung.
            # (Früher wurde hier per Textsuche nach "approved" entschieden; dadurch
            # konnte z.B. "not approved" als Freigabe gewertet werden.)
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if not json_match:
                raise ValueError("Modellantwort enthält kein auswertbares JSON")
            opinion_data = json.loads(json_match.group())
            if not isinstance(opinion_data, dict):
                raise ValueError("Modellantwort ist kein JSON-Objekt")

            approved_raw = opinion_data.get("approved")
            if not isinstance(approved_raw, bool):
                raise ValueError(
                    f"Feld 'approved' fehlt oder ist kein Boolean: {approved_raw!r}"
                )

            confidence = float(opinion_data.get("confidence", 0.0))
            confidence = min(max(confidence, 0.0), 1.0)

            opinion = ExpertOpinion(
                expert=expert_id,
                name=expert_info["name"],
                approved=approved_raw,
                confidence=confidence,
                feedback=opinion_data.get("feedback", ""),
                suggestions=opinion_data.get("suggestions", []),
                conditions=opinion_data.get("conditions", []),
                reasoning=opinion_data.get("reasoning", ""),
            )

            logger.info(
                "expert_opinion_received",
                expert=expert_id,
                approved=opinion.approved,
                confidence=opinion.confidence,
            )

            return opinion

        except Exception as e:
            logger.error("expert_opinion_failed", expert=expert_id, error=str(e))
            # Fehler, Timeout oder unlesbare Antwort -> nicht validiert, nie freigegeben
            return ExpertOpinion(
                expert=expert_id,
                name=expert_info["name"],
                approved=False,
                confidence=0.0,
                feedback=f"[NICHT VALIDIERT] Expertenprüfung fehlgeschlagen: {str(e)}",
                suggestions=["Prüfung wiederholen oder manuell prüfen"],
                conditions=[],
                reasoning="Systemfehler während der Prüfung – keine Bewertung erfolgt",
                validated=False,
            )

    def _not_validated_result(
        self,
        statement: str,
        modes: List[str],
        timestamp: str,
        reason: str,
    ) -> ValidationResult:
        """Ergebnis, wenn keine Prüfung möglich war: niemals freigegeben."""
        expert_opinions = {}

        for expert_id in modes:
            if expert_id in self.experts:
                expert_info = self.experts[expert_id]
                expert_opinions[expert_id] = ExpertOpinion(
                    expert=expert_id,
                    name=expert_info["name"],
                    approved=False,
                    confidence=0.0,
                    feedback=f"[NICHT VALIDIERT] {reason}",
                    suggestions=["Prüfung mit konfiguriertem Modellzugang wiederholen oder manuell prüfen"],
                    conditions=[],
                    reasoning=reason,
                    validated=False,
                )

        return ValidationResult(
            statement=statement,
            timestamp=timestamp,
            expert_opinions=expert_opinions,
            overall_approved=False,
            approval_level=NOT_VALIDATED,
            suggestions=["Prüfung mit konfiguriertem Modellzugang wiederholen oder manuell prüfen"],
            conditions=[],
        )

    async def quick_check(
        self,
        statement: str,
        expert_id: str
    ) -> Tuple[bool, str]:
        """Quick validation against single expert perspective"""
        if expert_id not in self.experts:
            return False, f"Unknown expert: {expert_id}"

        expert_info = self.experts[expert_id]
        opinion = await self._get_expert_opinion(expert_id, expert_info, statement)
        return (opinion.validated and opinion.approved is True), opinion.feedback


# Global validator instance
expert_validator = ExpertValidator()
