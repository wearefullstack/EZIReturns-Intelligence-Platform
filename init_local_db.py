"""
Ezi Returns - Local Database Initializer
Creates and seeds a SQLite database for local development.
Run once before starting local_app.py.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ezi_local.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    phone         TEXT,
    city          TEXT,
    total_orders  INTEGER DEFAULT 0,
    total_returns INTEGER DEFAULT 0,
    return_rate   REAL DEFAULT 0,
    risk_score    INTEGER DEFAULT 0,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS returns (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        TEXT UNIQUE NOT NULL,
    customer_id     INTEGER REFERENCES customers(id),
    product_name    TEXT NOT NULL,
    product_sku     TEXT,
    carrier         TEXT,
    status          TEXT DEFAULT 'pending_assessment',
    condition_label TEXT,
    condition_score INTEGER,
    fraud_score     REAL DEFAULT 0,
    is_flagged      INTEGER DEFAULT 0,
    fraud_resolved  INTEGER DEFAULT 0,
    flag_reason     TEXT,
    return_value    REAL,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS condition_assessments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    return_id       INTEGER REFERENCES returns(id),
    condition_label TEXT,
    confidence      INTEGER,
    damage_types    TEXT DEFAULT '[]',
    ai_notes        TEXT,
    action          TEXT,
    assessed_at     TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chat_conversations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role       TEXT NOT NULL,
    content    TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
"""


def dt(hours=0, days=0):
    return (datetime.now() - timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')


def main():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        conn.close()
        if count > 0:
            print(f"Already initialised at: {DB_PATH}")
            print("Delete ezi_local.db to re-seed.")
            return

    print(f"Creating database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    cur = conn.cursor()

    # ── Customers ────────────────────────────────────────────────────────────
    customers = [
        ('Sipho Dlamini',       'sipho.dlamini@gmail.com',       '+27 82 345 6789', 'Cape Town',        24, 3,  0.1250, 12),
        ('Priya Naidoo',        'priya.naidoo@webmail.co.za',    '+27 83 456 7890', 'Durban',           18, 2,  0.1111, 8),
        ('Johan van der Merwe', 'jvdm@outlook.com',              '+27 71 234 5678', 'Pretoria',         31, 4,  0.1290, 15),
        ('Zanele Mokoena',      'zanele.m@yahoo.com',            '+27 76 567 8901', 'Johannesburg',     12, 7,  0.5833, 72),
        ('Thabo Nkosi',         'thabo.nkosi@icloud.com',        '+27 82 678 9012', 'Cape Town',        9,  1,  0.1111, 5),
        ('Liezel du Plessis',   'liezel.dp@mweb.co.za',          '+27 72 789 0123', 'Stellenbosch',     22, 3,  0.1364, 10),
        ('Naledi Khumalo',      'naledi.khumalo@gmail.com',      '+27 79 890 1234', 'Soweto',           7,  5,  0.7143, 88),
        ('Riku Maharaj',        'riku.maharaj@hotmail.com',      '+27 83 901 2345', 'Durban',           15, 2,  0.1333, 9),
        ('Francois Botha',      'fbotha@gmail.com',              '+27 82 012 3456', 'George',           20, 3,  0.1500, 18),
        ('Aisha Parker',        'aisha.parker@gmail.com',        '+27 71 123 4567', 'Cape Town',        11, 1,  0.0909, 4),
        ('David Chen',          'david.chen@gmail.com',          '+27 83 234 5678', 'Cape Town',        28, 4,  0.1429, 14),
        ('Nomsa Dube',          'nomsa.dube@vodamail.co.za',     '+27 76 345 6789', 'Pietermaritzburg', 8,  6,  0.7500, 91),
        ('Werner Grobler',      'wgrobler@telkomsa.net',         '+27 82 456 7890', 'Bloemfontein',     19, 2,  0.1053, 7),
        ('Fatima Abrahams',     'fatima.a@gmail.com',            '+27 71 567 8901', 'Cape Town',        14, 2,  0.1429, 11),
        ('Bongani Zulu',        'bongani.zulu@gmail.com',        '+27 79 678 9012', 'Johannesburg',     6,  4,  0.6667, 79),
    ]
    cur.executemany(
        "INSERT INTO customers (name,email,phone,city,total_orders,total_returns,return_rate,risk_score) VALUES (?,?,?,?,?,?,?,?)",
        customers,
    )

    # ── Returns ───────────────────────────────────────────────────────────────
    # (order_id, cust_id, product, sku, carrier, status, condition, cond_score, fraud_score, flagged, resolved, flag_reason, value, created_at)
    R = [
        # Recent (today)
        ('EZI-20261', 1,  'Samsung Galaxy S24 Ultra 256GB',   'SAM-S24U-256',  'DHL Express',       'pending_assessment', None,              None, 4.2,  0, 0, None, 22999.00, dt(hours=2)),
        ('EZI-20262', 3,  'Apple iPhone 15 Pro Max 256GB',    'APL-I15PM-256', 'The Courier Guy',   'pending_assessment', None,              None, 3.8,  0, 0, None, 27499.00, dt(hours=4)),
        ('EZI-20263', 6,  'Sony WH-1000XM5 Headphones',       'SNY-WH1000-5',  'Fastway Couriers',  'assessed',           'Good',            78,   5.1,  0, 0, None, 6999.00,  dt(hours=6)),
        ('EZI-20264', 12, 'Apple AirPods Pro 2nd Gen',         'APL-APPRO-2',   'DHL Express',       'approved',           'Like New',        92,   88.5, 1, 0, 'Return frequency exceeds policy limits (4 returns in 30 days)', 5499.00, dt(hours=8)),
        ('EZI-20265', 2,  'Nike Air Max 270 Running Shoes',    'NKE-AM270-42',  'Aramex',            'refunded',           'Good',            75,   2.3,  0, 0, None, 2799.00,  dt(hours=10)),
        ('EZI-20266', 7,  'iPad Pro 11" M4 Wi-Fi 256GB',       'APL-IPRO11-M4', 'PostNet',           'pending_assessment', None,              None, 91.2, 1, 0, 'High-value item returned without defect claim; serial return pattern detected', 19999.00, dt(hours=12)),
        ('EZI-20267', 5,  'Dyson V15 Detect Absolute Vacuum',  'DYS-V15-ABS',   'The Courier Guy',   'assessed',           'Like New',        94,   1.8,  0, 0, None, 12999.00, dt(hours=14)),
        ('EZI-20268', 11, 'Adidas Ultraboost 23 - Size 10',    'ADI-UB23-10',   'Fastway Couriers',  'refunded',           'Good',            71,   6.2,  0, 0, None, 3299.00,  dt(hours=16)),
        ('EZI-20269', 4,  'Nintendo Switch OLED Console',      'NIN-SWOL-WHT',  'The Courier Guy',   'approved',           'Fair',            55,   73.4, 1, 0, 'Return after extended use (27 days); customer account flagged', 7499.00, dt(hours=18)),
        ('EZI-20270', 9,  'Garmin Forerunner 265 Watch',       'GAR-FR265-BLK', 'DHL Express',       'assessed',           'Good',            80,   3.1,  0, 0, None, 8999.00,  dt(hours=20)),
        # 4 days ago
        ('EZI-20251', 13, 'Samsung Galaxy S24 Ultra 512GB',    'SAM-S24U-512',  'Aramex',            'refunded',           'Like New',        91,   4.5,  0, 0, None, 24999.00, dt(days=4)),
        ('EZI-20252', 7,  'LG 55" OLED C3 TV',                 'LG-OLED55-C3',  'DHL Express',       'rejected',           'Damaged/Unusable',15,   85.3, 1, 0, 'Damage inconsistent with reported fault; serial number mismatch detected', 24999.00, dt(days=4, hours=2)),
        ('EZI-20253', 14, 'JBL Flip 6 Portable Speaker',       'JBL-FLP6-BLK',  'PostNet',           'refunded',           'Good',            77,   2.1,  0, 0, None, 2999.00,  dt(days=4, hours=3)),
        ('EZI-20254', 10, 'Makita Cordless Drill Set 18V',      'MAK-DDF481-KIT','Fastway Couriers',  'approved',           'Like New',        89,   3.4,  0, 0, None, 4599.00,  dt(days=4, hours=5)),
        ('EZI-20255', 15, 'Apple iPhone 15 Pro Max 512GB',      'APL-I15PM-512', 'DHL Express',       'approved',           'Fair',            60,   76.8, 1, 0, 'Multiple returns from same address; return value anomaly detected', 30999.00, dt(days=4, hours=6)),
        # 7 days ago
        ('EZI-20241', 1,  'DJI Mini 4 Pro Drone Combo',        'DJI-M4P-CMBO',  'The Courier Guy',   'refunded',           'Good',            74,   5.2,  0, 0, None, 18999.00, dt(days=7)),
        ('EZI-20242', 8,  'Sony WH-1000XM5 Headphones',        'SNY-WH1000-5B', 'Aramex',            'refunded',           'New/Unused',      99,   2.8,  0, 0, None, 6999.00,  dt(days=7, hours=1)),
        ('EZI-20243', 12, 'Samsung Galaxy Tab S9 Ultra',       'SAM-TABS9U',    'DHL Express',       'approved',           'Good',            72,   90.1, 1, 0, "Customer's 3rd high-value return in 6 weeks; return rate 75%", 21999.00, dt(days=7, hours=2)),
        ('EZI-20244', 6,  "Levi's 512 Slim Taper Jeans W34",   'LVI-512-3234',  'PostNet',           'refunded',           'New/Unused',      98,   1.5,  0, 0, None, 1299.00,  dt(days=7, hours=4)),
        ('EZI-20245', 11, 'Bose QuietComfort 45 Headphones',   'BSE-QC45-BLK',  'Fastway Couriers',  'assessed',           'Like New',        93,   4.1,  0, 0, None, 5499.00,  dt(days=7, hours=5)),
        ('EZI-20246', 3,  'Apple Watch Series 9 45mm GPS',     'APL-WS9-45',    'The Courier Guy',   'refunded',           'Good',            76,   3.9,  0, 0, None, 9999.00,  dt(days=7, hours=7)),
        # 10 days ago
        ('EZI-20231', 2,  'Samsung Galaxy A55 5G 256GB',       'SAM-A55-256',   'Aramex',            'refunded',           'Good',            73,   2.7,  0, 0, None, 8999.00,  dt(days=10)),
        ('EZI-20232', 4,  'Dyson Airwrap Complete Styler',     'DYS-AWC-CMPL',  'DHL Express',       'approved',           'Like New',        90,   62.4, 1, 0, 'Return after 24 days; item shows signs of use; change-of-mind claim', 8999.00, dt(days=10, hours=2)),
        ('EZI-20233', 9,  'Makita 18V LXT Combi Drill',        'MAK-DHP481-B',  'PostNet',           'refunded',           'New/Unused',      97,   1.2,  0, 0, None, 3299.00,  dt(days=10, hours=3)),
        ('EZI-20234', 5,  'Nike Pegasus 41 Running Shoes',     'NKE-PEG41-44',  'The Courier Guy',   'refunded',           'Good',            78,   3.3,  0, 0, None, 2499.00,  dt(days=10, hours=4)),
        ('EZI-20235', 13, 'GoPro Hero 12 Black Bundle',        'GPR-H12-BNDL',  'Fastway Couriers',  'refunded',           'Like New',        88,   5.6,  0, 0, None, 7999.00,  dt(days=10, hours=5)),
        ('EZI-20236', 7,  'Xiaomi Smart TV A Pro 55"',         'XMI-TVAP-55',   'DHL Express',       'rejected',           'Damaged/Unusable',20,   88.7, 1, 0, 'Item returned damaged; 5th return in 2 months; fraud pattern confirmed', 9999.00, dt(days=10, hours=6)),
        # 13 days ago
        ('EZI-20221', 14, 'Apple AirPods Max Space Grey',      'APL-APM-SG',    'The Courier Guy',   'refunded',           'Good',            75,   3.8,  0, 0, None, 9999.00,  dt(days=13)),
        ('EZI-20222', 11, 'Lenovo ThinkPad X1 Carbon Gen 12',  'LNV-X1C-G12',   'DHL Express',       'assessed',           'Good',            79,   4.2,  0, 0, None, 31999.00, dt(days=13, hours=2)),
        ('EZI-20223', 1,  'Razer BlackShark V2 Pro Headset',   'RZR-BSV2P-BLK', 'Aramex',            'refunded',           'Like New',        92,   2.6,  0, 0, None, 3499.00,  dt(days=13, hours=3)),
        ('EZI-20224', 6,  'Russell Hobbs Illumina Kettle',     'RH-KT-ILL-BLK', 'PostNet',           'refunded',           'New/Unused',      100,  1.1,  0, 0, None, 899.00,   dt(days=13, hours=5)),
        ('EZI-20225', 15, 'Samsung Galaxy S24+ 256GB',         'SAM-S24P-256',  'The Courier Guy',   'approved',           'Poor',            35,   74.5, 1, 0, 'Screen damage not matching original reported issue; fraud pattern suspected', 19999.00, dt(days=13, hours=7)),
        ('EZI-20226', 8,  'Logitech MX Master 3S Mouse',       'LGT-MXM3S-GRY', 'Fastway Couriers',  'refunded',           'Like New',        94,   1.9,  0, 0, None, 1999.00,  dt(days=13, hours=8)),
        # 16 days ago
        ('EZI-20211', 3,  'Dell XPS 15 9530 Laptop',           'DLL-XPS15-9530','DHL Express',       'in_transit',         'Fair',            58,   6.1,  0, 0, None, 34999.00, dt(days=16)),
        ('EZI-20212', 10, 'Apple MacBook Air M3 13"',          'APL-MBA-M3-13', 'Aramex',            'assessed',           'Good',            80,   3.4,  0, 0, None, 26999.00, dt(days=16, hours=2)),
        ('EZI-20213', 12, 'Nikon Z50 II Mirrorless Camera',    'NKN-Z50-II-KIT','DHL Express',       'approved',           'Like New',        91,   87.6, 1, 0, 'Customer account shows pattern of high-value returns; return rate 75%', 17999.00, dt(days=16, hours=3)),
        ('EZI-20214', 2,  'JBL PartyBox 110 Speaker',          'JBL-PB110-BLK', 'PostNet',           'refunded',           'Good',            70,   4.8,  0, 0, None, 5499.00,  dt(days=16, hours=5)),
        ('EZI-20215', 4,  'Adidas Predator Elite FG Boots',    'ADI-PRED-E-FG', 'Fastway Couriers',  'refunded',           'New/Unused',      99,   65.0, 1, 1, 'Return within 2 hours of delivery; suspicious timing (resolved)', 3999.00, dt(days=16, hours=6)),
        ('EZI-20216', 9,  'Philips Hue Starter Kit E27',       'PHL-HUE-E27-KT','The Courier Guy',   'refunded',           'Like New',        90,   2.4,  0, 0, None, 1899.00,  dt(days=16, hours=8)),
        # 20 days ago
        ('EZI-20201', 13, 'Apple iPad Air 11" M2 Wi-Fi',       'APL-IPA11-M2',  'DHL Express',       'refunded',           'Good',            77,   3.7,  0, 0, None, 14999.00, dt(days=20)),
        ('EZI-20202', 5,  'Canon EOS R50 Camera Kit',          'CNN-EOSR50-KT', 'Aramex',            'refunded',           'Like New',        92,   2.9,  0, 0, None, 11999.00, dt(days=20, hours=2)),
        ('EZI-20203', 14, 'Samsung 32" Odyssey G5 Monitor',    'SAM-OG5-32',    'The Courier Guy',   'assessed',           'Good',            74,   4.3,  0, 0, None, 5999.00,  dt(days=20, hours=4)),
        ('EZI-20204', 15, 'DJI OM 6 Smartphone Gimbal',        'DJI-OM6-PLT',   'PostNet',           'approved',           'Fair',            56,   71.2, 1, 0, 'Third DJI product returned; mismatched serial number on return label', 3499.00, dt(days=20, hours=6)),
        ('EZI-20205', 11, 'Braun Series 9 Pro Shaver',         'BRN-S9PRO-BLK', 'Fastway Couriers',  'refunded',           'Like New',        89,   1.6,  0, 0, None, 4299.00,  dt(days=20, hours=8)),
        ('EZI-20206', 6,  'Tefal ActiFry Genius XL',           'TFL-AFG-XL',    'DHL Express',       'refunded',           'New/Unused',      100,  1.0,  0, 0, None, 3499.00,  dt(days=20, hours=9)),
        # 24 days ago
        ('EZI-20191', 8,  'Apple iPhone 15 128GB Midnight',    'APL-I15-128-MN','The Courier Guy',   'refunded',           'Good',            73,   3.2,  0, 0, None, 17999.00, dt(days=24)),
        ('EZI-20192', 3,  'Samsung 65" Neo QLED 4K TV',        'SAM-QN65-4K',   'DHL Express',       'assessed',           'Good',            76,   5.9,  0, 0, None, 27999.00, dt(days=24, hours=2)),
        ('EZI-20193', 1,  'Jabra Evolve2 85 Headset',          'JAB-EV285-UC',  'Aramex',            'refunded',           'Like New',        93,   2.0,  0, 0, None, 6999.00,  dt(days=24, hours=3)),
        ('EZI-20194', 12, 'Huawei MatePad Pro 12.2"',          'HWI-MPP-12-5G', 'DHL Express',       'approved',           'Fair',            62,   86.4, 1, 0, 'Same address used for 3 different customer accounts; returns fraud ring suspected', 14999.00, dt(days=24, hours=5)),
        ('EZI-20195', 10, 'Mecer Xpress Smartlife 14"',        'MCR-XPS-SL14',  'PostNet',           'refunded',           'New/Unused',      100,  1.4,  0, 0, None, 8999.00,  dt(days=24, hours=7)),
        ('EZI-20196', 2,  'Fitbit Charge 6 Fitness Tracker',   'FIT-CHG6-BLK',  'Fastway Couriers',  'refunded',           'Good',            78,   3.5,  0, 0, None, 2999.00,  dt(days=24, hours=9)),
        # 28 days ago
        ('EZI-20181', 9,  'Sony PlayStation 5 Slim Digital',   'SNY-PS5-SLD',   'DHL Express',       'refunded',           'Good',            75,   4.4,  0, 0, None, 10999.00, dt(days=28)),
        ('EZI-20182', 13, 'Xbox Series X Console',             'MSF-XSXC',      'The Courier Guy',   'refunded',           'Like New',        90,   2.5,  0, 0, None, 11999.00, dt(days=28, hours=2)),
        ('EZI-20183', 4,  'Kensington Thunderbolt 4 Dock',     'KNS-TB4-DK',    'Aramex',            'approved',           'Fair',            58,   63.8, 1, 0, 'Return without original accessories; suspicious damage pattern', 5999.00, dt(days=28, hours=3)),
        ('EZI-20184', 7,  'Samsung Galaxy Z Flip 5 256GB',     'SAM-ZF5-256',   'DHL Express',       'rejected',           'Damaged/Unusable',10,   92.3, 1, 0, 'Intentional damage suspected; non-OEM screen replacement before return', 18999.00, dt(days=28, hours=5)),
        ('EZI-20185', 5,  'Amazfit GTR 4 Smartwatch',          'AMZ-GTR4-BLK',  'PostNet',           'refunded',           'New/Unused',      99,   1.3,  0, 0, None, 3299.00,  dt(days=28, hours=7)),
        # 32 days ago
        ('EZI-20171', 14, 'Huawei Band 9 Smart Wristband',     'HWI-BND9-BLK',  'Fastway Couriers',  'refunded',           'Good',            71,   2.2,  0, 0, None, 1299.00,  dt(days=32)),
        ('EZI-20172', 11, 'Anker MagGo Wireless Charger 3in1', 'ANK-MGG-3N1',   'PostNet',           'refunded',           'Like New',        95,   1.7,  0, 0, None, 1999.00,  dt(days=32, hours=3)),
        ('EZI-20173', 6,  'Nespresso Vertuo Pop Coffee Machine','NSP-VP-RED',    'The Courier Guy',   'refunded',           'New/Unused',      100,  1.0,  0, 0, None, 2799.00,  dt(days=32, hours=5)),
        ('EZI-20174', 15, 'ASUS ROG Strix G16 Gaming Laptop',  'ASS-ROGG16-R9', 'DHL Express',       'approved',           'Poor',            32,   78.9, 1, 0, 'Laptop returned with aftermarket modifications; elevated fraud score', 29999.00, dt(days=32, hours=7)),
        ('EZI-20175', 8,  'Dell Alienware 27" QD-OLED Monitor','DLL-AW2725DF',  'DHL Express',       'assessed',           'Good',            81,   3.8,  0, 0, None, 19999.00, dt(days=32, hours=8)),
    ]

    cur.executemany(
        """INSERT INTO returns
           (order_id,customer_id,product_name,product_sku,carrier,status,condition_label,
            condition_score,fraud_score,is_flagged,fraud_resolved,flag_reason,return_value,created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        R,
    )

    # ── Condition assessments from assessed returns ───────────────────────────
    CMAP = {
        'New/Unused':        (97, '[]',                                                                      'Item appears completely unused. Original packaging intact with all inserts.',              'Resell as New'),
        'Like New':          (91, '["minimal packaging wear"]',                                              'Item shows minimal signs of use. Functionality fully intact.',                           'Resell as New'),
        'Good':              (79, '["light surface scratches","minor wear on grip areas"]',                  'Normal wear consistent with reported use. Core functionality intact.',                   'Restock'),
        'Fair':              (68, '["visible scratches on display","worn button edges","scuff marks"]',      'Moderate cosmetic wear. Item functional but shows clear signs of extended use.',          'Restock'),
        'Poor':              (85, '["cracked housing","missing accessories","significant wear"]',             'Significant damage present. Refurbishment required before resale.',                      'Refurbish'),
        'Damaged/Unusable':  (93, '["broken screen","structural damage","non-OEM components detected"]',     'Severe damage detected. Item unsuitable for resale.',                                    'Dispose'),
    }

    cur.execute("SELECT id, condition_label, created_at FROM returns WHERE condition_label IS NOT NULL")
    for row in cur.fetchall():
        rid, cond, created_at = row
        if cond not in CMAP:
            continue
        conf, dmg, notes, action = CMAP[cond]
        try:
            assessed_at = (datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            assessed_at = dt()
        cur.execute(
            """INSERT INTO condition_assessments
               (return_id,condition_label,confidence,damage_types,ai_notes,action,assessed_at)
               VALUES (?,?,?,?,?,?,?)""",
            (rid, cond, conf, dmg, notes, action, assessed_at),
        )

    # Standalone assessments for the Condition AI page history
    cur.executemany(
        "INSERT INTO condition_assessments (condition_label,confidence,damage_types,ai_notes,action,assessed_at) VALUES (?,?,?,?,?,?)",
        [
            ('Good',     82, '["light scratches on rear panel"]',  'Item shows light use. Screen in excellent condition. All accessories present.', 'Restock',       dt(hours=1)),
            ('Like New', 94, '[]',                                  'Virtually unused. Sealed packaging with minor storage wear only.',               'Resell as New', dt(hours=3)),
            ('Poor',     88, '["cracked screen","missing charger"]','Screen damage present. Missing original charger. Parts replacement required.',  'Refurbish',     dt(hours=5)),
        ],
    )

    conn.commit()
    conn.close()
    print(f"Done. 15 customers, {len(R)} returns seeded.")
    print(f"Location: {DB_PATH}")


if __name__ == '__main__':
    main()
