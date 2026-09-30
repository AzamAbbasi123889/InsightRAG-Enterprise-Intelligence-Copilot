from sqlalchemy import text
from app.database import SessionLocal

SQL_TEMPLATES = {
    "europe_revenue": """
        SELECT region, SUM(revenue) AS revenue
        FROM sales
        WHERE quarter = :quarter AND region = 'Europe'
        GROUP BY region
    """,
    "top_products_q3": """
        SELECT product, SUM(revenue) AS revenue
        FROM sales
        WHERE quarter = 'Q3'
        GROUP BY product ORDER BY revenue DESC LIMIT 5
    """,
    "regional_revenue": """
        SELECT region, SUM(revenue) AS revenue
        FROM sales WHERE quarter = :quarter
        GROUP BY region ORDER BY revenue DESC
    """,
    "support_by_product": """
        SELECT product, COUNT(*) AS tickets
        FROM support_tickets GROUP BY product ORDER BY tickets DESC LIMIT 10
    """,
}


def _run(sql: str, params: dict | None = None):
    with SessionLocal() as db:
        rows = db.execute(text(sql), params or {}).mappings().all()
        return [dict(r) for r in rows]


def answer_sql(question: str):
    q = question.lower()
    if "top" in q and "product" in q and "q3" in q:
        rows = _run(SQL_TEMPLATES["top_products_q3"])
        return rows, "Top products by Q3 revenue were computed directly from the sales table."
    if "europe" in q and "revenue" in q and "q3" in q:
        rows = _run(SQL_TEMPLATES["europe_revenue"], {"quarter": "Q3"})
        return rows, "Europe Q3 revenue was computed from the sales table."
    if "support" in q or "ticket" in q:
        rows = _run(SQL_TEMPLATES["support_by_product"])
        return rows, "Support volume was computed from the support_tickets table."
    rows = _run(SQL_TEMPLATES["regional_revenue"], {"quarter": "Q3"})
    return rows, "Regional Q3 revenue was computed from the sales table."
