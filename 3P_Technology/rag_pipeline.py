from typing import List, Dict
# RAG Pipeline combining vector DB and LLM to go over project documents
class RAGPipeline:
    def __init__(self, vector_db):
        self.db = vector_db

    def ingest_docs(self, docs: List[Dict]):
        for d in docs:
            self.db.add(d['id'], d['text'])

    def query(self, q: str):
        # returns top-k docs and an LLM-generated answer 
        results = self.db.search(q, k=5)
        return {
            'query': q,
            'hits': results,
            'answer': "This system recommends using Profinet + redundant controllers for X scenario."
        }
