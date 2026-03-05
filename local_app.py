"""
Ezi Returns Intelligence Platform - Local Runner (SQLite, no Docker)
Access at: http://localhost:5000
"""

import os
import json
import base64
import re
import random
import sqlite3
from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, jsonify

# ── AI ───────────────────────────────────────────────────────────────────────
try:
    import anthropic
    _key = os.environ.get('ANTHROPIC_API_KEY', '')
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key=_key) if _key else None
    AI_ENABLED = bool(_key)
except Exception:
    ANTHROPIC_CLIENT = None
    AI_ENABLED = False

# ── Paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(_HERE, 'ezi_local.db')

# ── Flask ─────────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder=os.path.join(_HERE, 'backend', 'templates'),
    static_folder=os.path.join(_HERE, 'backend', 'static'),
    static_url_path='/static',
)
app.secret_key = 'ezi-returns-spacer-2026'


def get_db():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fmt_dt(val):
    return str(val)[:16] if val else ''


def fmt_date(val):
    return str(val)[:10] if val else ''


# ── Demo / mock data ──────────────────────────────────────────────────────────
DEMO_ASSESSMENTS = [
    {'condition': 'Good',      'confidence': 82, 'damage_types': ['light surface scratches', 'minor wear on edges'],       'notes': 'Item shows normal signs of use. Core functionality intact. Original accessories present.', 'action': 'Restock',       'estimated_value_recovery': '70-80%'},
    {'condition': 'Like New',  'confidence': 94, 'damage_types': [],                                                       'notes': 'Item appears virtually unused. Original packaging intact with all inserts. No visible wear.', 'action': 'Resell as New', 'estimated_value_recovery': '90-95%'},
    {'condition': 'Poor',      'confidence': 88, 'damage_types': ['cracked housing', 'missing components', 'scuff marks'], 'notes': 'Significant damage present. Refurbishment required before resale. Missing accessories.',   'action': 'Refurbish',     'estimated_value_recovery': '25-40%'},
    {'condition': 'Fair',      'confidence': 79, 'damage_types': ['scratches on display', 'worn grip areas'],              'notes': 'Moderate wear consistent with extended use. Item is functional but cosmetically affected.',  'action': 'Restock',       'estimated_value_recovery': '50-65%'},
]

SYSTEM_PROMPT = """You are the AI customer service assistant for Ezi Returns, a South African
logistics and returns management company. Help customers with return queries, policy questions,
refund timelines, and shipping information. Key policies: 30-day return window, 5-7 business
days for refunds, free returns for defective items, R85 fee for change-of-mind returns.
Be concise, professional, and helpful. Under 150 words unless detail is needed."""

DEMO_RESPONSES = {
    'refund':   'Your refund will be processed within 5-7 business days after our warehouse completes the condition assessment. You will receive an email confirmation once approved.',
    'status':   'To check your return status, please provide your order number (format: EZI-XXXXX) and I will pull up the details right away.',
    'return':   'Starting a return is easy — log into your account, find the order, and select "Request Return". We will email a prepaid label within 2 hours for eligible returns.',
    'shipping': 'We use The Courier Guy, Fastway, and DHL Express. Free return shipping for defective items; a R85 fee applies for change-of-mind returns.',
    'policy':   'Returns accepted within 30 days of purchase. Items should be in original condition with packaging. Electronics must include all accessories.',
    'track':    'Use the tracking number in your return confirmation email, or provide your order number (EZI-XXXXX) and I will check the status for you.',
    'customs':  'For international returns our team handles all customs documentation. You will receive a customs declaration form by email — no action needed on your side.',
}


def mock_response(msg):
    for kw, resp in DEMO_RESPONSES.items():
        if kw in msg.lower():
            return resp
    return 'Happy to help — could you share your order number (EZI-XXXXX) so I can look into this for you?'


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    try:
        get_db().close()
        db = 'ok'
    except Exception:
        db = 'error'
    return jsonify({'status': 'ok', 'db': db, 'ai': AI_ENABLED})


@app.route('/')
def index():
    return render_template('index.html', ai_enabled=AI_ENABLED)


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', ai_enabled=AI_ENABLED)


@app.route('/api/dashboard-data')
def dashboard_data():
    conn = get_db()
    cur = conn.cursor()

    today_returns = cur.execute("SELECT COUNT(*) FROM returns WHERE date(created_at) >= date('now')").fetchone()[0]
    pending       = cur.execute("SELECT COUNT(*) FROM returns WHERE status = 'pending_assessment'").fetchone()[0]
    fraud_alerts  = cur.execute("SELECT COUNT(*) FROM returns WHERE is_flagged = 1 AND fraud_resolved = 0").fetchone()[0]
    cost_savings  = float(cur.execute(
        "SELECT COALESCE(SUM(return_value * 0.68), 0) FROM returns WHERE condition_label IN ('Good','Like New','New/Unused','Fair')"
    ).fetchone()[0] or 0)

    # Trend: Python generates date range, DB supplies counts
    today = date.today()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    raw = cur.execute(
        "SELECT date(created_at) AS d, COUNT(*) AS c FROM returns WHERE date(created_at) >= date('now','-29 days') GROUP BY date(created_at)"
    ).fetchall()
    counts = {r['d']: r['c'] for r in raw}
    trend = [{'date': d, 'count': counts.get(d, 0)} for d in dates]

    conditions = [
        {'label': r['condition_label'], 'count': r['count']}
        for r in cur.execute(
            "SELECT condition_label, COUNT(*) AS count FROM returns WHERE condition_label IS NOT NULL GROUP BY condition_label ORDER BY count DESC"
        ).fetchall()
    ]

    recent = [
        {
            'id': r['id'], 'order_id': r['order_id'], 'customer': r['name'],
            'product': r['product_name'], 'status': r['status'],
            'condition': r['condition_label'],
            'fraud_score': float(r['fraud_score'] or 0),
            'value': float(r['return_value'] or 0),
            'created_at': fmt_dt(r['created_at']),
        }
        for r in cur.execute("""
            SELECT r.id, r.order_id, c.name, r.product_name, r.status,
                   r.condition_label, r.fraud_score, r.return_value, r.created_at
            FROM returns r JOIN customers c ON r.customer_id = c.id
            ORDER BY r.created_at DESC LIMIT 10
        """).fetchall()
    ]

    conn.close()
    return jsonify({
        'kpis': {'today_returns': today_returns, 'pending': pending,
                 'fraud_alerts': fraud_alerts, 'cost_savings': f'R{cost_savings:,.0f}'},
        'trend': trend, 'conditions': conditions, 'recent': recent,
    })


# ── Condition Assessment ──────────────────────────────────────────────────────

@app.route('/condition')
def condition():
    return render_template('condition.html', ai_enabled=AI_ENABLED)


@app.route('/api/assess-condition', methods=['POST'])
def assess_condition():
    demo = request.form.get('demo_mode') == 'true'
    if request.is_json:
        demo = (request.get_json(silent=True) or {}).get('demo_mode', False)

    if demo or not AI_ENABLED:
        assessment = dict(random.choice(DEMO_ASSESSMENTS))
    else:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded. Use Demo mode or upload an image.'}), 400
        raw = request.files['image'].read()
        if not raw:
            return jsonify({'error': 'Empty file.'}), 400
        try:
            msg = ANTHROPIC_CLIENT.messages.create(
                model='claude-sonnet-4-6', max_tokens=1024,
                messages=[{'role': 'user', 'content': [
                    {'type': 'image', 'source': {'type': 'base64', 'media_type': request.files['image'].content_type or 'image/jpeg', 'data': base64.b64encode(raw).decode()}},
                    {'type': 'text', 'text': 'Analyze this returned item. Respond ONLY with JSON: {"condition":"Good","confidence":85,"damage_types":[],"notes":"...","action":"Restock","estimated_value_recovery":"70-80%"}. Condition: New/Unused|Like New|Good|Fair|Poor|Damaged/Unusable. Action: Resell as New|Restock|Refurbish|Liquidate|Dispose.'},
                ]}],
            )
            text = msg.content[0].text
            m = re.search(r'\{.*\}', text, re.DOTALL)
            assessment = json.loads(m.group()) if m else {'error': 'Parse error', 'raw': text}
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO condition_assessments (condition_label,confidence,damage_types,ai_notes,action,assessed_at) VALUES (?,?,?,?,?,datetime('now'))",
            (assessment.get('condition'), assessment.get('confidence'),
             json.dumps(assessment.get('damage_types', [])), assessment.get('notes'), assessment.get('action')),
        )
        assessment['id'] = cur.lastrowid
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify(assessment)


@app.route('/api/recent-assessments')
def recent_assessments():
    conn = get_db()
    rows = conn.execute(
        "SELECT id,condition_label,confidence,ai_notes,action,assessed_at FROM condition_assessments ORDER BY assessed_at DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return jsonify([
        {'id': r['id'], 'condition': r['condition_label'], 'confidence': r['confidence'],
         'notes': r['ai_notes'], 'action': r['action'], 'assessed_at': fmt_dt(r['assessed_at'])}
        for r in rows
    ])


# ── Chat ──────────────────────────────────────────────────────────────────────

@app.route('/chat')
def chat():
    return render_template('chat.html', ai_enabled=AI_ENABLED)


@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(force=True)
    msg = (data.get('message') or '').strip()
    history = data.get('history', [])
    sid = data.get('session_id') or f'local-{random.randint(10000, 99999)}'

    if not msg:
        return jsonify({'error': 'Empty message'}), 400

    if not AI_ENABLED:
        reply = mock_response(msg)
    else:
        messages = [{'role': m['role'], 'content': m['content']} for m in history[-10:]]
        messages.append({'role': 'user', 'content': msg})
        try:
            resp = ANTHROPIC_CLIENT.messages.create(
                model='claude-sonnet-4-6', max_tokens=512,
                system=SYSTEM_PROMPT, messages=messages,
            )
            reply = resp.content[0].text
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    try:
        conn = get_db()
        conn.execute("INSERT INTO chat_conversations (session_id,role,content) VALUES (?,'user',?)", (sid, msg))
        conn.execute("INSERT INTO chat_conversations (session_id,role,content) VALUES (?,'assistant',?)", (sid, reply))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify({'message': reply, 'session_id': sid})


# ── Fraud Detection ───────────────────────────────────────────────────────────

@app.route('/fraud')
def fraud():
    return render_template('fraud.html', ai_enabled=AI_ENABLED)


@app.route('/api/fraud-data')
def fraud_data():
    conn = get_db()
    cur = conn.cursor()

    active    = cur.execute("SELECT COUNT(*) FROM returns WHERE is_flagged=1 AND fraud_resolved=0").fetchone()[0]
    avg_score = float(cur.execute("SELECT AVG(fraud_score) FROM returns WHERE is_flagged=1").fetchone()[0] or 0)
    exposed   = float(cur.execute("SELECT COALESCE(SUM(return_value),0) FROM returns WHERE is_flagged=1 AND fraud_resolved=0").fetchone()[0] or 0)
    resolved  = cur.execute("SELECT COUNT(*) FROM returns WHERE is_flagged=1 AND fraud_resolved=1 AND date(updated_at)=date('now')").fetchone()[0]

    flagged = [
        {
            'id': r['id'], 'order_id': r['order_id'], 'customer': r['name'], 'email': r['email'],
            'product': r['product_name'], 'fraud_score': float(r['fraud_score'] or 0),
            'reason': r['flag_reason'], 'value': float(r['return_value'] or 0),
            'date': fmt_date(r['created_at']), 'resolved': bool(r['fraud_resolved']),
            'total_returns': r['total_returns'], 'return_rate': float(r['return_rate'] or 0),
        }
        for r in cur.execute("""
            SELECT r.id,r.order_id,c.name,c.email,r.product_name,r.fraud_score,
                   r.flag_reason,r.return_value,r.created_at,r.fraud_resolved,
                   c.total_returns,c.return_rate
            FROM returns r JOIN customers c ON r.customer_id=c.id
            WHERE r.is_flagged=1
            ORDER BY r.fraud_resolved ASC, r.fraud_score DESC LIMIT 20
        """).fetchall()
    ]

    risk_dist = [
        {'band': r['risk_band'], 'count': r['count']}
        for r in cur.execute("""
            SELECT CASE WHEN fraud_score>=80 THEN 'Critical (80-100)'
                        WHEN fraud_score>=60 THEN 'High (60-79)'
                        WHEN fraud_score>=40 THEN 'Medium (40-59)'
                        ELSE 'Low (0-39)' END AS risk_band,
                   COUNT(*) AS count
            FROM returns WHERE is_flagged=1
            GROUP BY risk_band ORDER BY MIN(fraud_score) DESC
        """).fetchall()
    ]

    conn.close()
    return jsonify({
        'stats': {'active_flags': active, 'avg_risk_score': round(avg_score, 1),
                  'exposed_value': f'R{exposed:,.0f}', 'resolved_today': resolved},
        'flagged': flagged, 'risk_distribution': risk_dist,
    })


@app.route('/api/resolve-flag/<int:return_id>', methods=['POST'])
def resolve_flag(return_id):
    conn = get_db()
    conn.execute("UPDATE returns SET fraud_resolved=1, updated_at=datetime('now') WHERE id=?", (return_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'resolved', 'id': return_id})


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if not os.path.exists(SQLITE_PATH):
        print(f'\nDatabase not found. Run first:\n  python.exe init_local_db.py\n')
        raise SystemExit(1)
    print('\n' + '=' * 48)
    print('  EZI Returns Intelligence Platform')
    print('  http://localhost:5000')
    if AI_ENABLED:
        print('  AI: Live (Claude)')
    else:
        print('  AI: Demo mode (set ANTHROPIC_API_KEY for live)')
    print('=' * 48 + '\n')
    app.run(debug=True, host='127.0.0.1', port=5000)
