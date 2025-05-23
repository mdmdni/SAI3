"""
RAG System Setup with LlamaIndex
================================
Intelligent Document Processing and Retrieval-Augmented Generation

Features:
- Intelligente Chunk-Aufteilung respektiert Paper-Grenzen  
- ChromaDB als Vector Store
- Sentence-Transformers für lokale Embeddings
- LlamaIndex für RAG-Pipeline
- Interaktives Query-Interface

Author: SAI3 Project Team
Date: 2025
"""

import os
import re
import chromadb
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import warnings
warnings.filterwarnings("ignore")

class RAGSystem:
    def __init__(self, data_dir="../", collection_name="cyber_security_papers"):
        """
        Initialisiert das RAG-System
        
        Args:
            data_dir: Verzeichnis mit combined_text.txt
            collection_name: Name der ChromaDB Collection
        """
        self.data_dir = data_dir
        self.collection_name = collection_name
        self.text_file = os.path.join(data_dir, "combined_text.txt")
        
        # Überprüfe ob Textdatei existiert
        if not os.path.exists(self.text_file):
            raise FileNotFoundError(f"Datei nicht gefunden: {self.text_file}")
        
        print(f"📚 RAG-System wird initialisiert...")
        print(f"📁 Datenquelle: {self.text_file}")
        
        # Setup Embeddings (lokal, ohne API-Keys)
        self.setup_embeddings()
        
        # Setup Vector Store
        self.setup_vector_store()
        
        # Lade und verarbeite Dokumente
        self.load_and_process_documents()
        
        # Erstelle Index
        self.create_index()
        
        print("✅ RAG-System erfolgreich initialisiert!")
    
    def setup_embeddings(self):
        """Setup lokale Sentence Transformer Embeddings"""
        print("🔧 Setup Embeddings...")
        
        # Verwende lokales Embedding-Modell (kein OpenAI API-Key nötig)
        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Setze globale Settings für LlamaIndex
        Settings.embed_model = embed_model
        
        # Chunk-Size für bessere Performance
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        
        print("✅ Embeddings konfiguriert")
    
    def setup_vector_store(self):
        """Setup ChromaDB Vector Store"""
        print("🗄️ Setup Vector Store...")
        
        # ChromaDB Client (persistent local storage)
        chroma_client = chromadb.PersistentClient(path="../chroma_db")
        
        # Collection erstellen oder laden
        chroma_collection = chroma_client.get_or_create_collection(self.collection_name)
        
        # Vector Store wrapper für LlamaIndex
        self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        
        print("✅ Vector Store konfiguriert")
    
    def intelligent_text_chunking(self, text):
        """
        Intelligente Aufteilung des Textes respektiert Paper-Grenzen
        
        Args:
            text: Vollständiger Text aus combined_text.txt
            
        Returns:
            List von Document-Objekten mit Metadaten
        """
        print("🧠 Intelligente Text-Segmentierung...")
        
        # Erkenne Paper-Grenzen basierend auf Mustern
        paper_separator = "=" * 50
        papers = text.split(paper_separator)
        
        documents = []
        paper_count = 0
        
        for i, paper_text in enumerate(papers):
            if len(paper_text.strip()) < 100:  # Skip sehr kurze Abschnitte
                continue
                
            paper_count += 1
            
            # Extrahiere Titel (erste Zeile nach Bereinigung)
            lines = paper_text.strip().split('\n')
            title = "Unknown Paper"
            
            for line in lines[:5]:  # Suche in ersten 5 Zeilen nach Titel
                clean_line = line.strip()
                if len(clean_line) > 10 and not clean_line.startswith('http'):
                    title = clean_line[:100] + "..." if len(clean_line) > 100 else clean_line
                    break
            
            # Erstelle Document mit Metadaten
            doc = Document(
                text=paper_text.strip(),
                metadata={
                    "source": "combined_text.txt",
                    "paper_id": f"paper_{paper_count}",
                    "title": title,
                    "chunk_type": "full_paper"
                }
            )
            
            documents.append(doc)
            
            # Status-Update
            if paper_count % 10 == 0:
                print(f"   📄 {paper_count} Papers verarbeitet...")
        
        print(f"✅ {len(documents)} Dokumente erstellt")
        return documents
    
    def load_and_process_documents(self):
        """Lädt und verarbeitet die Textdateien"""
        print("📖 Lade und verarbeite Dokumente...")
        
        # Lade Textdatei
        with open(self.text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"📊 Textgröße: {len(text_content):,} Zeichen")
        
        # Intelligente Segmentierung
        self.documents = self.intelligent_text_chunking(text_content)
        
        # Weitere Aufteilung in kleinere Chunks für bessere Retrieval-Performance
        node_parser = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separator=" "
        )
        
        print("🔄 Erstelle feinere Chunks...")
        self.nodes = node_parser.get_nodes_from_documents(self.documents)
        
        print(f"✅ {len(self.nodes)} Chunks erstellt")
    
    def create_index(self):
        """Erstellt den Vector Store Index"""
        print("🔍 Erstelle Vector Store Index...")
        
        # Storage Context mit ChromaDB
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        
        # Erstelle Index
        self.index = VectorStoreIndex(
            self.nodes,
            storage_context=storage_context,
            show_progress=True
        )
        
        # Query Engine für Retrieval
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=5,  # Top 5 ähnlichste Chunks
            response_mode="tree_summarize"  # Intelligente Antwort-Synthese
        )
        
        print("✅ Index erstellt und Query Engine bereit")
    
    def query(self, question):
        """
        Stelle eine Frage an das RAG-System
        
        Args:
            question: Die Frage als String
            
        Returns:
            Antwort des RAG-Systems
        """
        print(f"\n🤔 Frage: {question}")
        print("🔍 Suche relevante Informationen...")
        
        response = self.query_engine.query(question)
        
        print(f"💡 Antwort: {response.response}")
        
        # Zeige verwendete Quellen
        if hasattr(response, 'source_nodes') and response.source_nodes:
            print("\n📚 Verwendete Quellen:")
            for i, node in enumerate(response.source_nodes, 1):
                title = node.metadata.get('title', 'Unknown')
                score = node.score if hasattr(node, 'score') else 'N/A'
                print(f"   {i}. {title[:50]}... (Score: {score})")
        
        return response
    
    def interactive_mode(self):
        """Startet interaktiven Frage-Modus"""
        print("\n" + "="*60)
        print("🎯 INTERAKTIVER RAG-MODUS")
        print("="*60)
        print("Stelle Fragen zu Cybersecurity Papers!")
        print("Eingabe 'quit' zum Beenden\n")
        
        while True:
            try:
                question = input("❓ Deine Frage: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Auf Wiedersehen!")
                    break
                
                if not question:
                    continue
                
                # Beantworte Frage
                response = self.query(question)
                print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

def main():
    """Hauptfunktion"""
    print("🚀 RAG-System mit LlamaIndex startet...")
    
    try:
        # RAG-System initialisieren
        rag = RAGSystem()
        
        # Beispiel-Fragen
        example_questions = [
            "Was sind die wichtigsten Cybersecurity-Bedrohungen?",
            "Wie funktioniert Machine Learning in der Cybersecurity?",
            "Was ist Zero-Day-Exploitation?",
            "Welche Rolle spielt KI bei der Bedrohungserkennung?"
        ]
        
        print("\n🎯 Teste mit Beispiel-Fragen:")
        for question in example_questions[:2]:  # Teste ersten 2 Fragen
            rag.query(question)
            print("\n" + "-"*50 + "\n")
        
        # Interaktiver Modus
        rag.interactive_mode()
        
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")

if __name__ == "__main__":
    main() 