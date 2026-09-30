CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY,
  quarter TEXT NOT NULL,
  region TEXT NOT NULL,
  product TEXT NOT NULL,
  revenue NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS support_tickets (
  id INTEGER PRIMARY KEY,
  product TEXT NOT NULL,
  priority TEXT NOT NULL,
  created_at DATE NOT NULL
);

INSERT INTO sales (id, quarter, region, product, revenue) VALUES
(1,'Q3','Europe','Atlas Analytics',180000),
(2,'Q3','Europe','NovaDesk',145000),
(3,'Q3','Europe','Orbit CRM',210000),
(4,'Q3','North America','Atlas Analytics',310000),
(5,'Q3','North America','NovaDesk',280000),
(6,'Q3','North America','Orbit CRM',390000),
(7,'Q3','APAC','Atlas Analytics',120000),
(8,'Q3','APAC','NovaDesk',95000),
(9,'Q3','APAC','Orbit CRM',160000),
(10,'Q2','Europe','Atlas Analytics',220000),
(11,'Q2','Europe','NovaDesk',190000),
(12,'Q2','Europe','Orbit CRM',205000)
ON CONFLICT DO NOTHING;

INSERT INTO support_tickets (id, product, priority, created_at) VALUES
(1,'Atlas Analytics','high','2026-07-01'),
(2,'Atlas Analytics','high','2026-07-03'),
(3,'Atlas Analytics','medium','2026-07-10'),
(4,'NovaDesk','high','2026-07-02'),
(5,'NovaDesk','medium','2026-07-08'),
(6,'Orbit CRM','low','2026-07-12'),
(7,'NovaDesk','high','2026-07-15')
ON CONFLICT DO NOTHING;
