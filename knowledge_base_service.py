import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict
import uuid

class LocalKnowledgeBaseService:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        # Create or get collection
        self.collection_name = "rag_documents"
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✅ Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(name=self.collection_name)
            print(f"✅ Created new collection: {self.collection_name}")
            # Add some sample documents
            self._add_sample_documents()
    
    def _add_sample_documents(self):
        """Add some sample documents for testing"""
        sample_docs = [
            {
                "id": str(uuid.uuid4()),
                "content": "Quantum computing is a revolutionary technology that leverages quantum mechanical phenomena like superposition and entanglement to process information.",
                "metadata": {"topic": "quantum_computing", "source": "tech_guide"}
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
                "metadata": {"topic": "machine_learning", "source": "ai_guide"}
            }
        ]
        
        # Add documents to collection
        self.collection.add(
            documents=[doc["content"] for doc in sample_docs],
            metadatas=[doc["metadata"] for doc in sample_docs],
            ids=[doc["id"] for doc in sample_docs]
        )
        print(f"✅ Added {len(sample_docs)} sample documents to knowledge base")
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search the knowledge base for relevant documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "id": results['ids'][0][i] if results['ids'] else f"doc_{i}"
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error searching knowledge base: {e}")
            return []
    
    def get_collection_info(self) -> Dict:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "status": "healthy"
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "document_count": 0,
                "status": f"error: {e}"
            }
