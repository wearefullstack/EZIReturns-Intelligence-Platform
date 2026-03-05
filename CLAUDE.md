# Ezi Returns SPACER

## Project Type
SPACER - Sales prototype, 3-day build. Not production. No unit tests, no CI/CD, no
comprehensive error handling. Focus on the demo path.

## Tech Stack
- Backend: Python (Flask) with Gunicorn
- Frontend: Jinja2 templates + Bootstrap 5.3 + Chart.js 4.x (CDN)
- Database: PostgreSQL 16
- Cache: Redis 7 (Alpine)
- AI: Anthropic Claude (claude-sonnet-4-6) - with mock mode if no API key
- Container: Docker Compose
- Proxy: Nginx (Alpine)
- Auth: None (demo only)

## Brand Rules
- Primary: #0A4C8A | Primary light: #1565C0 | Dark: #082C5A
- Secondary: #00BDA5 (teal)
- Accent: #F5A623 (amber)
- Background: #F0F4F8 | Card: #FFFFFF
- Text: #2C3E50 | Muted: #6C7D8C
- All cards: white background with box-shadow: 0 2px 12px rgba(0,0,0,0.08)
- Navbar: primary gradient (#0A4C8A to #082C5A)
- Footer: "Powered by Full Stack" subtle dark footer

## Key Commands
```bash
docker-compose up --build        # Start everything
docker-compose logs -f backend   # Watch backend logs
docker-compose down -v           # Clean restart (wipes DB)
docker-compose restart           # Restart without rebuild
```

App runs at: http://localhost

## Domain Context
- **Return**: A physical item sent back by a customer requesting refund or exchange
- **Condition Assessment**: AI evaluation of returned item physical state (New/Like New/Good/Fair/Poor/Damaged)
- **Fraud Score**: 0-100 risk rating. >60 = flagged for review. >80 = critical
- **Return Rate**: Customer's returns / orders ratio. >0.5 = high risk
- **POPIA**: SA Protection of Personal Information Act (equivalent to GDPR)
- **Expandly**: E-commerce platform used by Ezi for order management
- **BOK**: Body of Knowledge - all inputs that inform the prototype

## Data Model
- `customers` - customer profiles with return history and risk scoring
- `returns` - individual return transactions (linked to customers)
- `condition_assessments` - AI assessment results (standalone, linked to return optionally)
- `chat_conversations` - customer service chat history by session

## Return Statuses
- `pending_assessment` - received, awaiting condition check
- `assessed` - AI assessment complete, awaiting decision
- `approved` - return approved, processing refund
- `rejected` - return rejected (policy violation)
- `refunded` - refund issued
- `in_transit` - item en route back to warehouse

## Demo Script (10 minutes)
1. **Landing page** (30s) - "This is the platform we've built for you"
2. **Dashboard** (2min) - Walk KPIs, trend chart, condition donut, recent table
3. **Condition Assessment** (2min) - Click Demo Assessment, show AI analysis
4. **Customer Chat** (1.5min) - Type "How do I track my return?" - show AI response
5. **Fraud Detection** (1.5min) - Show flagged returns, risk scores, patterns
6. **Close** (30s) - "Phase 1 delivery: 3 months, R200k-250k"

## Environment Variables (.env)
- `ANTHROPIC_API_KEY` - Set for live AI; leave blank for demo/mock mode
- `SECRET_KEY` - Flask session key
- `DATABASE_URL` - Auto-set by Docker Compose
