import os
import json
import base64
import re
import random
import time
from datetime import datetime

from flask import Flask, render_template, request, jsonify

try:
    import anthropic
    _api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    ANTHROPIC_CLIENT = anthropic.Anthropic(api_key=_api_key) if _api_key else None
    AI_ENABLED = bool(_api_key)
except Exception:
    ANTHROPIC_CLIENT = None
    AI_ENABLED = False

import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ezi-returns-spacer-2026')

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://ezi_user:ezi_pass@postgres:5432/ezi_returns'
)

SYSTEM_PROMPT = """You are the AI customer service assistant for Ezi Returns, a South African
logistics and returns management company.

You help customers with:
- Return status inquiries (ask for order number in format EZI-XXXXX)
- How to initiate a return
- Return policy questions
- Refund timelines and amounts
- Shipping and carrier questions
- Customs and international return queries

Key policies:
- Returns accepted within 30 days of purchase
- Items should be in original condition with packaging where possible
- Refunds processed within 5-7 business days after condition assessment
- Free return shipping for defective or incorrect items
- R85 return shipping fee for change-of-mind returns
- Partner carriers: The Courier Guy, Fastway, DHL Express, Aramex
- Integration with Expandly for e-commerce order tracking

Be helpful, concise, and professional. If you cannot find specific account details,
explain what information you need. Respond in the same language the customer uses.
Keep responses under 150 words unless detail is needed."""

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def get_db():
    for attempt in range(5):
        try:
            return psycopg2.connect(DATABASE_URL)
        except Exception:
            if attempt < 4:
                time.sleep(2)
            else:
                raise


# ---------------------------------------------------------------------------
# Demo / mock data helpers
# ---------------------------------------------------------------------------

DEMO_ASSESSMENTS = [
    {
        'condition': 'Good',
        'confidence': 82,
        'damage_types': ['light surface scratches', 'minor wear on edges'],
        'notes': 'Item shows normal signs of use. Core functionality intact. Original accessories present. Suitable for restocking at reduced price.',
        'action': 'Restock',
        'estimated_value_recovery': '70-80%',
    },
    {
        'condition': 'Like New',
        'confidence': 94,
        'damage_types': [],
        'notes': 'Item appears virtually unused. Original packaging intact with all inserts. No visible wear or marks detected.',
        'action': 'Resell as New',
        'estimated_value_recovery': '90-95%',
    },
    {
        'condition': 'Poor',
        'confidence': 88,
        'damage_types': ['cracked housing', 'missing components', 'visible scuff marks'],
        'notes': 'Significant damage present. Item requires professional refurbishment before any resale. Missing charging accessories.',
        'action': 'Refurbish',
        'estimated_value_recovery': '25-40%',
    },
    {
        'condition': 'Fair',
        'confidence': 79,
        'damage_types': ['scratches on display', 'worn grip areas'],
        'notes': 'Moderate wear consistent with extended use. Cosmetic damage present but item is fully functional.',
        'action': 'Restock',
        'estimated_value_recovery': '50-65%',
    },
]

DEMO_CHAT_RESPONSES = {
    'refund': 'Your refund will be processed within 5-7 business days after our warehouse completes the condition assessment. You will receive an email confirmation with the refund amount once approved.',
    'status': 'To check your return status, please provide your order number (format: EZI-XXXXX) and I will pull up the details for you right away.',
    'return': 'Starting a return is straightforward. Log into your account, locate the order, and select "Request Return". Choose your reason and we will email a prepaid shipping label within 2 hours for eligible returns.',
    'shipping': 'We use The Courier Guy, Fastway, and DHL Express for returns. Free return shipping applies to defective or incorrect items. A R85 fee applies for change-of-mind returns.',
    'policy': 'Our return policy allows returns within 30 days of purchase. Items should be in original condition with packaging. Electronics must include all accessories. Some items (e.g. perishables, custom orders) are non-returnable.',
    'track': 'You can track your return shipment using the tracking number in your return confirmation email. Alternatively, provide your order number (EZI-XXXXX) and I will check the current status.',
    'customs': 'For international returns, our team handles all customs documentation. You will receive a customs declaration form by email. Duties and taxes on returned goods are typically waived but depend on the origin country.',
}


def mock_chat_response(message: str) -> str:
    msg_lower = message.lower()
    for keyword, response in DEMO_CHAT_RESPONSES.items():
        if keyword in msg_lower:
            return response
    return (
        'I am happy to help with your return. Could you please provide your order number '
        '(format: EZI-XXXXX) so I can look into this for you directly?'
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/health')
def health():
    db_ok = False
    try:
        conn = get_db()
        conn.close()
        db_ok = True
    except Exception:
        pass
    return jsonify({'status': 'ok', 'db': 'ok' if db_ok else 'error', 'ai': AI_ENABLED})


@app.route('/')
def index():
    return render_template('index.html', ai_enabled=AI_ENABLED)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', ai_enabled=AI_ENABLED)


@app.route('/api/dashboard-data')
def dashboard_data():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT COUNT(*) AS c FROM returns WHERE created_at >= CURRENT_DATE")
    today_returns = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) AS c FROM returns WHERE status = 'pending_assessment'")
    pending = cur.fetchone()['c']

    cur.execute(
        "SELECT COUNT(*) AS c FROM returns WHERE is_flagged = TRUE AND fraud_resolved = FALSE"
    )
    fraud_alerts = cur.fetchone()['c']

    cur.execute("""
        SELECT COALESCE(SUM(return_value * 0.68), 0) AS savings
        FROM returns
        WHERE condition_label IN ('Good', 'Like New', 'New/Unused', 'Fair')
    """)
    cost_savings = float(cur.fetchone()['savings'] or 0)

    # 30-day trend
    cur.execute("""
        SELECT gs::date AS date, COALESCE(COUNT(r.id), 0) AS count
        FROM generate_series(
            CURRENT_DATE - INTERVAL '29 days',
            CURRENT_DATE,
            '1 day'::interval
        ) gs
        LEFT JOIN returns r ON DATE(r.created_at) = gs::date
        GROUP BY gs::date
        ORDER BY gs::date
    """)
    trend = [{'date': str(r['date']), 'count': int(r['count'])} for r in cur.fetchall()]

    # Condition distribution
    cur.execute("""
        SELECT condition_label, COUNT(*) AS count
        FROM returns
        WHERE condition_label IS NOT NULL
        GROUP BY condition_label
        ORDER BY count DESC
    """)
    conditions = [{'label': r['condition_label'], 'count': r['count']} for r in cur.fetchall()]

    # Recent returns
    cur.execute("""
        SELECT r.id, r.order_id, c.name, r.product_name, r.status,
               r.condition_label, r.fraud_score, r.return_value, r.created_at
        FROM returns r
        JOIN customers c ON r.customer_id = c.id
        ORDER BY r.created_at DESC
        LIMIT 10
    """)
    recent = [
        {
            'id': r['id'],
            'order_id': r['order_id'],
            'customer': r['name'],
            'product': r['product_name'],
            'status': r['status'],
            'condition': r['condition_label'],
            'fraud_score': float(r['fraud_score'] or 0),
            'value': float(r['return_value'] or 0),
            'created_at': r['created_at'].strftime('%Y-%m-%d %H:%M'),
        }
        for r in cur.fetchall()
    ]

    conn.close()
    return jsonify({
        'kpis': {
            'today_returns': today_returns,
            'pending': pending,
            'fraud_alerts': fraud_alerts,
            'cost_savings': f'R{cost_savings:,.0f}',
        },
        'trend': trend,
        'conditions': conditions,
        'recent': recent,
    })


# ---------------------------------------------------------------------------
# Condition Assessment
# ---------------------------------------------------------------------------

@app.route('/condition')
def condition():
    return render_template('condition.html', ai_enabled=AI_ENABLED)


@app.route('/api/assess-condition', methods=['POST'])
def assess_condition():
    use_demo = request.form.get('demo_mode') == 'true'
    if request.is_json:
        use_demo = request.get_json(silent=True, force=True).get('demo_mode', False)

    assessment = None

    if use_demo or not AI_ENABLED:
        assessment = dict(random.choice(DEMO_ASSESSMENTS))
    else:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded. Use demo mode or upload an image.'}), 400
        file = request.files['image']
        raw = file.read()
        if not raw:
            return jsonify({'error': 'Empty file uploaded.'}), 400
        image_b64 = base64.b64encode(raw).decode('utf-8')
        media_type = file.content_type or 'image/jpeg'

        try:
            msg = ANTHROPIC_CLIENT.messages.create(
                model='claude-sonnet-4-6',
                max_tokens=1024,
                messages=[{
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': media_type,
                                'data': image_b64,
                            },
                        },
                        {
                            'type': 'text',
                            'text': (
                                'You are Ezi Returns\' AI condition assessment system. '
                                'Analyze this returned item image and respond ONLY with valid JSON:\n'
                                '{\n'
                                '  "condition": "Good",\n'
                                '  "confidence": 85,\n'
                                '  "damage_types": ["scratch on surface"],\n'
                                '  "notes": "Brief 2-sentence assessment.",\n'
                                '  "action": "Restock",\n'
                                '  "estimated_value_recovery": "70-80%"\n'
                                '}\n\n'
                                'Condition must be one of: New/Unused, Like New, Good, Fair, Poor, Damaged/Unusable\n'
                                'Action must be one of: Resell as New, Restock, Refurbish, Liquidate, Dispose'
                            ),
                        },
                    ],
                }],
            )
            text = msg.content[0].text
            m = re.search(r'\{.*\}', text, re.DOTALL)
            assessment = json.loads(m.group()) if m else {'error': 'Parse error', 'raw': text}
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Persist to DB
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO condition_assessments
                (condition_label, confidence, damage_types, ai_notes, action, assessed_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id
            """,
            (
                assessment.get('condition'),
                assessment.get('confidence'),
                json.dumps(assessment.get('damage_types', [])),
                assessment.get('notes'),
                assessment.get('action'),
            ),
        )
        assessment['id'] = cur.fetchone()[0]
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify(assessment)


@app.route('/api/recent-assessments')
def recent_assessments():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT id, condition_label, confidence, ai_notes, action, assessed_at
        FROM condition_assessments
        ORDER BY assessed_at DESC
        LIMIT 6
    """)
    results = [
        {
            'id': r['id'],
            'condition': r['condition_label'],
            'confidence': r['confidence'],
            'notes': r['ai_notes'],
            'action': r['action'],
            'assessed_at': r['assessed_at'].strftime('%Y-%m-%d %H:%M'),
        }
        for r in cur.fetchall()
    ]
    conn.close()
    return jsonify(results)


# ---------------------------------------------------------------------------
# Customer Chat
# ---------------------------------------------------------------------------

@app.route('/chat')
def chat():
    return render_template('chat.html', ai_enabled=AI_ENABLED)


@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(force=True)
    user_message = (data.get('message') or '').strip()
    history = data.get('history', [])
    session_id = data.get('session_id') or f'session-{random.randint(10000, 99999)}'

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    if not AI_ENABLED:
        reply = mock_chat_response(user_message)
    else:
        messages = [
            {'role': m['role'], 'content': m['content']}
            for m in history[-10:]
        ]
        messages.append({'role': 'user', 'content': user_message})
        try:
            response = ANTHROPIC_CLIENT.messages.create(
                model='claude-sonnet-4-6',
                max_tokens=512,
                system=SYSTEM_PROMPT,
                messages=messages,
            )
            reply = response.content[0].text
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Persist chat
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_conversations (session_id, role, content) VALUES (%s, 'user', %s)",
            (session_id, user_message),
        )
        cur.execute(
            "INSERT INTO chat_conversations (session_id, role, content) VALUES (%s, 'assistant', %s)",
            (session_id, reply),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

    return jsonify({'message': reply, 'session_id': session_id})


# ---------------------------------------------------------------------------
# Fraud Detection
# ---------------------------------------------------------------------------

@app.route('/fraud')
def fraud():
    return render_template('fraud.html', ai_enabled=AI_ENABLED)


@app.route('/api/fraud-data')
def fraud_data():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        "SELECT COUNT(*) AS c FROM returns WHERE is_flagged = TRUE AND fraud_resolved = FALSE"
    )
    active_flags = cur.fetchone()['c']

    cur.execute("SELECT AVG(fraud_score) AS avg FROM returns WHERE is_flagged = TRUE")
    avg_score = float(cur.fetchone()['avg'] or 0)

    cur.execute(
        "SELECT COALESCE(SUM(return_value), 0) AS val FROM returns WHERE is_flagged = TRUE AND fraud_resolved = FALSE"
    )
    exposed_value = float(cur.fetchone()['val'] or 0)

    cur.execute(
        "SELECT COUNT(*) AS c FROM returns WHERE is_flagged = TRUE AND fraud_resolved = TRUE AND DATE(updated_at) = CURRENT_DATE"
    )
    resolved_today = cur.fetchone()['c']

    cur.execute("""
        SELECT r.id, r.order_id, c.name, c.email, r.product_name,
               r.fraud_score, r.flag_reason, r.return_value, r.created_at,
               r.fraud_resolved, c.total_returns, c.return_rate
        FROM returns r
        JOIN customers c ON r.customer_id = c.id
        WHERE r.is_flagged = TRUE
        ORDER BY r.fraud_resolved ASC, r.fraud_score DESC
        LIMIT 20
    """)
    flagged = [
        {
            'id': r['id'],
            'order_id': r['order_id'],
            'customer': r['name'],
            'email': r['email'],
            'product': r['product_name'],
            'fraud_score': float(r['fraud_score'] or 0),
            'reason': r['flag_reason'],
            'value': float(r['return_value'] or 0),
            'date': r['created_at'].strftime('%Y-%m-%d'),
            'resolved': r['fraud_resolved'],
            'total_returns': r['total_returns'],
            'return_rate': float(r['return_rate'] or 0),
        }
        for r in cur.fetchall()
    ]

    cur.execute("""
        SELECT
            CASE
                WHEN fraud_score >= 80 THEN 'Critical (80-100)'
                WHEN fraud_score >= 60 THEN 'High (60-79)'
                WHEN fraud_score >= 40 THEN 'Medium (40-59)'
                ELSE 'Low (0-39)'
            END AS risk_band,
            COUNT(*) AS count
        FROM returns
        WHERE is_flagged = TRUE
        GROUP BY risk_band
        ORDER BY MIN(fraud_score) DESC
    """)
    risk_dist = [{'band': r['risk_band'], 'count': r['count']} for r in cur.fetchall()]

    conn.close()
    return jsonify({
        'stats': {
            'active_flags': active_flags,
            'avg_risk_score': round(avg_score, 1),
            'exposed_value': f'R{exposed_value:,.0f}',
            'resolved_today': resolved_today,
        },
        'flagged': flagged,
        'risk_distribution': risk_dist,
    })


@app.route('/api/resolve-flag/<int:return_id>', methods=['POST'])
def resolve_flag(return_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE returns SET fraud_resolved = TRUE, updated_at = NOW() WHERE id = %s",
        (return_id,),
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'resolved', 'id': return_id})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
