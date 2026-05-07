"""
Unit tests for Project Memory module
Tests JSON-LD memory management, tasks, decisions, financial tracking
"""

import pytest
import tempfile
import json
from pathlib import Path

# Adjust path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.memory import ProjectMemory


@pytest.fixture
def temp_memory_file():
    """Create temporary memory file for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory_path = Path(tmpdir) / "memory.jsonld"
        yield str(memory_path)


@pytest.fixture
def project_memory(temp_memory_file, monkeypatch):
    """Create project memory with temp file"""
    monkeypatch.setenv("KAPPA_MEMORY_PATH", temp_memory_file)
    memory = ProjectMemory(temp_memory_file)
    yield memory


class TestProjectMemory:
    """Project Memory tests"""

    def test_memory_initialization(self, project_memory):
        """Test memory initializes with default structure"""
        data = project_memory.get_full_memory()
        assert "@context" in data
        assert "@type" in data
        assert data["@type"] == "ProjectMemory"

    def test_get_project_status(self, project_memory):
        """Test getting project status"""
        status = project_memory.get_project_status()
        assert "current_phase" in status
        assert "last_updated" in status

    def test_update_project_status(self, project_memory):
        """Test updating project status"""
        project_memory.update_project_status({
            "current_phase": "Phase 2",
            "health": "excellent"
        })
        status = project_memory.get_project_status()
        assert status["current_phase"] == "Phase 2"
        assert status["health"] == "excellent"

    def test_add_task(self, project_memory):
        """Test adding tasks"""
        task = project_memory.add_task(
            "Implement Knowledge Base",
            priority="high",
            assigned_to="developer"
        )
        assert task["id"] > 0
        assert task["status"] == "open"

    def test_get_open_tasks(self, project_memory):
        """Test retrieving open tasks"""
        project_memory.add_task("Task 1", priority="high")
        project_memory.add_task("Task 2", priority="medium")
        tasks = project_memory.get_open_tasks()
        assert len(tasks) >= 2

    def test_complete_task(self, project_memory):
        """Test marking task as complete"""
        task = project_memory.add_task("Test Task")
        project_memory.complete_task(task["id"])

        open_tasks = project_memory.get_open_tasks()
        completed = [t for t in project_memory.data.get("open_tasks", [])
                    if t["id"] == task["id"]]
        assert len(completed) > 0
        assert completed[0]["status"] == "completed"

    def test_add_decision(self, project_memory):
        """Test recording decisions"""
        decision = project_memory.add_decision(
            "Proceed with FastAPI implementation",
            reason="Optimal for async ML services",
            decided_by="CTO"
        )
        assert decision["id"] > 0
        assert decision["decision"] == "Proceed with FastAPI implementation"

    def test_get_decisions(self, project_memory):
        """Test retrieving recent decisions"""
        project_memory.add_decision("Decision 1", "Reason 1")
        project_memory.add_decision("Decision 2", "Reason 2")
        decisions = project_memory.get_decisions(limit=5)
        assert len(decisions) >= 2

    def test_update_financial_data(self, project_memory):
        """Test financial tracking"""
        project_memory.update_financial_data(
            budget=100000.0,
            spent=25000.0,
            runway_weeks=52
        )
        financial = project_memory.get_financial_data()
        assert financial["budget"] == 100000.0
        assert financial["spent"] == 25000.0
        assert financial["runway_weeks"] == 52

    def test_update_technical_module(self, project_memory):
        """Test technical module tracking"""
        project_memory.update_technical_module(
            "orc",
            "prototype",
            details={"trl": 5, "efficiency": 0.15}
        )
        modules = project_memory.get_technical_modules()
        assert "orc" in modules
        assert modules["orc"]["status"] == "prototype"

    def test_add_stakeholder(self, project_memory):
        """Test stakeholder management"""
        stakeholder = project_memory.add_stakeholder(
            "Dr. Prof. Schmidt",
            role="Academic Advisor",
            contact="schmidt@uni.de"
        )
        assert stakeholder["id"] > 0

    def test_get_stakeholders(self, project_memory):
        """Test retrieving stakeholders"""
        project_memory.add_stakeholder("Stakeholder 1", "Investor")
        project_memory.add_stakeholder("Stakeholder 2", "Partner")
        stakeholders = project_memory.get_stakeholders()
        assert len(stakeholders) >= 2

    def test_add_milestone(self, project_memory):
        """Test milestone tracking"""
        milestone = project_memory.add_milestone(
            "MVP Complete",
            target_date="2026-06-01",
            description="Phases 1-5 complete"
        )
        assert milestone["id"] > 0
        assert milestone["completed"] is False

    def test_get_milestones(self, project_memory):
        """Test retrieving milestones"""
        project_memory.add_milestone("M1", "2026-05-15")
        project_memory.add_milestone("M2", "2026-06-01")
        milestones = project_memory.get_milestones()
        assert len(milestones) >= 2

    def test_add_risk(self, project_memory):
        """Test risk identification"""
        risk = project_memory.add_risk(
            "API rate limits exceeded",
            severity="high",
            mitigation="Implement caching layer"
        )
        assert risk["id"] > 0
        assert risk["status"] == "open"

    def test_get_risks(self, project_memory):
        """Test retrieving risks"""
        project_memory.add_risk("Risk 1", severity="high")
        project_memory.add_risk("Risk 2", severity="medium")
        risks = project_memory.get_risks()
        assert len(risks) >= 2

    def test_record_audit_event(self, project_memory):
        """Test audit event recording"""
        project_memory.record_audit_event(
            "memory_modification",
            {"key": "test", "operation": "update"}
        )
        full_data = project_memory.get_full_memory()
        assert len(full_data.get("audit_events", [])) > 0

    def test_memory_stats(self, project_memory):
        """Test memory statistics"""
        project_memory.add_task("Task")
        project_memory.add_decision("Decision", "Reason")
        project_memory.add_stakeholder("Stakeholder", "Role")

        stats = project_memory.get_memory_stats()
        assert stats["open_tasks"] >= 1
        assert stats["recent_decisions"] >= 1
        assert stats["stakeholders"] >= 1

    def test_memory_summary(self, project_memory):
        """Test getting memory summary"""
        project_memory.update_project_status({"current_phase": "Phase 2"})
        project_memory.add_task("Test Task")

        summary = project_memory.get_memory_summary()
        assert "project_status" in summary
        assert "tasks" in summary
        assert "stats" in summary

    def test_memory_persistence(self, temp_memory_file):
        """Test that memory persists to disk"""
        memory1 = ProjectMemory(temp_memory_file)
        memory1.add_task("Persistent Task")

        # Load again
        memory2 = ProjectMemory(temp_memory_file)
        tasks = memory2.get_open_tasks()
        assert any(t["task"] == "Persistent Task" for t in tasks)

    def test_memory_file_exists(self, temp_memory_file):
        """Test that memory file is created"""
        ProjectMemory(temp_memory_file)
        assert Path(temp_memory_file).exists(), "Memory file should be created"

    def test_memory_json_valid(self, temp_memory_file):
        """Test that memory file contains valid JSON"""
        ProjectMemory(temp_memory_file)
        with open(temp_memory_file) as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "@context" in data
