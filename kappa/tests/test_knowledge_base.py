"""
Unit tests for Knowledge Base module
Tests concept management, relationships, and facts
"""

import pytest
import tempfile
import json
from pathlib import Path

# Adjust path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.knowledge_base import KnowledgeBase
from utils.database import DatabaseManager


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_kb.db"
        yield str(db_path)


@pytest.fixture
def knowledge_base(temp_db, monkeypatch):
    """Create knowledge base with temp database"""
    monkeypatch.setenv("KAPPA_KB_PATH", temp_db)
    kb = KnowledgeBase()
    yield kb


class TestKnowledgeBase:
    """Knowledge Base tests"""

    def test_core_concepts_loaded(self, knowledge_base):
        """Test that core concepts are loaded on init"""
        stats = knowledge_base.get_stats()
        assert stats["total_concepts"] >= 8, "Core concepts should be pre-loaded"

    def test_add_concept(self, knowledge_base):
        """Test adding a new concept"""
        concept_id = knowledge_base.add_concept(
            name="Test Concept",
            category="technical",
            definition="A test concept for unit testing",
            context="Test context"
        )
        assert concept_id > 0, "Concept should be added with positive ID"

        # Verify we can retrieve it
        concept = knowledge_base.get_concept("Test Concept")
        assert concept is not None
        assert concept["definition"] == "A test concept for unit testing"

    def test_duplicate_concept_returns_existing(self, knowledge_base):
        """Test that adding duplicate concept returns existing ID"""
        id1 = knowledge_base.add_concept("Unique Concept", "technical", "Definition 1")
        id2 = knowledge_base.add_concept("Unique Concept", "technical", "Definition 2")
        assert id1 == id2, "Duplicate concept should return same ID"

    def test_search_concepts(self, knowledge_base):
        """Test searching concepts"""
        knowledge_base.add_concept("Solar Energy", "technical", "Energy from sun")
        results = knowledge_base.search_concepts("Energy")
        assert len(results) > 0, "Should find concepts with 'Energy' in name or definition"

    def test_concepts_by_category(self, knowledge_base):
        """Test filtering concepts by category"""
        knowledge_base.add_concept("Test Tech", "technical", "A technical concept")
        tech_concepts = knowledge_base.get_concepts_by_category("technical")
        assert len(tech_concepts) > 0, "Should return technical concepts"

    def test_add_relationship(self, knowledge_base):
        """Test adding relationships between concepts"""
        # Ensure concepts exist
        knowledge_base.add_concept("Concept A", "technical", "First concept")
        knowledge_base.add_concept("Concept B", "technical", "Second concept")

        rel_id = knowledge_base.add_relationship(
            "Concept A",
            "Concept B",
            "requires",
            strength=0.9
        )
        assert rel_id > 0, "Relationship should be created"

    def test_get_related_concepts(self, knowledge_base):
        """Test retrieving related concepts"""
        knowledge_base.add_concept("Parent", "technical", "Parent concept")
        knowledge_base.add_concept("Child", "technical", "Child concept")
        knowledge_base.add_relationship("Parent", "Child", "part_of", strength=1.0)

        related = knowledge_base.get_related_concepts("Parent")
        assert len(related) > 0, "Should return related concepts"
        assert any(r["name"] == "Child" for r in related), "Should include Child concept"

    def test_add_fact(self, knowledge_base):
        """Test adding facts to concepts"""
        knowledge_base.add_concept("ORC", "technical", "Organic Rankine Cycle")
        fact_id = knowledge_base.add_fact(
            "ORC",
            "Efficiency at 100°C",
            data_type="percentage",
            value="15",
            unit="%",
            verified=True
        )
        assert fact_id > 0, "Fact should be added"

    def test_get_facts(self, knowledge_base):
        """Test retrieving facts"""
        knowledge_base.add_concept("TEG", "technical", "Thermoelectric Generator")
        knowledge_base.add_fact("TEG", "Max efficiency", data_type="percentage", value="5")
        knowledge_base.add_fact("TEG", "Operating temp", data_type="range", value="50-200")

        facts = knowledge_base.get_facts("TEG")
        assert len(facts) >= 2, "Should return all facts"

    def test_get_verified_facts_only(self, knowledge_base):
        """Test filtering for verified facts only"""
        knowledge_base.add_concept("Test", "technical", "Test")
        knowledge_base.add_fact("Test", "Verified fact", verified=True)
        knowledge_base.add_fact("Test", "Unverified fact", verified=False)

        verified = knowledge_base.get_facts("Test", verified_only=True)
        assert len(verified) == 1, "Should return only verified facts"

    def test_store_terra_data(self, knowledge_base):
        """Test storing Terra Nature specific data"""
        data_id = knowledge_base.store_terra_data(
            "metric",
            "daily_co2_compensation",
            "150.5",
            metadata={"unit": "kg", "source": "MHKW Rosenheim"}
        )
        assert data_id > 0, "Terra data should be stored"

    def test_get_terra_data(self, knowledge_base):
        """Test retrieving Terra data"""
        knowledge_base.store_terra_data("project_status", "phase", "MVP Phase 1")
        data = knowledge_base.get_terra_data("project_status", "phase")
        assert len(data) > 0, "Should retrieve stored data"
        assert data[0]["value"] == "MVP Phase 1"

    def test_stats(self, knowledge_base):
        """Test knowledge base statistics"""
        stats = knowledge_base.get_stats()
        assert "total_concepts" in stats
        assert "total_relationships" in stats
        assert "total_facts" in stats
        assert "total_terra_data" in stats
        assert "concepts_by_category" in stats
