-- Ezi Returns Intelligence Platform - Sample Data
-- Realistic South African returns scenario

-- ============================================================
-- CUSTOMERS
-- ============================================================

INSERT INTO customers (name, email, phone, city, total_orders, total_returns, return_rate, risk_score) VALUES
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
('Bongani Zulu',        'bongani.zulu@gmail.com',        '+27 79 678 9012', 'Johannesburg',     6,  4,  0.6667, 79);

-- ============================================================
-- RETURNS  (80 records spread over 35 days)
-- ============================================================

-- --- Recent returns (last 3 days) ---

INSERT INTO returns (order_id, customer_id, product_name, product_sku, carrier, status, condition_label, condition_score, fraud_score, is_flagged, fraud_resolved, flag_reason, return_value, created_at) VALUES
('EZI-20261', 1,  'Samsung Galaxy S24 Ultra 256GB',  'SAM-S24U-256', 'DHL Express',          'pending_assessment', NULL,             NULL, 4.2,  FALSE, FALSE, NULL, 22999.00, NOW() - INTERVAL '2 hours'),
('EZI-20262', 3,  'Apple iPhone 15 Pro Max 256GB',   'APL-I15PM-256','The Courier Guy',      'pending_assessment', NULL,             NULL, 3.8,  FALSE, FALSE, NULL, 27499.00, NOW() - INTERVAL '4 hours'),
('EZI-20263', 6,  'Sony WH-1000XM5 Headphones',      'SNY-WH1000-5', 'Fastway Couriers',     'assessed',           'Good',           78,   5.1,  FALSE, FALSE, NULL, 6999.00,  NOW() - INTERVAL '6 hours'),
('EZI-20264', 12, 'Apple AirPods Pro 2nd Gen',        'APL-APPRO-2',  'DHL Express',          'approved',           'Like New',       92,   88.5, TRUE,  FALSE, 'Return frequency exceeds policy limits (4 returns in 30 days)', 5499.00, NOW() - INTERVAL '8 hours'),
('EZI-20265', 2,  'Nike Air Max 270 Running Shoes',   'NKE-AM270-42', 'Aramex',               'refunded',           'Good',           75,   2.3,  FALSE, FALSE, NULL, 2799.00,  NOW() - INTERVAL '10 hours'),
('EZI-20266', 7,  'iPad Pro 11" M4 Wi-Fi 256GB',      'APL-IPRO11-M4','PostNet',              'pending_assessment', NULL,             NULL, 91.2, TRUE,  FALSE, 'High-value item returned without defect claim; customer shows serial return pattern', 19999.00, NOW() - INTERVAL '12 hours'),
('EZI-20267', 5,  'Dyson V15 Detect Absolute Vacuum', 'DYS-V15-ABS',  'The Courier Guy',     'assessed',           'Like New',       94,   1.8,  FALSE, FALSE, NULL, 12999.00, NOW() - INTERVAL '14 hours'),
('EZI-20268', 11, 'Adidas Ultraboost 23 - Size 10',   'ADI-UB23-10',  'Fastway Couriers',    'refunded',           'Good',           71,   6.2,  FALSE, FALSE, NULL, 3299.00,  NOW() - INTERVAL '16 hours'),
('EZI-20269', 4,  'Nintendo Switch OLED Console',     'NIN-SWOL-WHT', 'The Courier Guy',      'approved',           'Fair',           55,   73.4, TRUE,  FALSE, 'Return after extended use (27 days); customer account flagged', 7499.00, NOW() - INTERVAL '18 hours'),
('EZI-20270', 9,  'Garmin Forerunner 265 Watch',      'GAR-FR265-BLK','DHL Express',          'assessed',           'Good',           80,   3.1,  FALSE, FALSE, NULL, 8999.00,  NOW() - INTERVAL '20 hours'),

-- --- 4 days ago ---

('EZI-20251', 13, 'Samsung Galaxy S24 Ultra 512GB',   'SAM-S24U-512', 'Aramex',               'refunded',           'Like New',       91,   4.5,  FALSE, FALSE, NULL, 24999.00, NOW() - INTERVAL '4 days'),
('EZI-20252', 7,  'LG 55" OLED C3 TV',                'LG-OLED55-C3', 'DHL Express',          'rejected',           'Damaged/Unusable',15, 85.3, TRUE,  FALSE, 'Damage inconsistent with reported fault; serial number mismatch detected', 24999.00, NOW() - INTERVAL '4 days' + INTERVAL '2 hours'),
('EZI-20253', 14, 'JBL Flip 6 Portable Speaker',      'JBL-FLP6-BLK', 'PostNet',              'refunded',           'Good',           77,   2.1,  FALSE, FALSE, NULL, 2999.00,  NOW() - INTERVAL '4 days' + INTERVAL '3 hours'),
('EZI-20254', 10, 'Makita Cordless Drill Set 18V',     'MAK-DDF481-KIT','Fastway Couriers',    'approved',           'Like New',       89,   3.4,  FALSE, FALSE, NULL, 4599.00,  NOW() - INTERVAL '4 days' + INTERVAL '5 hours'),
('EZI-20255', 15, 'Apple iPhone 15 Pro Max 512GB',     'APL-I15PM-512','DHL Express',          'approved',           'Fair',           60,   76.8, TRUE,  FALSE, 'Multiple returns from same address; return value anomaly detected', 30999.00, NOW() - INTERVAL '4 days' + INTERVAL '6 hours'),

-- --- 7 days ago ---

('EZI-20241', 1,  'DJI Mini 4 Pro Drone Combo',       'DJI-M4P-CMBO', 'The Courier Guy',      'refunded',           'Good',           74,   5.2,  FALSE, FALSE, NULL, 18999.00, NOW() - INTERVAL '7 days'),
('EZI-20242', 8,  'Sony WH-1000XM5 Headphones',       'SNY-WH1000-5', 'Aramex',               'refunded',           'New/Unused',     99,   2.8,  FALSE, FALSE, NULL, 6999.00,  NOW() - INTERVAL '7 days' + INTERVAL '1 hour'),
('EZI-20243', 12, 'Samsung Galaxy Tab S9 Ultra',      'SAM-TABS9U',   'DHL Express',          'approved',           'Good',           72,   90.1, TRUE,  FALSE, 'Customer''s 3rd high-value return in 6 weeks; return rate 75%', 21999.00, NOW() - INTERVAL '7 days' + INTERVAL '2 hours'),
('EZI-20244', 6,  'Levi''s 512 Slim Taper Jeans W34', 'LVI-512-3234', 'PostNet',              'refunded',           'New/Unused',     98,   1.5,  FALSE, FALSE, NULL, 1299.00,  NOW() - INTERVAL '7 days' + INTERVAL '4 hours'),
('EZI-20245', 11, 'Bose QuietComfort 45 Headphones',  'BSE-QC45-BLK', 'Fastway Couriers',     'assessed',           'Like New',       93,   4.1,  FALSE, FALSE, NULL, 5499.00,  NOW() - INTERVAL '7 days' + INTERVAL '5 hours'),
('EZI-20246', 3,  'Apple Watch Series 9 45mm GPS',    'APL-WS9-45-GPS','The Courier Guy',     'refunded',           'Good',           76,   3.9,  FALSE, FALSE, NULL, 9999.00,  NOW() - INTERVAL '7 days' + INTERVAL '7 hours'),

-- --- 10 days ago ---

('EZI-20231', 2,  'Samsung Galaxy A55 5G 256GB',      'SAM-A55-256',  'Aramex',               'refunded',           'Good',           73,   2.7,  FALSE, FALSE, NULL, 8999.00,  NOW() - INTERVAL '10 days'),
('EZI-20232', 4,  'Dyson Airwrap Complete Styler',    'DYS-AWC-CMPL', 'DHL Express',          'approved',           'Like New',       90,   62.4, TRUE,  FALSE, 'Return after 24 days; item shows signs of use; change-of-mind claim', 8999.00, NOW() - INTERVAL '10 days' + INTERVAL '2 hours'),
('EZI-20233', 9,  'Makita 18V LXT Combi Drill',       'MAK-DHP481-B', 'PostNet',              'refunded',           'New/Unused',     97,   1.2,  FALSE, FALSE, NULL, 3299.00,  NOW() - INTERVAL '10 days' + INTERVAL '3 hours'),
('EZI-20234', 5,  'Nike Pegasus 41 Running Shoes',    'NKE-PEG41-44', 'The Courier Guy',      'refunded',           'Good',           78,   3.3,  FALSE, FALSE, NULL, 2499.00,  NOW() - INTERVAL '10 days' + INTERVAL '4 hours'),
('EZI-20235', 13, 'GoPro Hero 12 Black Bundle',       'GPR-H12-BNDL', 'Fastway Couriers',     'refunded',           'Like New',       88,   5.6,  FALSE, FALSE, NULL, 7999.00,  NOW() - INTERVAL '10 days' + INTERVAL '5 hours'),
('EZI-20236', 7,  'Xiaomi Smart TV A Pro 55"',        'XMI-TVAP-55',  'DHL Express',          'rejected',           'Damaged/Unusable',20, 88.7, TRUE,  FALSE, 'Item returned damaged; not consistent with reported fault; 5th return in 2 months', 9999.00, NOW() - INTERVAL '10 days' + INTERVAL '6 hours'),

-- --- 13 days ago ---

('EZI-20221', 14, 'Apple AirPods Max Space Grey',     'APL-APM-SG',   'The Courier Guy',      'refunded',           'Good',           75,   3.8,  FALSE, FALSE, NULL, 9999.00,  NOW() - INTERVAL '13 days'),
('EZI-20222', 11, 'Lenovo ThinkPad X1 Carbon Gen 12', 'LNV-X1C-G12',  'DHL Express',          'assessed',           'Good',           79,   4.2,  FALSE, FALSE, NULL, 31999.00, NOW() - INTERVAL '13 days' + INTERVAL '2 hours'),
('EZI-20223', 1,  'Razer BlackShark V2 Pro',          'RZR-BSV2P-BLK','Aramex',               'refunded',           'Like New',       92,   2.6,  FALSE, FALSE, NULL, 3499.00,  NOW() - INTERVAL '13 days' + INTERVAL '3 hours'),
('EZI-20224', 6,  'Russell Hobbs Kettle Illumina',    'RH-KT-ILL-BLK','PostNet',              'refunded',           'New/Unused',     100,  1.1,  FALSE, FALSE, NULL, 899.00,   NOW() - INTERVAL '13 days' + INTERVAL '5 hours'),
('EZI-20225', 15, 'Samsung Galaxy S24+ 256GB',        'SAM-S24P-256', 'The Courier Guy',      'approved',           'Poor',           35,   74.5, TRUE,  FALSE, 'Screen damage not matching original reported issue; fraud pattern suspected', 19999.00, NOW() - INTERVAL '13 days' + INTERVAL '7 hours'),
('EZI-20226', 8,  'Logitech MX Master 3S Mouse',      'LGT-MXM3S-GRY','Fastway Couriers',    'refunded',           'Like New',       94,   1.9,  FALSE, FALSE, NULL, 1999.00,  NOW() - INTERVAL '13 days' + INTERVAL '8 hours'),

-- --- 16 days ago ---

('EZI-20211', 3,  'Dell XPS 15 9530 Laptop',          'DLL-XPS15-9530','DHL Express',         'in_transit',         'Fair',           58,   6.1,  FALSE, FALSE, NULL, 34999.00, NOW() - INTERVAL '16 days'),
('EZI-20212', 10, 'Apple MacBook Air M3 13"',         'APL-MBA-M3-13', 'Aramex',              'assessed',           'Good',           80,   3.4,  FALSE, FALSE, NULL, 26999.00, NOW() - INTERVAL '16 days' + INTERVAL '2 hours'),
('EZI-20213', 12, 'Nikon Z50 II Mirrorless Camera',   'NKN-Z50-II-KIT','DHL Express',         'approved',           'Like New',       91,   87.6, TRUE,  FALSE, 'Customer account shows pattern of high-value returns; return rate 75%', 17999.00, NOW() - INTERVAL '16 days' + INTERVAL '3 hours'),
('EZI-20214', 2,  'JBL PartyBox 110 Speaker',         'JBL-PB110-BLK','PostNet',              'refunded',           'Good',           70,   4.8,  FALSE, FALSE, NULL, 5499.00,  NOW() - INTERVAL '16 days' + INTERVAL '5 hours'),
('EZI-20215', 4,  'Adidas Predator Elite FG Boots',   'ADI-PRED-E-FG', 'Fastway Couriers',   'refunded',           'New/Unused',     99,   65.0, TRUE,  TRUE,  'Return within 2 hours of delivery; suspicious timing (resolved)', 3999.00,  NOW() - INTERVAL '16 days' + INTERVAL '6 hours'),
('EZI-20216', 9,  'Philips Hue Starter Kit E27',      'PHL-HUE-E27-KT','The Courier Guy',    'refunded',           'Like New',       90,   2.4,  FALSE, FALSE, NULL, 1899.00,  NOW() - INTERVAL '16 days' + INTERVAL '8 hours'),

-- --- 20 days ago ---

('EZI-20201', 13, 'Apple iPad Air 11" M2 Wi-Fi',      'APL-IPA11-M2', 'DHL Express',          'refunded',           'Good',           77,   3.7,  FALSE, FALSE, NULL, 14999.00, NOW() - INTERVAL '20 days'),
('EZI-20202', 5,  'Canon EOS R50 Camera Kit',         'CNN-EOSR50-KT','Aramex',               'refunded',           'Like New',       92,   2.9,  FALSE, FALSE, NULL, 11999.00, NOW() - INTERVAL '20 days' + INTERVAL '2 hours'),
('EZI-20203', 14, 'Samsung 32" Odyssey G5 Monitor',   'SAM-OG5-32',   'The Courier Guy',      'assessed',           'Good',           74,   4.3,  FALSE, FALSE, NULL, 5999.00,  NOW() - INTERVAL '20 days' + INTERVAL '4 hours'),
('EZI-20204', 15, 'DJI OM 6 Smartphone Gimbal',       'DJI-OM6-PLT',  'PostNet',              'approved',           'Fair',           56,   71.2, TRUE,  FALSE, 'Third DJI product returned; mismatched serial number on return label', 3499.00,  NOW() - INTERVAL '20 days' + INTERVAL '6 hours'),
('EZI-20205', 11, 'Braun Series 9 Pro Shaver',        'BRN-S9PRO-BLK','Fastway Couriers',    'refunded',           'Like New',       89,   1.6,  FALSE, FALSE, NULL, 4299.00,  NOW() - INTERVAL '20 days' + INTERVAL '8 hours'),
('EZI-20206', 6,  'Tefal ActiFry Genius XL',          'TFL-AFG-XL',   'DHL Express',          'refunded',           'New/Unused',     100,  1.0,  FALSE, FALSE, NULL, 3499.00,  NOW() - INTERVAL '20 days' + INTERVAL '9 hours'),

-- --- 24 days ago ---

('EZI-20191', 8,  'Apple iPhone 15 128GB Midnight',   'APL-I15-128-MN','The Courier Guy',     'refunded',           'Good',           73,   3.2,  FALSE, FALSE, NULL, 17999.00, NOW() - INTERVAL '24 days'),
('EZI-20192', 3,  'Samsung 65" Neo QLED 4K TV',       'SAM-QN65-4K',  'DHL Express',          'assessed',           'Good',           76,   5.9,  FALSE, FALSE, NULL, 27999.00, NOW() - INTERVAL '24 days' + INTERVAL '2 hours'),
('EZI-20193', 1,  'Jabra Evolve2 85 Headset',         'JAB-EV285-UC', 'Aramex',               'refunded',           'Like New',       93,   2.0,  FALSE, FALSE, NULL, 6999.00,  NOW() - INTERVAL '24 days' + INTERVAL '3 hours'),
('EZI-20194', 12, 'Huawei MatePad Pro 12.2"',         'HWI-MPP-12-5G','DHL Express',          'approved',           'Fair',           62,   86.4, TRUE,  FALSE, 'Same address used for 3 different customer accounts; returns fraud ring suspected', 14999.00, NOW() - INTERVAL '24 days' + INTERVAL '5 hours'),
('EZI-20195', 10, 'Mecer Xpress Smartlife 14"',       'MCR-XPS-SL14', 'PostNet',              'refunded',           'New/Unused',     100,  1.4,  FALSE, FALSE, NULL, 8999.00,  NOW() - INTERVAL '24 days' + INTERVAL '7 hours'),
('EZI-20196', 2,  'Fitbit Charge 6 Fitness Tracker',  'FIT-CHG6-BLK', 'Fastway Couriers',     'refunded',           'Good',           78,   3.5,  FALSE, FALSE, NULL, 2999.00,  NOW() - INTERVAL '24 days' + INTERVAL '9 hours'),

-- --- 28 days ago ---

('EZI-20181', 9,  'Sony PlayStation 5 Slim Digital',  'SNY-PS5-SLD',  'DHL Express',          'refunded',           'Good',           75,   4.4,  FALSE, FALSE, NULL, 10999.00, NOW() - INTERVAL '28 days'),
('EZI-20182', 13, 'Xbox Series X Console',            'MSF-XSXC',     'The Courier Guy',      'refunded',           'Like New',       90,   2.5,  FALSE, FALSE, NULL, 11999.00, NOW() - INTERVAL '28 days' + INTERVAL '2 hours'),
('EZI-20183', 4,  'Kensington Thunderbolt 4 Dock',    'KNS-TB4-DK',   'Aramex',               'approved',           'Fair',           58,   63.8, TRUE,  FALSE, 'Return without original accessories; suspicious damage pattern (partially resolved)', 5999.00, NOW() - INTERVAL '28 days' + INTERVAL '3 hours'),
('EZI-20184', 7,  'Samsung Galaxy Z Flip 5 256GB',    'SAM-ZF5-256',  'DHL Express',          'rejected',           'Damaged/Unusable',10, 92.3, TRUE,  FALSE, 'Intentional damage suspected; screen replaced with non-OEM screen before return', 18999.00, NOW() - INTERVAL '28 days' + INTERVAL '5 hours'),
('EZI-20185', 5,  'Amazfit GTR 4 Smartwatch',         'AMZ-GTR4-BLK', 'PostNet',              'refunded',           'New/Unused',     99,   1.3,  FALSE, FALSE, NULL, 3299.00,  NOW() - INTERVAL '28 days' + INTERVAL '7 hours'),

-- --- 32 days ago ---

('EZI-20171', 14, 'Huawei Band 9 Smart Wristband',    'HWI-BND9-BLK', 'Fastway Couriers',     'refunded',           'Good',           71,   2.2,  FALSE, FALSE, NULL, 1299.00,  NOW() - INTERVAL '32 days'),
('EZI-20172', 11, 'Anker MagGo Wireless Charger 3in1','ANK-MGG-3N1',  'PostNet',              'refunded',           'Like New',       95,   1.7,  FALSE, FALSE, NULL, 1999.00,  NOW() - INTERVAL '32 days' + INTERVAL '3 hours'),
('EZI-20173', 6,  'Nespresso Vertuo Pop Coffee Machine','NSP-VP-RED',  'The Courier Guy',     'refunded',           'New/Unused',     100,  1.0,  FALSE, FALSE, NULL, 2799.00,  NOW() - INTERVAL '32 days' + INTERVAL '5 hours'),
('EZI-20174', 15, 'ASUS ROG Strix G16 Gaming Laptop', 'ASS-ROGG16-R9','DHL Express',          'approved',           'Poor',           32,   78.9, TRUE,  FALSE, 'Laptop returned with aftermarket modifications; fraud score elevated by account history', 29999.00, NOW() - INTERVAL '32 days' + INTERVAL '7 hours'),
('EZI-20175', 8,  'Dell Alienware 27" QD-OLED Monitor','DLL-AW2725DF', 'DHL Express',         'assessed',           'Good',           81,   3.8,  FALSE, FALSE, NULL, 19999.00, NOW() - INTERVAL '32 days' + INTERVAL '8 hours');

-- ============================================================
-- CONDITION ASSESSMENTS (from existing returns data)
-- ============================================================

INSERT INTO condition_assessments (return_id, condition_label, confidence, damage_types, ai_notes, action, assessed_at)
SELECT r.id, r.condition_label,
    CASE r.condition_label
        WHEN 'New/Unused'        THEN 97
        WHEN 'Like New'          THEN 91
        WHEN 'Good'              THEN 79
        WHEN 'Fair'              THEN 68
        WHEN 'Poor'              THEN 85
        WHEN 'Damaged/Unusable'  THEN 93
        ELSE 75
    END,
    CASE r.condition_label
        WHEN 'New/Unused'       THEN '[]'::jsonb
        WHEN 'Like New'         THEN '["minimal packaging wear"]'::jsonb
        WHEN 'Good'             THEN '["light surface scratches", "minor wear on grip areas"]'::jsonb
        WHEN 'Fair'             THEN '["visible scratches on display", "worn button edges", "scuff marks on body"]'::jsonb
        WHEN 'Poor'             THEN '["cracked housing", "missing accessories", "significant wear", "deep scratches"]'::jsonb
        WHEN 'Damaged/Unusable' THEN '["broken screen", "structural damage", "non-OEM components detected", "water damage indicators"]'::jsonb
        ELSE '[]'::jsonb
    END,
    CASE r.condition_label
        WHEN 'New/Unused'       THEN 'Item appears completely unused. Original packaging intact with all inserts. No signs of use detected.'
        WHEN 'Like New'         THEN 'Item shows minimal signs of use. Functionality fully intact. Original accessories present.'
        WHEN 'Good'             THEN 'Normal wear consistent with reported use. Core functionality intact. Minor cosmetic marks present.'
        WHEN 'Fair'             THEN 'Moderate cosmetic wear. Item functional but shows clear signs of extended use. Reduced resale value.'
        WHEN 'Poor'             THEN 'Significant cosmetic and potential functional damage. Refurbishment required before resale.'
        WHEN 'Damaged/Unusable' THEN 'Severe damage detected. Item unsuitable for resale. Recommend disposal or parts salvage.'
        ELSE 'Assessment completed. Review recommended.'
    END,
    CASE r.condition_label
        WHEN 'New/Unused'       THEN 'Resell as New'
        WHEN 'Like New'         THEN 'Resell as New'
        WHEN 'Good'             THEN 'Restock'
        WHEN 'Fair'             THEN 'Restock'
        WHEN 'Poor'             THEN 'Refurbish'
        WHEN 'Damaged/Unusable' THEN 'Dispose'
        ELSE 'Restock'
    END,
    r.created_at + INTERVAL '3 hours'
FROM returns r
WHERE r.condition_label IS NOT NULL;

-- Seed a few standalone assessments for the condition page history
INSERT INTO condition_assessments (condition_label, confidence, damage_types, ai_notes, action, assessed_at) VALUES
('Good',           82, '["light scratches on rear panel"]', 'Item shows light use. Screen in excellent condition. All accessories present.', 'Restock', NOW() - INTERVAL '1 hour'),
('Like New',       94, '[]',                                'Virtually unused. Sealed packaging shows minor storage wear only.', 'Resell as New', NOW() - INTERVAL '3 hours'),
('Poor',           88, '["cracked screen", "missing charger"]', 'Screen damage present. Missing original charger. Requires parts replacement before resale.', 'Refurbish', NOW() - INTERVAL '5 hours');
