#!/usr/bin/env python3
"""
Simple RAG System
=================
Einfaches Retrieval-Augmented Generation System mit ChromaDB und Sentence Transformers

Features:
- Intelligente Chunk-Aufteilung
- ChromaDB Vector Store
- Sentence-Transformers für Embeddings
- Similarity Search
- Interaktives Query Interface

Author: SAI3 Project Team
Date: 2025
"""

import os
import re
import numpy as np
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings("ignore")

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    print("✅ Dependencies erfolgreich importiert")
except ImportError as e:
    print(f"❌ Import Fehler: {e}")
    print("Installiere fehlende Dependencies mit:")
    print("pip install chromadb sentence-transformers")
    exit(1)

class SimpleRAGSystem:
    def __init__(self, data_dir="../", collection_name="cyber_security_papers"):
        """
        Initialisiert das Simple RAG-System
        
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
        
        print(f"📚 Simple RAG-System wird initialisiert...")
        print(f"📁 Datenquelle: {self.text_file}")
        print(f"📊 Dateigröße: {os.path.getsize(self.text_file):,} bytes")
        
        # Setup Components
        self.setup_embeddings()
        self.setup_vector_store()
        self.load_and_process_documents()
        
        print("✅ RAG-System erfolgreich initialisiert!")
    
    def setup_embeddings(self):
        """Setup Sentence Transformer für Embeddings"""
        print("🔧 Setup Embedding Model...")
        
        # Lade lokales Sentence Transformer Model
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        print(f"   📦 Lade Model: {model_name}")
        
        self.embedding_model = SentenceTransformer(model_name)
        
        print("✅ Embedding Model geladen")
    
    def setup_vector_store(self):
        """Setup ChromaDB Vector Store"""
        print("🗄️ Setup Vector Store...")
        
        # ChromaDB Client (persistent local storage)
        chroma_client = chromadb.PersistentClient(path="../chroma_db")
        
        # Collection erstellen oder laden
        try:
            self.collection = chroma_client.get_collection(self.collection_name)
            print(f"   📦 Bestehende Collection geladen: {self.collection_name}")
        except:
            self.collection = chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Cybersecurity Papers RAG Collection"}
            )
            print(f"   🆕 Neue Collection erstellt: {self.collection_name}")
        
        print("✅ Vector Store konfiguriert")
    
    def intelligent_text_chunking(self, text: str) -> List[Dict]:
        """
        Intelligente Aufteilung des Textes in semantische Chunks
        
        Args:
            text: Vollständiger Text aus combined_text.txt
            
        Returns:
            List von Dictionaries mit Chunk-Informationen
        """
        print("🧠 Intelligente Text-Segmentierung...")
        
        # Erkenne Paper-Grenzen
        paper_separator = "=" * 50
        papers = text.split(paper_separator)
        
        chunks = []
        chunk_id = 0
        
        for i, paper_text in enumerate(papers):
            if len(paper_text.strip()) < 100:  # Skip sehr kurze Abschnitte
                continue
            
            # Extrahiere Titel
            lines = paper_text.strip().split('\n')
            title = "Unknown Paper"
            
            for line in lines[:5]:
                clean_line = line.strip()
                if len(clean_line) > 10 and not clean_line.startswith('http'):
                    title = clean_line[:100] + "..." if len(clean_line) > 100 else clean_line
                    break
            
            # Teile Paper in kleinere Chunks auf
            sentences = paper_text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) < 512:  # Chunk-Size Limit
                    current_chunk += sentence + ". "
                else:
                    if len(current_chunk.strip()) > 50:  # Mindestlänge
                        chunks.append({
                            "id": f"chunk_{chunk_id}",
                            "text": current_chunk.strip(),
                            "metadata": {
                                "paper_id": f"paper_{i}",
                                "title": title,
                                "source": "combined_text.txt"
                            }
                        })
                        chunk_id += 1
                    
                    current_chunk = sentence + ". "
            
            # Letzter Chunk
            if len(current_chunk.strip()) > 50:
                chunks.append({
                    "id": f"chunk_{chunk_id}",
                    "text": current_chunk.strip(),
                    "metadata": {
                        "paper_id": f"paper_{i}",
                        "title": title,
                        "source": "combined_text.txt"
                    }
                })
                chunk_id += 1
            
            # Progress Update
            if (i + 1) % 10 == 0:
                print(f"   📄 {i + 1} Papers verarbeitet...")
        
        print(f"✅ {len(chunks)} Chunks erstellt")
        return chunks
    
    def load_and_process_documents(self):
        """Lädt und verarbeitet die Textdateien"""
        print("📖 Lade und verarbeite Dokumente...")
        
        # Prüfe ob Collection bereits Daten enthält
        count = self.collection.count()
        if count > 0:
            print(f"   📦 Collection enthält bereits {count} Chunks")
            user_input = input("   ❓ Neu verarbeiten? (y/n): ").strip().lower()
            if user_input != 'y':
                print("   ✅ Verwende bestehende Daten")
                return
            else:
                # Lösche bestehende Daten
                print("   🗑️ Lösche bestehende Daten...")
                self.collection.delete()
        
        # Lade Textdatei
        print("   📚 Lade Textdatei...")
        with open(self.text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"   📊 Textgröße: {len(text_content):,} Zeichen")
        
        # Intelligente Segmentierung
        chunks = self.intelligent_text_chunking(text_content)
        
        # Erstelle Embeddings und speichere in ChromaDB
        print("🔢 Erstelle Embeddings...")
        
        # Batch-Processing für bessere Performance
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            
            # Extrahiere Texte und Metadaten
            texts = [chunk["text"] for chunk in batch]
            ids = [chunk["id"] for chunk in batch]
            metadatas = [chunk["metadata"] for chunk in batch]
            
            # Erstelle Embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Speichere in ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"   📥 Batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1} gespeichert")
        
        print(f"✅ {len(chunks)} Chunks indexiert")
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """
        Stelle eine Frage an das RAG-System
        
        Args:
            question: Die Frage als String
            top_k: Anzahl der ähnlichsten Chunks
            
        Returns:
            Dictionary mit Antwort und Quellen
        """
        print(f"\n🤔 Frage: {question}")
        print("🔍 Suche relevante Informationen...")
        
        # Erstelle Query Embedding
        query_embedding = self.embedding_model.encode([question]).tolist()
        
        # Suche ähnliche Chunks
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # Extrahiere relevante Informationen
        relevant_chunks = []
        for i in range(len(results['documents'][0])):
            relevant_chunks.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'id': results['ids'][0][i]
            })
        
        # Erstelle Antwort basierend auf relevanten Chunks
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
        
        # Simple Antwort-Generierung (ohne LLM)
        answer = self.generate_simple_answer(question, relevant_chunks)
        
        print(f"💡 Gefundene relevante Chunks: {len(relevant_chunks)}")
        
        # Zeige verwendete Quellen
        print("\n📚 Verwendete Quellen:")
        for i, chunk in enumerate(relevant_chunks, 1):
            title = chunk['metadata'].get('title', 'Unknown')
            distance = chunk['distance']
            print(f"   {i}. {title[:50]}... (Similarity: {1-distance:.3f})")
        
        result = {
            'question': question,
            'answer': answer,
            'relevant_chunks': relevant_chunks,
            'context': context
        }
        
        return result
    
    def generate_simple_answer(self, question: str, chunks: List[Dict]) -> str:
        """
        Generiert eine einfache Antwort basierend auf relevanten Chunks
        
        Args:
            question: Die ursprüngliche Frage
            chunks: Liste relevanter Chunks
            
        Returns:
            Einfache Antwort als String
        """
        if not chunks:
            return "Keine relevanten Informationen gefunden."
        
        # Kombiniere die besten Chunks
        best_chunks = chunks[:3]  # Top 3 Chunks
        combined_text = " ".join([chunk['text'] for chunk in best_chunks])
        
        # Einfache Keyword-basierte Antwort-Generierung
        answer_parts = []
        
        # Finde relevante Sätze
        sentences = combined_text.split('. ')
        question_words = set(question.lower().split())
        
        relevant_sentences = []
        for sentence in sentences:
            sentence_words = set(sentence.lower().split())
            overlap = len(question_words.intersection(sentence_words))
            if overlap > 1:  # Mindestens 2 gemeinsame Wörter
                relevant_sentences.append((sentence, overlap))
        
        # Sortiere nach Relevanz
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Erstelle Antwort
        if relevant_sentences:
            answer = "Basierend auf den gefundenen Dokumenten:\n\n"
            for sentence, _ in relevant_sentences[:3]:  # Top 3 Sätze
                answer += f"• {sentence.strip()}.\n"
        else:
            answer = f"Die gefundenen Dokumente enthalten Informationen zu '{question}', aber keine direkten Antworten. Bitte betrachte die angezeigten Quellen für Details."
        
        return answer
    
    def interactive_mode(self):
        """Startet interaktiven Frage-Modus"""
        print("\n" + "="*60)
        print("🎯 INTERAKTIVER RAG-MODUS")
        print("="*60)
        print("Stelle Fragen zu Cybersecurity Papers!")
        print("Kommandos:")
        print("  'quit' oder 'q' - Beenden")
        print("  'stats' - Zeige Statistiken")
        print("  'help' - Zeige Hilfe")
        print()
        
        while True:
            try:
                question = input("❓ Deine Frage: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Auf Wiedersehen!")
                    break
                
                if question.lower() == 'stats':
                    count = self.collection.count()
                    print(f"📊 Collection enthält {count} Chunks")
                    continue
                
                if question.lower() == 'help':
                    print("🔧 Verfügbare Kommandos:")
                    print("  - Stelle direkte Fragen zu Cybersecurity-Themen")
                    print("  - 'stats' für Statistiken")
                    print("  - 'quit' zum Beenden")
                    continue
                
                if not question:
                    continue
                
                # Beantworte Frage
                result = self.query(question)
                print(f"\n💡 Antwort:\n{result['answer']}")
                print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

def main():
    """Hauptfunktion"""
    print("🚀 Simple RAG-System startet...")
    
    try:
        # RAG-System initialisieren
        rag = SimpleRAGSystem()
        
        # Test-Fragen
        test_questions = [
            "Was ist machine learning in cybersecurity?",
            "Wie funktioniert threat detection?",
        ]
        
        print("\n🎯 Teste mit Beispiel-Fragen:")
        for question in test_questions:
            result = rag.query(question)
            print(f"\n💡 Antwort:\n{result['answer']}")
            print("\n" + "-"*50 + "\n")
        
        # Interaktiver Modus
        rag.interactive_mode()
        
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 