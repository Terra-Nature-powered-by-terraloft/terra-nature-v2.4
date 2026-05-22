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


@dataclass
class ValidationResult:
    """Complete validation across all experts"""
    statement: str
    timestamp: str
    expert_opinions: Dict[str, ExpertOpinion]
    overall_approved: bool
    approval_level: str  # "approved", "conditional", "requires_review"
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
            return self._stub_validation(statement, modes or list(self.experts.keys()), timestamp)

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

        # Calculate aggregate approval
        approved_count = sum(1 for op in expert_opinions.values() if op.approved)
        approval_rate = approved_count / len(expert_opinions) if expert_opinions else 0

        if approval_rate >= 0.8:
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

            client = anthropic.Anthropic(api_key=self.api_key)

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

            # Parse JSON response
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                opinion_data = json.loads(json_match.group())
            else:
                # Fallback parsing
                opinion_data = {
                    "approved": "approved" in response_text.lower(),
                    "confidence": 0.5,
                    "feedback": response_text,
                    "suggestions": [],
                    "conditions": [],
                    "reasoning": response_text,
                }

            opinion = ExpertOpinion(
                expert=expert_id,
                name=expert_info["name"],
                approved=opinion_data.get("approved", False),
                confidence=float(opinion_data.get("confidence", 0.5)),
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
            # Return stub opinion on error
            return ExpertOpinion(
                expert=expert_id,
                name=expert_info["name"],
                approved=False,
                confidence=0.0,
                feedback=f"[ERROR] Expert validation failed: {str(e)}",
                suggestions=["Retry validation"],
                conditions=[],
                reasoning="System error during validation",
            )

    def _stub_validation(
        self,
        statement: str,
        modes: List[str],
        timestamp: str
    ) -> ValidationResult:
        """Return stub validation when API key not available"""
        expert_opinions = {}

        for expert_id in modes:
            if expert_id in self.experts:
                expert_info = self.experts[expert_id]
                expert_opinions[expert_id] = ExpertOpinion(
                    expert=expert_id,
                    name=expert_info["name"],
                    approved=True,
                    confidence=0.0,
                    feedback="[STUB] Expert validation framework ready. Actual rules load in Phase 5.",
                    suggestions=["Load expert rules from YAML"],
                    conditions=[],
                    reasoning="Stub response - API key not configured",
                )

        return ValidationResult(
            statement=statement,
            timestamp=timestamp,
            expert_opinions=expert_opinions,
            overall_approved=True,
            approval_level="approved",
            suggestions=["Load expert rules from YAML"],
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
        return opinion.approved, opinion.feedback


# Global validator instance
expert_validator = ExpertValidator()
