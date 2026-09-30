from app.config import settings

class GraphService:
    def query(self, question: str):
        try:
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password))
            cypher = """
            MATCH (p:Product)-[:HAS_TICKET]->(t:Ticket)
            RETURN p.name AS product, count(t) AS tickets
            ORDER BY tickets DESC LIMIT 5
            """
            with driver.session() as session:
                result = [dict(r) for r in session.run(cypher)]
            driver.close()
            return result
        except Exception:
            return []
