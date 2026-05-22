"""
Kappa Knowledge Base Engine
SQLite-backed knowledge management for Terra Nature concepts
"""

from typing import List, Dict, Optional, Any
from datetime import datetime

from ..utils.database import db
from ..utils.logging import logger

class KnowledgeBase:
    """Manage Terra Nature knowledge and concepts"""

    # Pre-loaded Terra Nature Core Concepts
    CORE_CONCEPTS = {
        "ORC": {
            "category": "technical",
            "definition": "Organic Rankine Cycle - Wärmekraftmaschine für niedrige Temperaturdifferenzen",
            "context": "Abwärmenutzung bei 50-150°C, typisch 10-20% Wirkungsgrad",
            "source": "terra_nature_spec",
        },
        "TEG": {
            "category": "technical",
            "definition": "Thermoelectric Generator - Halbleiter-basierte Stromerzeugung aus Wärme",
            "context": "TRL 4-5, unter 5% Wirkungsgrad, direkt integrierbar",
            "source": "terra_nature_spec",
        },
        "Abwärmenutzung": {
            "category": "technical",
            "definition": "Erfassung und Wandlung von Prozesswärmeverlusten",
            "context": "MHKW Rosenheim, Industrieprozesse, Datencentern",
            "source": "terra_nature_spec",
        },
        "MRV": {
            "category": "regulatory",
            "definition": "Monitoring, Reporting, Verification - Nachweisführung von CO₂-Einsparungen",
            "context": "EnEfG, EU-ETS, CSRD Konformität erforderlich",
            "source": "terra_nature_spec",
        },
        "Bankfähigkeit": {
            "category": "financial",
            "definition": "Fähigkeit eines Geschäftsmodells, Bankfinanzierung zu erhalten",
            "context": "§18 KWG, CAPEX/OPEX rational, Sicherheiten, Rendite >10%",
            "source": "terra_nature_spec",
        },
        "TerraNode": {
            "category": "technical",
            "definition": "Modulare Messinheit für dezentrales Energie-Monitoring",
            "context": "Sensorik, Datenerfassung, SCADA-Integration",
            "source": "terra_nature_spec",
        },
        "Stadtwerke": {
            "category": "industrial",
            "definition": "Kommunale Energieversorger, primäre Zielkunden",
            "context": "Betreiberakzeptanz, technische Anforderungen, Wartbarkeit",
            "source": "terra_nature_spec",
        },
        "MHKW Rosenheim": {
            "category": "industrial",
            "definition": "Müllheizkraftwerk Rosenheim - Pilotanwendung für Terra Nature",
            "context": "Abwärmetemperatur 90-120°C, ca. 20 MW Wärmeleistung",
            "source": "terra_nature_spec",
        },
    }

    def __init__(self):
        """Initialize knowledge base"""
        logger.info("knowledge_base_init")
        self._load_core_concepts()

    def _load_core_concepts(self):
        """Load core Terra Nature concepts into database"""
        for name, data in self.CORE_CONCEPTS.items():
            existing = db.execute_one(
                "SELECT id FROM concepts WHERE name = ?",
                (name,)
            )
            if not existing:
                db.insert("concepts", {
                    "name": name,
                    "category": data["category"],
                    "definition": data["definition"],
                    "context": data.get("context"),
                    "source": data.get("source", "system"),
                    "confidence": 1.0,
                })
                logger.info("concept_loaded", name=name, category=data["category"])

    def add_concept(self, name: str, category: str, definition: str,
                   context: Optional[str] = None, source: str = "user") -> int:
        """Add a new concept to knowledge base"""
        existing = db.execute_one(
            "SELECT id FROM concepts WHERE name = ?",
            (name,)
        )
        if existing:
            logger.warning("concept_already_exists", name=name)
            return existing["id"]

        concept_id = db.insert("concepts", {
            "name": name,
            "category": category,
            "definition": definition,
            "context": context,
            "source": source,
            "confidence": 0.8,  # User-added concepts start with lower confidence
        })

        logger.info("concept_added", name=name, id=concept_id)
        return concept_id

    def get_concept(self, name: str) -> Optional[Dict]:
        """Get concept by name"""
        return db.execute_one(
            "SELECT * FROM concepts WHERE name = ?",
            (name,)
        )

    def search_concepts(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search concepts by name or definition"""
        sql = "SELECT * FROM concepts WHERE (name LIKE ? OR definition LIKE ?)"
        params = [f"%{query}%", f"%{query}%"]

        if category:
            sql += " AND category = ?"
            params.append(category)

        return db.execute(sql, tuple(params))

    def get_concepts_by_category(self, category: str) -> List[Dict]:
        """Get all concepts in a category"""
        return db.execute(
            "SELECT * FROM concepts WHERE category = ? ORDER BY confidence DESC",
            (category,)
        )

    def add_relationship(self, concept_name: str, related_name: str,
                        relation_type: str, strength: float = 1.0) -> Optional[int]:
        """Add relationship between two concepts"""
        concept = self.get_concept(concept_name)
        related = self.get_concept(related_name)

        if not concept or not related:
            logger.warning(
                "concept_not_found_for_relationship",
                concept=concept_name,
                related=related_name
            )
            return None

        rel_id = db.insert("relationships", {
            "concept_id": concept["id"],
            "related_id": related["id"],
            "relation_type": relation_type,
            "strength": strength,
        })

        logger.info(
            "relationship_added",
            concept=concept_name,
            related=related_name,
            relation_type=relation_type
        )
        return rel_id

    def get_related_concepts(self, concept_name: str,
                            relation_type: Optional[str] = None) -> List[Dict]:
        """Get concepts related to given concept"""
        concept = self.get_concept(concept_name)
        if not concept:
            return []

        sql = """
            SELECT c.*, r.relation_type, r.strength
            FROM concepts c
            JOIN relationships r ON c.id = r.related_id
            WHERE r.concept_id = ?
        """
        params = [concept["id"]]

        if relation_type:
            sql += " AND r.relation_type = ?"
            params.append(relation_type)

        sql += " ORDER BY r.strength DESC"
        return db.execute(sql, tuple(params))

    def add_fact(self, concept_name: str, fact_text: str,
                data_type: Optional[str] = None, value: Optional[str] = None,
                unit: Optional[str] = None, source: str = "user",
                verified: bool = False) -> Optional[int]:
        """Add a fact or data point about a concept"""
        concept = self.get_concept(concept_name)
        if not concept:
            logger.warning("concept_not_found_for_fact", concept=concept_name)
            return None

        fact_id = db.insert("facts", {
            "concept_id": concept["id"],
            "fact_text": fact_text,
            "data_type": data_type,
            "value": value,
            "unit": unit,
            "source": source,
            "verified": 1 if verified else 0,
        })

        logger.info("fact_added", concept=concept_name, fact_id=fact_id)
        return fact_id

    def get_facts(self, concept_name: str, verified_only: bool = False) -> List[Dict]:
        """Get all facts about a concept"""
        concept = self.get_concept(concept_name)
        if not concept:
            return []

        sql = "SELECT * FROM facts WHERE concept_id = ?"
        params = [concept["id"]]

        if verified_only:
            sql += " AND verified = 1"

        sql += " ORDER BY updated_at DESC"
        return db.execute(sql, tuple(params))

    def store_terra_data(self, data_type: str, key: str, value: str,
                        metadata: Optional[Dict] = None, source: str = "system") -> int:
        """Store Terra Nature specific data"""
        import json

        metadata_json = json.dumps(metadata) if metadata else None

        # Update if exists, insert if not
        existing = db.execute_one(
            "SELECT id FROM terra_data WHERE data_type = ? AND key = ?",
            (data_type, key)
        )

        if existing:
            db.update(
                "terra_data",
                {"value": value, "metadata": metadata_json, "source": source},
                {"id": existing["id"]}
            )
            logger.info("terra_data_updated", data_type=data_type, key=key)
            return existing["id"]
        else:
            data_id = db.insert("terra_data", {
                "data_type": data_type,
                "key": key,
                "value": value,
                "metadata": metadata_json,
                "source": source,
            })
            logger.info("terra_data_stored", data_type=data_type, key=key, id=data_id)
            return data_id

    def get_terra_data(self, data_type: str, key: Optional[str] = None) -> List[Dict]:
        """Retrieve Terra Nature data"""
        if key:
            result = db.execute_one(
                "SELECT * FROM terra_data WHERE data_type = ? AND key = ?",
                (data_type, key)
            )
            return [result] if result else []
        else:
            return db.execute(
                "SELECT * FROM terra_data WHERE data_type = ? ORDER BY timestamp DESC",
                (data_type,)
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        stats = {
            "total_concepts": db.execute_one(
                "SELECT COUNT(*) as count FROM concepts"
            )["count"],
            "concepts_by_category": {},
            "total_relationships": db.execute_one(
                "SELECT COUNT(*) as count FROM relationships"
            )["count"],
            "total_facts": db.execute_one(
                "SELECT COUNT(*) as count FROM facts"
            )["count"],
            "total_terra_data": db.execute_one(
                "SELECT COUNT(*) as count FROM terra_data"
            )["count"],
        }

        # Count concepts by category
        by_category = db.execute(
            "SELECT category, COUNT(*) as count FROM concepts GROUP BY category"
        )
        stats["concepts_by_category"] = {row["category"]: row["count"] for row in by_category}

        return stats

# Global knowledge base instance
kb = KnowledgeBase()
