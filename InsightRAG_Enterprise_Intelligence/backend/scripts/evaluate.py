import json
from pathlib import Path
from app.services.rag_service import HybridRAG

ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT / "data" / "eval_questions.json").read_text())
rag = HybridRAG()

hits = 0
for item in items:
    results = rag.search(item["question"], top_k=3)
    ids = [r["id"] for r in results]
    expected = item.get("expected_doc")
    hit = any(expected in x for x in ids) if expected else True
    hits += int(hit)
    print(f"{'PASS' if hit else 'MISS'} | {item['question']} | {ids}")

print(f"\nRetrieval hit rate: {hits/len(items):.2%}")
