# BOK Immutable Input Log - Ezi Returns SPACER

## Purpose
This log records all inputs to the Body of Knowledge (BOK) for the Ezi Returns SPACER.
Entries are IMMUTABLE - never edited, only appended. This log is the audit trail.

---

## Input #001
**Date:** 2026-03-05
**Type:** Proposal Document
**Source:** `PROP EZI Returns 27022026.docx`
**Processed by:** SPACER Phase S/P (Scope and Prepare)

**Key extractions:**
- Client: Ezi Returns (logistics/returns management, South Africa)
- Stakeholders: Mark Burch (CEO), Lorna (Operations), Ant (E-commerce, 15yr exp)
- Discovery meeting held prior to proposal
- 4 priority use cases identified:
  1. Customer service automation (FAQ handling, query routing, multi-channel)
  2. Automated condition assessment (image-based, classification, confidence scoring)
  3. AI-assisted routing optimization (dynamic re-routing, cost optimization, consolidation)
  4. Fraud and abuse detection (pattern recognition, risk scoring, flagging)
- Integration priority: Expandly platform (order/return data sync)
- Other integrations: Shipping/logistics APIs, customs systems, payment/financial systems
- Compliance: POPIA, audit logging, data retention
- Delivery: 4 phases over ~9 months, then ongoing
- Commercial: R500/hr blended rate, R655k-R815k total estimated (Phases 0-3)

**Notes:** Single discovery session - requirements need validation via Phase 0 elicitation.

---

## Input #002
**Date:** 2026-03-05
**Type:** Methodology Document
**Source:** `SPACER_Methodology_Checklist.docx`
**Processed by:** SPACER Phase S

**Key extractions:**
- SPACER = Sales-Proactive Accelerated Client Engagement through Rapid Prototyping
- Stack: Flask + PostgreSQL + Redis + Docker Compose + Nginx (proven pattern)
- AI: Anthropic Claude API (claude-sonnet-4-6)
- 6 phases: Scope, Prepare, Architect, Code, Embellish, Release
- Hero features: 3-5 features that prove the concept
- Realistic sample data minimum: 50-100 records
- Brand early: apply colours and logo in first coding hour

---

## Status
- [x] Input #001 processed into BRIEF.MD
- [x] Input #002 processed into CLAUDE.md
- [x] Domain model designed (see CLAUDE.md)
- [x] Sample data SQL generated (see database/init/02_sample_data.sql)
- [ ] Brand assets (logo, colours extracted from website)
- [ ] Client confirmation of hero features
