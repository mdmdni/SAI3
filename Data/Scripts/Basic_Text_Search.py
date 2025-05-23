#!/usr/bin/env python3
"""
Basic Text Search System
========================
Demonstriert RAG-Konzepte mit einfachen Python-Libraries

Features:
- Intelligente Text-Segmentierung
- TF-IDF basierte Suche
- Keyword-Matching
- Interaktives Interface

Zeigt die Grundprinzipien von RAG ohne komplexe Dependencies.

Author: SAI3 Project Team
Date: 2025
"""

import os
import re
import math
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import json

class BasicRAGSystem:
    def __init__(self, data_dir="../"):
        """
        Initialisiert das Basic RAG-System
        
        Args:
            data_dir: Verzeichnis mit combined_text.txt
        """
        self.data_dir = data_dir
        self.text_file = os.path.join(data_dir, "combined_text.txt")
        self.index_file = os.path.join(data_dir, "text_index.json")
        
        # Überprüfe ob Textdatei existiert
        if not os.path.exists(self.text_file):
            raise FileNotFoundError(f"Datei nicht gefunden: {self.text_file}")
        
        print(f"📚 Basic RAG-System wird initialisiert...")
        print(f"📁 Datenquelle: {self.text_file}")
        print(f"📊 Dateigröße: {os.path.getsize(self.text_file):,} bytes")
        
        # System-Komponenten
        self.chunks = []
        self.word_index = defaultdict(set)  # Wort -> Set von Chunk-IDs
        self.tf_idf_scores = {}
        
        # Lade oder erstelle Index
        self.load_or_create_index()
        
        print("✅ RAG-System erfolgreich initialisiert!")
    
    def load_or_create_index(self):
        """Lädt bestehenden Index oder erstellt einen neuen"""
        if os.path.exists(self.index_file):
            print("📦 Lade bestehenden Index...")
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.chunks = data['chunks']
                    self.word_index = {k: set(v) for k, v in data['word_index'].items()}
                    self.tf_idf_scores = data['tf_idf_scores']
                print(f"✅ Index geladen: {len(self.chunks)} Chunks")
                return
            except:
                print("⚠️ Index beschädigt, erstelle neuen...")
        
        # Erstelle neuen Index
        self.create_index()
    
    def create_index(self):
        """Erstellt einen neuen Text-Index"""
        print("🔧 Erstelle neuen Index...")
        
        # Lade Textdatei
        with open(self.text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"📖 Textgröße: {len(text_content):,} Zeichen")
        
        # Segmentierung
        self.chunks = self.intelligent_chunking(text_content)
        
        # Erstelle Wort-Index
        print("🔍 Erstelle Suchindex...")
        self.build_word_index()
        
        # Berechne TF-IDF Scores
        print("📊 Berechne TF-IDF Scores...")
        self.calculate_tf_idf()
        
        # Speichere Index
        self.save_index()
        
        print("✅ Index erstellt und gespeichert")
    
    def intelligent_chunking(self, text: str) -> List[Dict]:
        """
        Intelligente Aufteilung des Textes
        
        Args:
            text: Vollständiger Text
            
        Returns:
            Liste von Chunk-Dictionaries
        """
        print("🧠 Intelligente Text-Segmentierung...")
        
        # Erkenne Paper-Grenzen
        paper_separator = "=" * 50
        papers = text.split(paper_separator)
        
        chunks = []
        chunk_id = 0
        
        for i, paper_text in enumerate(papers):
            if len(paper_text.strip()) < 100:
                continue
            
            # Extrahiere Titel
            lines = paper_text.strip().split('\n')
            title = "Unknown Paper"
            
            for line in lines[:5]:
                clean_line = line.strip()
                if len(clean_line) > 10 and not clean_line.startswith('http'):
                    title = clean_line[:100] + "..." if len(clean_line) > 100 else clean_line
                    break
            
            # Teile Paper in Chunks auf
            sentences = re.split(r'[.!?]+', paper_text)
            current_chunk = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                if len(current_chunk + sentence) < 800:  # Chunk-Size
                    current_chunk += sentence + ". "
                else:
                    if len(current_chunk.strip()) > 100:
                        chunks.append({
                            "id": chunk_id,
                            "text": current_chunk.strip(),
                            "title": title,
                            "paper_id": f"paper_{i}",
                            "source": "combined_text.txt"
                        })
                        chunk_id += 1
                    
                    current_chunk = sentence + ". "
            
            # Letzter Chunk
            if len(current_chunk.strip()) > 100:
                chunks.append({
                    "id": chunk_id,
                    "text": current_chunk.strip(),
                    "title": title,
                    "paper_id": f"paper_{i}",
                    "source": "combined_text.txt"
                })
                chunk_id += 1
            
            if (i + 1) % 20 == 0:
                print(f"   📄 {i + 1} Papers verarbeitet...")
        
        print(f"✅ {len(chunks)} Chunks erstellt")
        return chunks
    
    def clean_word(self, word: str) -> str:
        """Bereinigt ein Wort für die Indexierung"""
        # Entferne Sonderzeichen und konvertiere zu lowercase
        word = re.sub(r'[^\w\s]', '', word.lower())
        return word.strip()
    
    def build_word_index(self):
        """Erstellt den Wort-zu-Chunk Index"""
        self.word_index.clear()
        
        for chunk in self.chunks:
            chunk_id = chunk['id']
            words = chunk['text'].split()
            
            for word in words:
                clean_word = self.clean_word(word)
                if len(clean_word) > 2:  # Ignoriere sehr kurze Wörter
                    self.word_index[clean_word].add(chunk_id)
    
    def calculate_tf_idf(self):
        """Berechnet TF-IDF Scores für alle Chunks"""
        self.tf_idf_scores.clear()
        
        # Document frequency für jedes Wort
        df = defaultdict(int)
        for word, chunk_ids in self.word_index.items():
            df[word] = len(chunk_ids)
        
        total_docs = len(self.chunks)
        
        # TF-IDF für jeden Chunk
        for chunk in self.chunks:
            chunk_id = chunk['id']
            words = [self.clean_word(w) for w in chunk['text'].split()]
            word_count = len(words)
            
            if word_count == 0:
                continue
            
            # Term frequency
            tf = Counter(words)
            
            # TF-IDF für jedes Wort im Chunk
            chunk_scores = {}
            for word, count in tf.items():
                if len(word) > 2 and word in df:
                    tf_score = count / word_count
                    idf_score = math.log(total_docs / df[word])
                    chunk_scores[word] = tf_score * idf_score
            
            self.tf_idf_scores[chunk_id] = chunk_scores
    
    def save_index(self):
        """Speichert den Index in eine JSON-Datei"""
        try:
            # Konvertiere sets zu lists für JSON
            word_index_serializable = {k: list(v) for k, v in self.word_index.items()}
            
            data = {
                'chunks': self.chunks,
                'word_index': word_index_serializable,
                'tf_idf_scores': self.tf_idf_scores
            }
            
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern des Index: {e}")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Sucht relevante Chunks für eine Query
        
        Args:
            query: Suchquery
            top_k: Anzahl der Ergebnisse
            
        Returns:
            Liste von (chunk, score) Tupeln
        """
        query_words = [self.clean_word(w) for w in query.split()]
        query_words = [w for w in query_words if len(w) > 2]
        
        if not query_words:
            return []
        
        # Relevanz-Scores für alle Chunks
        chunk_scores = defaultdict(float)
        
        for word in query_words:
            if word in self.word_index:
                # Chunks die dieses Wort enthalten
                for chunk_id in self.word_index[word]:
                    if chunk_id in self.tf_idf_scores and word in self.tf_idf_scores[chunk_id]:
                        chunk_scores[chunk_id] += self.tf_idf_scores[chunk_id][word]
        
        # Sortiere nach Score
        sorted_chunks = sorted(chunk_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Hole top_k Chunks
        results = []
        for chunk_id, score in sorted_chunks[:top_k]:
            chunk = next(c for c in self.chunks if c['id'] == chunk_id)
            results.append((chunk, score))
        
        return results
    
    def query(self, question: str) -> Dict:
        """
        Beantwortet eine Frage mit dem RAG-System
        
        Args:
            question: Die Frage
            
        Returns:
            Dictionary mit Antwort und Quellen
        """
        print(f"\n🤔 Frage: {question}")
        print("🔍 Suche relevante Informationen...")
        
        # Suche relevante Chunks
        results = self.search(question, top_k=5)
        
        if not results:
            return {
                'question': question,
                'answer': "Keine relevanten Informationen gefunden.",
                'sources': []
            }
        
        print(f"💡 Gefundene relevante Chunks: {len(results)}")
        
        # Zeige Quellen
        print("\n📚 Relevante Quellen:")
        sources = []
        for i, (chunk, score) in enumerate(results, 1):
            title = chunk['title'][:50] + "..." if len(chunk['title']) > 50 else chunk['title']
            print(f"   {i}. {title} (Score: {score:.3f})")
            sources.append({
                'title': chunk['title'],
                'text': chunk['text'],
                'score': score
            })
        
        # Einfache Antwort-Generierung
        answer = self.generate_answer(question, results)
        
        return {
            'question': question,
            'answer': answer,
            'sources': sources
        }
    
    def generate_answer(self, question: str, results: List[Tuple[Dict, float]]) -> str:
        """
        Generiert eine Antwort basierend auf gefundenen Chunks
        
        Args:
            question: Die ursprüngliche Frage
            results: Liste von (chunk, score) Tupeln
            
        Returns:
            Generierte Antwort
        """
        if not results:
            return "Keine relevanten Informationen gefunden."
        
        # Kombiniere die besten Chunks
        top_chunks = [chunk for chunk, score in results[:3]]
        combined_text = " ".join([chunk['text'] for chunk in top_chunks])
        
        # Finde relevante Sätze
        question_words = set(self.clean_word(w) for w in question.split())
        sentences = re.split(r'[.!?]+', combined_text)
        
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            sentence_words = set(self.clean_word(w) for w in sentence.split())
            overlap = len(question_words.intersection(sentence_words))
            
            if overlap >= 1:  # Mindestens 1 gemeinsames Wort
                relevant_sentences.append((sentence, overlap))
        
        # Sortiere nach Relevanz
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Erstelle Antwort
        if relevant_sentences:
            answer = "Basierend auf den gefundenen Dokumenten:\n\n"
            for sentence, _ in relevant_sentences[:3]:
                answer += f"• {sentence}.\n"
        else:
            answer = f"Die gefundenen Dokumente enthalten Informationen zu '{question}', aber keine direkten Antworten."
        
        return answer
    
    def interactive_mode(self):
        """Startet interaktiven Modus"""
        print("\n" + "="*60)
        print("🎯 INTERAKTIVER SUCH-MODUS")
        print("="*60)
        print("Stelle Fragen zu Cybersecurity Papers!")
        print("Kommandos:")
        print("  'quit' oder 'q' - Beenden")
        print("  'stats' - Zeige Statistiken")
        print()
        
        while True:
            try:
                question = input("❓ Deine Frage: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Auf Wiedersehen!")
                    break
                
                if question.lower() == 'stats':
                    print(f"📊 System-Statistiken:")
                    print(f"   Chunks: {len(self.chunks)}")
                    print(f"   Indexierte Wörter: {len(self.word_index)}")
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
    print("🚀 Basic RAG-System startet...")
    
    try:
        # System initialisieren
        rag = BasicRAGSystem()
        
        # Test-Fragen
        test_questions = [
            "machine learning cybersecurity",
            "threat detection algorithms",
            "artificial intelligence security"
        ]
        
        print("\n🎯 Teste mit Beispiel-Fragen:")
        for question in test_questions[:2]:
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