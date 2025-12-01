CREATE TABLE IF NOT EXISTS sponsors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    website TEXT,
    contact_email TEXT,
    status TEXT DEFAULT 'Identified', -- Identified, Researching, Contacted, Negotiating, Won, Lost
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS research_artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor_id INTEGER,
    content TEXT, -- JSON or Markdown
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sponsor_id) REFERENCES sponsors(id)
);

CREATE TABLE IF NOT EXISTS email_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor_id INTEGER,
    thread_id TEXT,
    subject TEXT,
    last_message_content TEXT,
    last_message_date TIMESTAMP,
    FOREIGN KEY(sponsor_id) REFERENCES sponsors(id)
);

CREATE TABLE IF NOT EXISTS meeting_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT, -- Proposed, Confirmed
    FOREIGN KEY(sponsor_id) REFERENCES sponsors(id)
);

CREATE TABLE IF NOT EXISTS long_term_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor_id INTEGER,
    memory_text TEXT,
    trigger_date TIMESTAMP,
    processed BOOLEAN DEFAULT 0,
    FOREIGN KEY(sponsor_id) REFERENCES sponsors(id)
);

CREATE TABLE IF NOT EXISTS event_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor_id INTEGER,
    agent_name TEXT,
    action TEXT,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
