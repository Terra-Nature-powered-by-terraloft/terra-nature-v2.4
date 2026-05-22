-- Kappa Knowledge Base Schema
-- SQLite Database for Terra Nature Expert Knowledge

-- Core Concepts Table
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,  -- "technical", "regulatory", "financial", "industrial", "organizational"
    definition TEXT NOT NULL,
    context TEXT,  -- Additional context or notes
    source TEXT,  -- Where this knowledge comes from (e.g., "terra_nature_spec", "user_input")
    confidence REAL DEFAULT 1.0,  -- 0.0 to 1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_category CHECK (category IN ('technical', 'regulatory', 'financial', 'industrial', 'organizational'))
);

-- Relationships between concepts
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    related_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,  -- "requires", "conflicts_with", "implies", "example_of", "part_of"
    strength REAL DEFAULT 1.0,  -- 0.0 to 1.0 (how strong the relationship is)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE,
    FOREIGN KEY (related_id) REFERENCES concepts(id) ON DELETE CASCADE,
    CONSTRAINT valid_relation_type CHECK (relation_type IN ('requires', 'conflicts_with', 'implies', 'example_of', 'part_of'))
);

-- Facts and Data Points
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER NOT NULL,
    fact_text TEXT NOT NULL,
    data_type TEXT,  -- "number", "percentage", "range", "text", "timestamp"
    value TEXT,  -- Actual value (could be JSON for complex data)
    unit TEXT,  -- Unit if applicable (e.g., "kWh", "%", "EUR")
    source TEXT,
    verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

-- Terra Nature Specific Data
CREATE TABLE IF NOT EXISTS terra_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_type TEXT NOT NULL,  -- "metric", "project_status", "milestones", "contacts", "funding"
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    metadata TEXT,  -- JSON string for additional info
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    UNIQUE(data_type, key)
);

-- Expert Rules (for reference, actual rules in YAML)
CREATE TABLE IF NOT EXISTS expert_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    expert_type TEXT NOT NULL,  -- "cto", "mrv", "bank", "funding", "industrial", "ip", "communication", "professorale", "business"
    rule_description TEXT NOT NULL,
    yaml_source TEXT,  -- Reference to YAML file
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rule_name, expert_type)
);

-- Query Cache (for performance)
CREATE TABLE IF NOT EXISTS query_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_hash TEXT UNIQUE NOT NULL,
    query_text TEXT NOT NULL,
    response TEXT NOT NULL,
    response_mode TEXT,  -- "default", "cto", "mrv", etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 1
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_concepts_category ON concepts(category);
CREATE INDEX IF NOT EXISTS idx_concepts_name ON concepts(name);
CREATE INDEX IF NOT EXISTS idx_relationships_concept ON relationships(concept_id);
CREATE INDEX IF NOT EXISTS idx_relationships_related ON relationships(related_id);
CREATE INDEX IF NOT EXISTS idx_facts_concept ON facts(concept_id);
CREATE INDEX IF NOT EXISTS idx_terra_data_type_key ON terra_data(data_type, key);
CREATE INDEX IF NOT EXISTS idx_query_cache_hash ON query_cache(query_hash);
