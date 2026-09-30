from app.services.rag_service import HybridRAG

if __name__ == "__main__":
    rag = HybridRAG()
    print(f"Loaded {len(rag.chunks)} document chunks from data/docs")
    for c in rag.chunks:
        print(f"{c.id}: {c.title}")
