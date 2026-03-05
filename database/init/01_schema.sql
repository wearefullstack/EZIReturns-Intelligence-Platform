-- Ezi Returns Intelligence Platform - Database Schema
-- PostgreSQL 16

CREATE TABLE IF NOT EXISTS customers (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    phone         VARCHAR(25),
    city          VARCHAR(80),
    total_orders  INTEGER DEFAULT 0,
    total_returns INTEGER DEFAULT 0,
    return_rate   DECIMAL(5,4) DEFAULT 0,
    risk_score    INTEGER DEFAULT 0,
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS returns (
    id              SERIAL PRIMARY KEY,
    order_id        VARCHAR(20) UNIQUE NOT NULL,
    customer_id     INTEGER REFERENCES customers(id),
    product_name    VARCHAR(200) NOT NULL,
    product_sku     VARCHAR(50),
    carrier         VARCHAR(80),
    status          VARCHAR(40) DEFAULT 'pending_assessment',
    condition_label VARCHAR(50),
    condition_score INTEGER,
    fraud_score     DECIMAL(5,2) DEFAULT 0,
    is_flagged      BOOLEAN DEFAULT FALSE,
    fraud_resolved  BOOLEAN DEFAULT FALSE,
    flag_reason     TEXT,
    return_value    DECIMAL(10,2),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS condition_assessments (
    id              SERIAL PRIMARY KEY,
    return_id       INTEGER REFERENCES returns(id),
    condition_label VARCHAR(50),
    confidence      INTEGER,
    damage_types    JSONB DEFAULT '[]',
    ai_notes        TEXT,
    action          VARCHAR(80),
    assessed_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_conversations (
    id         SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    role       VARCHAR(20) NOT NULL,
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_returns_customer   ON returns(customer_id);
CREATE INDEX IF NOT EXISTS idx_returns_status     ON returns(status);
CREATE INDEX IF NOT EXISTS idx_returns_flagged    ON returns(is_flagged) WHERE is_flagged = TRUE;
CREATE INDEX IF NOT EXISTS idx_returns_created    ON returns(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_session       ON chat_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_assessments_date   ON condition_assessments(assessed_at DESC);
