"""
Kappa Expert Engine
Central orchestration of expert validation, knowledge base, and response generation
"""

from typing import Optional, List, Dict, Tuple
from datetime import datetime

from ..services.expert_validator import expert_validator, ExpertOpinion, ValidationResult
from ..services.mrv import mrv_validator, MRVCheckResult
from ..core.knowledge_base import kb
from ..core.memory import memory
from ..utils.logging import logger


class KappaExpertEngine:
    """Central expert validation and response engine"""

    def __init__(self):
        """Initialize Expert Engine"""
        logger.info("expert_engine_init")
        self.expert_modes = [
            "professorale",
            "cto",
            "mrv",
            "bank",
            "funding",
            "industrial",
            "ip",
            "communication",
            "business",
        ]

    async def validate_statement(
        self,
        statement: str,
        modes: Optional[List[str]] = None,
        user: str = "system"
    ) -> Dict:
        """
        Validate a statement against multiple expert perspectives

        Args:
            statement: The statement to validate
            modes: Specific expert modes to validate against (None = all 9)
            user: User identifier for audit logging

        Returns:
            Comprehensive validation result with expert opinions
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Determine which modes to validate
        validation_modes = modes or self.expert_modes
        # Filter to only known modes
        validation_modes = [m for m in validation_modes if m in self.expert_modes]

        logger.info(
            "validation_requested",
            statement_length=len(statement),
            modes=validation_modes,
            user=user,
        )

        # Get expert opinions
        result = await expert_validator.validate_statement(
            statement, validation_modes, timestamp
        )

        # Perform MRV checks if in MRV mode
        mrv_results = None
        if "mrv" in validation_modes:
            mrv_results = await self._perform_mrv_checks(statement)

        # Log validation result
        self._log_validation(statement, result, user)

        # Store in memory
        memory.record_audit_event("validation_completed", {
            "statement": statement[:100],
            "approval_level": result.approval_level,
            "modes": validation_modes,
            "user": user,
        })

        return {
            "statement": statement,
            "timestamp": timestamp,
            "validation_level": result.approval_level,
            "overall_approved": result.overall_approved,
            "expert_opinions": self._serialize_opinions(result.expert_opinions),
            "mrv_check": mrv_results,
            "suggestions": result.suggestions,
            "conditions": result.conditions,
            "approval_summary": self._create_approval_summary(result),
        }

    async def query_with_validation(
        self,
        query_text: str,
        mode: str = "default",
        user: str = "system"
    ) -> Dict:
        """
        Process query and apply expert validation if needed

        Args:
            query_text: User's query
            mode: Expert mode for validation
            user: User identifier

        Returns:
            Query response with validation results if applicable
        """
        logger.info("query_with_validation", mode=mode, user=user)

        timestamp = datetime.utcnow().isoformat() + "Z"

        # Search knowledge base
        search_results = kb.search_concepts(query_text)
        response_text = None
        sources = []
        confidence = 0.5

        if search_results:
            sources.append("knowledge_base")
            confidence = max(confidence, 0.7)
            concept_info = []
            for concept in search_results[:3]:
                concept_info.append(
                    f"{concept['name']} ({concept['category']}): {concept['definition']}"
                )
            response_text = "Wissensbank-Treffer:\n" + "\n".join(concept_info)

        # Check project memory
        memory_summary = memory.get_memory_summary()
        if memory_summary and memory_summary.get("project_status"):
            sources.append("project_memory")
            if response_text:
                response_text += (
                    "\n\nProjekt-Status: "
                    + str(memory_summary["project_status"].get("current_phase", "Unbekannt"))
                )

        # Fallback
        if not response_text:
            response_text = f"Keine Treffer für: {query_text}"
            sources.append("fallback")
            confidence = 0.3

        # Apply validation if expert mode requested
        validation_result = None
        if mode != "default" and mode in self.expert_modes:
            validation_result = await self.validate_statement(
                response_text, [mode], user
            )

        return {
            "response": response_text,
            "mode": mode,
            "confidence": confidence,
            "sources": sources,
            "timestamp": timestamp,
            "validation": validation_result,
        }

    async def _perform_mrv_checks(self, statement: str) -> Dict:
        """Perform MRV compliance checks"""
        logger.info("mrv_checks_started", statement_length=len(statement))

        try:
            co2_result = await mrv_validator.check_co2_statement(statement)
            energy_result = await mrv_validator.check_energy_statement(statement)
            additionality_result = await mrv_validator.check_additionality(statement)
            leakage_result = await mrv_validator.check_leakage(statement)

            all_compliant = all([
                co2_result.compliant,
                energy_result.compliant,
                additionality_result.compliant,
                leakage_result.compliant,
            ])

            avg_confidence = (
                co2_result.confidence
                + energy_result.confidence
                + additionality_result.confidence
                + leakage_result.confidence
            ) / 4

            return {
                "compliant": all_compliant,
                "confidence": avg_confidence,
                "checks": {
                    "co2": {
                        "compliant": co2_result.compliant,
                        "issues": co2_result.issues,
                        "requirements": co2_result.requirements,
                    },
                    "energy": {
                        "compliant": energy_result.compliant,
                        "issues": energy_result.issues,
                        "requirements": energy_result.requirements,
                    },
                    "additionality": {
                        "compliant": additionality_result.compliant,
                        "issues": additionality_result.issues,
                        "requirements": additionality_result.requirements,
                    },
                    "leakage": {
                        "compliant": leakage_result.compliant,
                        "issues": leakage_result.issues,
                        "requirements": leakage_result.requirements,
                    },
                },
            }

        except Exception as e:
            logger.error("mrv_checks_failed", error=str(e))
            return {
                "compliant": False,
                "confidence": 0.0,
                "error": str(e),
            }

    def _serialize_opinions(self, opinions: Dict[str, ExpertOpinion]) -> Dict:
        """Convert ExpertOpinion objects to serializable dicts"""
        return {
            expert_id: {
                "expert": opinion.expert,
                "name": opinion.name,
                "approved": opinion.approved,
                "confidence": opinion.confidence,
                "feedback": opinion.feedback,
                "suggestions": opinion.suggestions,
                "conditions": opinion.conditions,
                "reasoning": opinion.reasoning,
            }
            for expert_id, opinion in opinions.items()
        }

    def _create_approval_summary(self, result: ValidationResult) -> str:
        """Create human-readable approval summary"""
        approved_experts = sum(
            1 for op in result.expert_opinions.values() if op.approved
        )
        total_experts = len(result.expert_opinions)

        summary = f"{approved_experts}/{total_experts} Experten genehmigen | "

        if result.approval_level == "approved":
            summary += "✓ GENEHMIGT"
        elif result.approval_level == "conditional":
            summary += "⚠ BEDINGT GENEHMIGT"
        else:
            summary += "✗ ÜBERPRÜFUNG ERFORDERLICH"

        return summary

    def _log_validation(
        self,
        statement: str,
        result: ValidationResult,
        user: str
    ) -> None:
        """Log validation result for audit trail"""
        logger.info(
            "validation_logged",
            approval_level=result.approval_level,
            experts_count=len(result.expert_opinions),
            approved_count=sum(
                1 for op in result.expert_opinions.values() if op.approved
            ),
            user=user,
        )


# Global Expert Engine instance
expert_engine = KappaExpertEngine()
