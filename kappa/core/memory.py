"""
Kappa Project Memory Manager
JSON-LD based project state and decision tracking for Terra Nature
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from ..utils.logging import logger


class ProjectMemory:
    """Manage project memory and decision protocols in JSON-LD format"""

    def __init__(self, memory_path: str = "kappa/data/memory.jsonld"):
        """Initialize project memory from file"""
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_or_create()
        logger.info("project_memory_init", path=str(self.memory_path))

    def _load_or_create(self):
        """Load existing memory or create default structure"""
        if self.memory_path.exists():
            try:
                with open(self.memory_path, "r") as f:
                    self.data = json.load(f)
                logger.info("project_memory_loaded", path=str(self.memory_path))
            except Exception as e:
                logger.warning("project_memory_load_failed", error=str(e))
                self._create_default()
        else:
            self._create_default()

    def _create_default(self):
        """Create default project memory structure"""
        self.data = {
            "@context": "https://terra-nature.example/context.jsonld",
            "@type": "ProjectMemory",
            "project_status": {
                "current_phase": "MVP Phase 1",
                "start_date": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat(),
                "health": "operational",
            },
            "open_tasks": [],
            "recent_decisions": [],
            "financial_data": {
                "budget": None,
                "spent": 0.0,
                "runway_weeks": None,
            },
            "technical_modules": {
                "orc_status": None,
                "teg_status": None,
                "monitoring": None,
            },
            "stakeholders": [],
            "milestones": [],
            "risks": [],
            "audit_events": [],
        }
        self._save()
        logger.info("project_memory_created_default", path=str(self.memory_path))

    def _save(self):
        """Persist memory to disk"""
        try:
            with open(self.memory_path, "w") as f:
                json.dump(self.data, f, indent=2)
            logger.info("project_memory_saved")
        except Exception as e:
            logger.error("project_memory_save_failed", error=str(e))
            raise

    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status"""
        return self.data.get("project_status", {})

    def update_project_status(self, status_updates: Dict[str, Any]):
        """Update project status fields"""
        if "project_status" not in self.data:
            self.data["project_status"] = {}

        self.data["project_status"].update(status_updates)
        self.data["project_status"]["last_updated"] = datetime.utcnow().isoformat()
        self._save()
        logger.info("project_status_updated", fields=list(status_updates.keys()))

    def add_task(self, task: str, priority: str = "medium", assigned_to: Optional[str] = None) -> Dict:
        """Add an open task"""
        task_obj = {
            "id": len(self.data.get("open_tasks", [])) + 1,
            "task": task,
            "priority": priority,
            "assigned_to": assigned_to,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open",
        }

        if "open_tasks" not in self.data:
            self.data["open_tasks"] = []

        self.data["open_tasks"].append(task_obj)
        self._save()
        logger.info("task_added", task=task, priority=priority)
        return task_obj

    def complete_task(self, task_id: int):
        """Mark task as complete"""
        if "open_tasks" not in self.data:
            return

        for task in self.data["open_tasks"]:
            if task.get("id") == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.utcnow().isoformat()
                self._save()
                logger.info("task_completed", task_id=task_id)
                return

        logger.warning("task_not_found", task_id=task_id)

    def get_open_tasks(self) -> List[Dict]:
        """Get all open tasks"""
        return [t for t in self.data.get("open_tasks", []) if t.get("status") == "open"]

    def add_decision(self, decision: str, reason: str, decided_by: str = "system", context: Optional[Dict] = None) -> Dict:
        """Record a project decision"""
        decision_obj = {
            "id": len(self.data.get("recent_decisions", [])) + 1,
            "decision": decision,
            "reason": reason,
            "decided_by": decided_by,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {},
        }

        if "recent_decisions" not in self.data:
            self.data["recent_decisions"] = []

        self.data["recent_decisions"].insert(0, decision_obj)  # Most recent first
        # Keep only last 100 decisions
        self.data["recent_decisions"] = self.data["recent_decisions"][:100]
        self._save()
        logger.info("decision_recorded", decision=decision, decided_by=decided_by)
        return decision_obj

    def get_decisions(self, limit: int = 20) -> List[Dict]:
        """Get recent decisions"""
        return self.data.get("recent_decisions", [])[:limit]

    def update_financial_data(self, budget: Optional[float] = None, spent: Optional[float] = None,
                             runway_weeks: Optional[int] = None):
        """Update financial tracking"""
        if "financial_data" not in self.data:
            self.data["financial_data"] = {}

        if budget is not None:
            self.data["financial_data"]["budget"] = budget
        if spent is not None:
            self.data["financial_data"]["spent"] = spent
        if runway_weeks is not None:
            self.data["financial_data"]["runway_weeks"] = runway_weeks

        self.data["financial_data"]["last_updated"] = datetime.utcnow().isoformat()
        self._save()
        logger.info("financial_data_updated")

    def get_financial_data(self) -> Dict[str, Any]:
        """Get financial tracking"""
        return self.data.get("financial_data", {})

    def update_technical_module(self, module: str, status: str, details: Optional[Dict] = None):
        """Update status of a technical module (ORC, TEG, etc.)"""
        if "technical_modules" not in self.data:
            self.data["technical_modules"] = {}

        self.data["technical_modules"][module] = {
            "status": status,
            "details": details or {},
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._save()
        logger.info("technical_module_updated", module=module, status=status)

    def get_technical_modules(self) -> Dict[str, Any]:
        """Get all technical module statuses"""
        return self.data.get("technical_modules", {})

    def add_stakeholder(self, name: str, role: str, contact: Optional[str] = None) -> Dict:
        """Add a stakeholder"""
        stakeholder = {
            "id": len(self.data.get("stakeholders", [])) + 1,
            "name": name,
            "role": role,
            "contact": contact,
            "added_at": datetime.utcnow().isoformat(),
        }

        if "stakeholders" not in self.data:
            self.data["stakeholders"] = []

        self.data["stakeholders"].append(stakeholder)
        self._save()
        logger.info("stakeholder_added", name=name, role=role)
        return stakeholder

    def get_stakeholders(self) -> List[Dict]:
        """Get all stakeholders"""
        return self.data.get("stakeholders", [])

    def add_milestone(self, name: str, target_date: str, description: str = "") -> Dict:
        """Add a project milestone"""
        milestone = {
            "id": len(self.data.get("milestones", [])) + 1,
            "name": name,
            "target_date": target_date,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "completed": False,
        }

        if "milestones" not in self.data:
            self.data["milestones"] = []

        self.data["milestones"].append(milestone)
        self._save()
        logger.info("milestone_added", name=name, target_date=target_date)
        return milestone

    def get_milestones(self, completed_only: bool = False) -> List[Dict]:
        """Get milestones"""
        milestones = self.data.get("milestones", [])
        if completed_only:
            return [m for m in milestones if m.get("completed")]
        return milestones

    def add_risk(self, risk: str, severity: str = "medium", mitigation: str = "") -> Dict:
        """Log a project risk"""
        risk_obj = {
            "id": len(self.data.get("risks", [])) + 1,
            "risk": risk,
            "severity": severity,
            "mitigation": mitigation,
            "identified_at": datetime.utcnow().isoformat(),
            "status": "open",
        }

        if "risks" not in self.data:
            self.data["risks"] = []

        self.data["risks"].append(risk_obj)
        self._save()
        logger.info("risk_identified", risk=risk, severity=severity)
        return risk_obj

    def get_risks(self, status: str = "open") -> List[Dict]:
        """Get risks"""
        return [r for r in self.data.get("risks", []) if r.get("status") == status]

    def record_audit_event(self, event_type: str, details: Dict[str, Any]):
        """Record audit event in memory"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "details": details,
        }

        if "audit_events" not in self.data:
            self.data["audit_events"] = []

        self.data["audit_events"].append(event)
        # Keep only last 500 events
        self.data["audit_events"] = self.data["audit_events"][-500:]
        self._save()
        logger.info("audit_event_recorded", type=event_type)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "open_tasks": len(self.get_open_tasks()),
            "recent_decisions": len(self.data.get("recent_decisions", [])),
            "stakeholders": len(self.data.get("stakeholders", [])),
            "milestones": len(self.data.get("milestones", [])),
            "risks_open": len(self.get_risks("open")),
            "audit_events": len(self.data.get("audit_events", [])),
            "last_updated": self.data.get("project_status", {}).get("last_updated"),
        }

    def get_full_memory(self) -> Dict[str, Any]:
        """Get complete memory structure"""
        return self.data

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of project memory"""
        return {
            "project_status": self.get_project_status(),
            "tasks": self.get_open_tasks(),
            "recent_decisions": self.get_decisions(limit=5),
            "financial_data": self.get_financial_data(),
            "technical_modules": self.get_technical_modules(),
            "stats": self.get_memory_stats(),
        }


# Global project memory instance
memory = ProjectMemory()
