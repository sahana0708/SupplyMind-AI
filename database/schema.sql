
-- ==========================================
-- SUPPLYMIND AI - DATABASE SCHEMA
-- Day 2: Suppliers Table
-- ==========================================

CREATE TABLE suppliers (
    supplier_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_code VARCHAR(20) UNIQUE NOT NULL,
    supplier_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(30),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    reliability_score NUMERIC(5,2)
        CHECK (reliability_score BETWEEN 0 AND 100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
