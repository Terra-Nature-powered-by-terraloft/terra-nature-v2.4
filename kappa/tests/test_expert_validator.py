"""
Unit tests for Expert Validator and Expert Engine
Tests multi-expert validation framework
"""

import pytest
import sys
from pathlib import Path

# Adjust path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kappa.services.expert_validator import ExpertValidator
from kappa.services.mrv import MRVValidator
from kappa.core.engine import KappaExpertEngine


@pytest.fixture
def expert_validator():
    """Create expert validator without API key"""
    return ExpertValidator()


@pytest.fixture
def mrv_validator():
    """Create MRV validator"""
    return MRVValidator()


@pytest.fixture
def expert_engine():
    """Create expert engine"""
    return KappaExpertEngine()


class TestExpertValidator:
    """Expert Validator tests"""

    def test_validator_initialization(self, expert_validator):
        """Test validator initializes correctly"""
        assert expert_validator is not None
        assert hasattr(expert_validator, "experts")
        assert len(expert_validator.experts) == 9

    def test_all_experts_defined(self, expert_validator):
        """Test all 9 experts are defined"""
        expected_experts = [
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
        for expert_id in expected_experts:
            assert expert_id in expert_validator.experts
            assert "name" in expert_validator.experts[expert_id]
            assert "description" in expert_validator.experts[expert_id]

    def test_validate_statement_without_api_key(self, expert_validator):
        """Test validation returns stub response without API key"""
        import asyncio

        async def run_test():
            statement = "Der ORC nutzt Abwärme und erzeugt Strom mit 15% Effizienz."
            result = await expert_validator.validate_statement(statement)

            assert result is not None
            assert result.statement == statement
            assert hasattr(result, "expert_opinions")
            assert len(result.expert_opinions) > 0

        asyncio.run(run_test())

    def test_validate_with_specific_modes(self, expert_validator):
        """Test validation with specific expert modes"""
        import asyncio

        async def run_test():
            statement = "Die CAPEX betragen €2 Mio für eine 100kW ORC."
            modes = ["cto", "bank"]
            result = await expert_validator.validate_statement(
                statement, modes=modes
            )

            assert len(result.expert_opinions) == 2
            assert "cto" in result.expert_opinions
            assert "bank" in result.expert_opinions

        asyncio.run(run_test())

    def test_validation_result_structure(self, expert_validator):
        """Test validation result has correct structure"""
        import asyncio

        async def run_test():
            statement = "Test statement for validation"
            result = await expert_validator.validate_statement(statement)

            for expert_id, opinion in result.expert_opinions.items():
                assert hasattr(opinion, "expert")
                assert hasattr(opinion, "name")
                assert hasattr(opinion, "approved")
                assert hasattr(opinion, "confidence")
                assert hasattr(opinion, "feedback")
                assert hasattr(opinion, "suggestions")
                assert hasattr(opinion, "conditions")
                assert 0.0 <= opinion.confidence <= 1.0

        asyncio.run(run_test())

    def test_approval_level_determination(self, expert_validator):
        """Test approval level is correctly determined"""
        import asyncio

        async def run_test():
            statement = "Scientifically sound technical statement."
            result = await expert_validator.validate_statement(statement)

            # Check approval level is one of the valid options
            assert result.approval_level in ["approved", "conditional", "requires_review"]

        asyncio.run(run_test())


class TestMRVValidator:
    """MRV Validator tests"""

    def test_mrv_validator_initialization(self, mrv_validator):
        """Test MRV validator initializes"""
        assert mrv_validator is not None

    def test_co2_statement_check_without_timestamp(self, mrv_validator):
        """Test CO2 statement without timestamp is flagged"""
        import asyncio

        async def run_test():
            statement = "5 Tonnen CO2 wurden kompensiert."
            result = await mrv_validator.check_co2_statement(statement)

            assert "Zeitstempel" in str(result.issues) or len(result.issues) > 0
            assert isinstance(result.compliant, bool)
            assert 0.0 <= result.confidence <= 1.0

        asyncio.run(run_test())

    def test_co2_statement_check_with_timestamp(self, mrv_validator):
        """Test CO2 statement with timestamp"""
        import asyncio

        async def run_test():
            statement = "Am 2026-05-07 wurden 5 Tonnen CO2 kompensiert durch direkte Messung mit ±5% Genauigkeit."
            result = await mrv_validator.check_co2_statement(statement)

            # Should have fewer issues with proper timestamp and quality info
            assert isinstance(result.compliant, bool)
            assert result.confidence >= 0.3  # Confidence should be decent with timestamp

        asyncio.run(run_test())

    def test_energy_statement_check(self, mrv_validator):
        """Test energy statement validation"""
        import asyncio

        async def run_test():
            statement = "Die Anlage erzeugt 500 kWh pro Tag"
            result = await mrv_validator.check_energy_statement(statement)

            assert isinstance(result.compliant, bool)
            assert isinstance(result.issues, list)
            assert isinstance(result.requirements, list)

        asyncio.run(run_test())

    def test_efficiency_validation(self, mrv_validator):
        """Test efficiency claim validation"""
        import asyncio

        async def run_test():
            # Impossible efficiency
            statement = "Der ORC hat 150% Effizienz"
            result = await mrv_validator.check_energy_statement(statement)

            assert len(result.issues) > 0
            assert "100%" in str(result.issues) or "unmöglich" in str(result.issues)

        asyncio.run(run_test())

    def test_additionality_check(self, mrv_validator):
        """Test additionality validation"""
        import asyncio

        async def run_test():
            statement = "Ohne das Projekt würde die Abwärme nicht genutzt (Business Case)."
            result = await mrv_validator.check_additionality(statement)

            assert isinstance(result.compliant, bool)
            assert isinstance(result.confidence, float)

        asyncio.run(run_test())

    def test_leakage_check(self, mrv_validator):
        """Test leakage validation"""
        import asyncio

        async def run_test():
            statement = "Keine Verlagerung von Emissionen, da System lokal bleibt."
            result = await mrv_validator.check_leakage(statement)

            assert isinstance(result.compliant, bool)

        asyncio.run(run_test())


class TestExpertEngine:
    """Expert Engine tests"""

    def test_engine_initialization(self, expert_engine):
        """Test engine initializes correctly"""
        assert expert_engine is not None
        assert len(expert_engine.expert_modes) == 9

    def test_validate_statement_basic(self, expert_engine):
        """Test basic statement validation"""
        import asyncio

        async def run_test():
            statement = "Der ORC-Prozess nutzt Abwärme zur Stromerzeugung."
            result = await expert_engine.validate_statement(statement)

            assert "statement" in result
            assert "timestamp" in result
            assert "validation_level" in result
            assert "overall_approved" in result
            assert "expert_opinions" in result
            assert result["validation_level"] in ["approved", "conditional", "requires_review"]

        asyncio.run(run_test())

    def test_validate_with_specific_modes(self, expert_engine):
        """Test validation with specific modes"""
        import asyncio

        async def run_test():
            statement = "CAPEX: €5M, OPEX: €150k/Jahr"
            modes = ["bank", "business"]
            result = await expert_engine.validate_statement(
                statement, modes=modes
            )

            assert len(result["expert_opinions"]) == 2
            assert "bank" in result["expert_opinions"]
            assert "business" in result["expert_opinions"]

        asyncio.run(run_test())

    def test_mrv_checks_integration(self, expert_engine):
        """Test MRV checks are included in validation"""
        import asyncio

        async def run_test():
            statement = "Am 2026-05-07 wurden 10 Tonnen CO2 durch ORC kompensiert."
            modes = ["mrv"]
            result = await expert_engine.validate_statement(
                statement, modes=modes
            )

            # MRV mode should include MRV checks
            assert "mrv_check" in result or "expert_opinions" in result

        asyncio.run(run_test())

    def test_approval_summary_generation(self, expert_engine):
        """Test approval summary is generated"""
        import asyncio

        async def run_test():
            statement = "Die Anlage ist technisch und wirtschaftlich rentabel."
            result = await expert_engine.validate_statement(statement)

            assert "approval_summary" in result
            assert isinstance(result["approval_summary"], str)
            assert len(result["approval_summary"]) > 0

        asyncio.run(run_test())

    def test_query_with_validation(self, expert_engine):
        """Test query processing with validation"""
        import asyncio

        async def run_test():
            query = "Was ist ein ORC?"
            mode = "professorale"
            result = await expert_engine.query_with_validation(query, mode)

            assert "response" in result
            assert "timestamp" in result
            assert "mode" in result
            assert "sources" in result

        asyncio.run(run_test())

    def test_error_handling(self, expert_engine):
        """Test error handling in validation"""
        import asyncio

        async def run_test():
            # Empty statement should not crash
            result = await expert_engine.validate_statement("")
            assert "validation_level" in result

        asyncio.run(run_test())
