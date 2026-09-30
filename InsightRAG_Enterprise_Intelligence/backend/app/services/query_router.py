import re

SQL_HINTS = [
    r"revenue", r"sales", r"orders", r"customers", r"margin", r"growth",
    r"quarter", r"q[1-4]", r"month", r"top \d+", r"decline", r"increase",
    r"highest", r"lowest", r"average", r"count"
]
DOC_HINTS = [r"policy", r"manual", r"document", r"annual report", r"refund", r"guideline", r"terms", r"summari[sz]e"]
GRAPH_HINTS = [r"related", r"connected", r"associated", r"customers.*products", r"dependency", r"relationship"]


def route_query(question: str) -> str:
    q = question.lower()
    if any(re.search(p, q) for p in GRAPH_HINTS):
        return "hybrid_graph"
    sql = any(re.search(p, q) for p in SQL_HINTS)
    doc = any(re.search(p, q) for p in DOC_HINTS)
    if sql and doc:
        return "hybrid"
    if sql:
        return "sql"
    return "document"
