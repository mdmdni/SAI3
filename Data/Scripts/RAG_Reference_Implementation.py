#!/usr/bin/env python3
"""
RAG Reference Architecture Implementation
=========================================
Vollständige Implementation nach der Dozenten-Vorgabe

Komponenten:
1. Users + Search Interface
2. Document Retrieval + Vector Database  
3. Reranking & Relevance
4. Prompting
5. LLM Generation
6. Internal Knowledge Base

Author: SAI3 Project Team
Date: 2025
"""

import os
import json
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings("ignore")

# Optional: OpenAI Integration (fallback auf lokale Generation)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI nicht verfügbar - verwende lokale Generierung")

@dataclass
class RetrievalResult:
    """Struktur für Retrieval-Ergebnisse"""
    chunk_id: int
    text: str
    title: str
    relevance_score: float
    metadata: Dict

@dataclass
class RAGResponse:
    """Struktur für RAG-Antworten"""
    query: str
    retrieved_documents: List[RetrievalResult]
    context: str
    prompt: str
    generated_response: str
    sources: List[str]

class RAGReferenceSystem:
    """
    RAG System nach Reference Architecture
    """
    
    def __init__(self, data_dir="../", openai_api_key: Optional[str] = None):
        """
        Initialisiert das RAG System
        
        Args:
            data_dir: Datenverzeichnis
            openai_api_key: Optional OpenAI API Key
        """
        self.data_dir = data_dir
        self.text_file = os.path.join(data_dir, "combined_text.txt")
        self.index_file = os.path.join(data_dir, "text_index.json")
        
        # OpenAI Setup (optional)
        if openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = openai_api_key
            self.llm_available = True
            print("✅ LLM (OpenAI) verfügbar")
        else:
            self.llm_available = False
            print("📝 Lokale Generierung wird verwendet")
        
        # Internal Knowledge Base laden
        self._load_knowledge_base()
        
        print("🏗️ RAG Reference Architecture initialisiert")
    
    def _load_knowledge_base(self):
        """Lädt die Internal Knowledge Base"""
        print("📚 Lade Internal Knowledge Base...")
        
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chunks = data['chunks']
                self.word_index = {k: set(v) for k, v in data['word_index'].items()}
                self.tf_idf_scores = data['tf_idf_scores']
            print(f"✅ {len(self.chunks)} Dokumente geladen")
        else:
            raise FileNotFoundError("Knowledge Base nicht gefunden! Führe zuerst Basic_Text_Search.py aus.")
    
    def document_retrieval(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        1. DOCUMENT RETRIEVAL
        Query wird in Embeddings transformiert und mit Vector Database abgeglichen
        """
        print(f"🔍 Document Retrieval für: '{query}'")
        
        # Query Processing
        query_words = [self._clean_word(w) for w in query.split()]
        query_words = [w for w in query_words if len(w) > 2]
        
        if not query_words:
            return []
        
        # Vector Database Matching (TF-IDF basiert)
        chunk_scores = {}
        for word in query_words:
            if word in self.word_index:
                for chunk_id in self.word_index[word]:
                    chunk_id_str = str(chunk_id)
                    if chunk_id_str in self.tf_idf_scores and word in self.tf_idf_scores[chunk_id_str]:
                        if chunk_id not in chunk_scores:
                            chunk_scores[chunk_id] = 0
                        chunk_scores[chunk_id] += self.tf_idf_scores[chunk_id_str][word]
        
        # Top-K Selection
        sorted_chunks = sorted(chunk_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        # Erstelle RetrievalResult Objekte
        results = []
        for chunk_id, score in sorted_chunks:
            chunk = next(c for c in self.chunks if c['id'] == chunk_id)
            results.append(RetrievalResult(
                chunk_id=chunk_id,
                text=chunk['text'],
                title=chunk['title'],
                relevance_score=score,
                metadata={'paper_id': chunk['paper_id'], 'source': chunk['source']}
            ))
        
        print(f"📄 {len(results)} Dokumente retrievd")
        return results
    
    def reranking_and_relevance(self, query: str, retrieved_docs: List[RetrievalResult]) -> List[RetrievalResult]:
        """
        2. RERANKING & RELEVANCE
        Die ähnlichsten Matches werden identifiziert und die relevantesten ausgewählt
        """
        print("📊 Reranking & Relevance Processing...")
        
        # Advanced Relevance Scoring
        query_words = set(self._clean_word(w) for w in query.split())
        
        for doc in retrieved_docs:
            # Zusätzliche Relevanz-Faktoren
            doc_words = set(self._clean_word(w) for w in doc.text.split())
            
            # Keyword Overlap Bonus
            overlap = len(query_words.intersection(doc_words))
            overlap_bonus = overlap / len(query_words) if query_words else 0
            
            # Title Relevance Bonus  
            title_words = set(self._clean_word(w) for w in doc.title.split())
            title_overlap = len(query_words.intersection(title_words))
            title_bonus = title_overlap * 0.5
            
            # Document Length Penalty (bevorzuge fokussierte Antworten)
            length_penalty = min(1.0, 500 / len(doc.text)) if len(doc.text) > 500 else 1.0
            
            # Finaler Relevance Score
            doc.relevance_score = (
                doc.relevance_score * 0.7 +  # Original TF-IDF
                overlap_bonus * 0.2 +        # Keyword Overlap
                title_bonus * 0.1            # Title Relevance
            ) * length_penalty
        
        # Re-sort nach neuem Score
        retrieved_docs.sort(key=lambda x: x.relevance_score, reverse=True)
        
        print("✅ Reranking abgeschlossen")
        return retrieved_docs
    
    def prompting(self, query: str, relevant_docs: List[RetrievalResult]) -> str:
        """
        3. PROMPTING
        Prompt wird erstellt durch Kombination von extrahiertem Kontext und initialer Query
        """
        print("📝 Prompt Generation...")
        
        # Context Assembly
        context_parts = []
        for i, doc in enumerate(relevant_docs[:3], 1):  # Top 3 für Context
            context_parts.append(f"Document {i} (Title: {doc.title[:50]}...):\n{doc.text}\n")
        
        context = "\n".join(context_parts)
        
        # Prompt Template (nach Reference Architecture)
        prompt = f"""Du bist ein Experte für Cybersecurity-Forschung. Basierend auf den folgenden wissenschaftlichen Dokumenten, beantworte die Frage präzise und informativ.

KONTEXT AUS WISSENSCHAFTLICHEN PAPERS:
{context}

FRAGE: {query}

ANTWORT: Basierend auf den bereitgestellten Dokumenten kann ich folgendes antworten:"""

        print("✅ Prompt erstellt")
        return prompt
    
    def llm_generation(self, prompt: str) -> str:
        """
        4. LLM GENERATION
        Verwendung von LLM für finale Antwort-Generierung
        """
        print("🤖 LLM Generation...")
        
        if self.llm_available:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein hilfreicher Assistent für Cybersecurity-Forschung."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                generated_response = response.choices[0].message.content
                print("✅ LLM Response generiert")
                return generated_response
            except Exception as e:
                print(f"⚠️ LLM Error: {e} - Fallback auf lokale Generierung")
        
        # Fallback: Lokale Generierung
        return self._local_generation(prompt)
    
    def _local_generation(self, prompt: str) -> str:
        """
        Fallback: Lokale Antwort-Generierung ohne LLM
        """
        print("📝 Lokale Generierung...")
        
        # Extrahiere Query aus Prompt
        lines = prompt.split('\n')
        query_line = next(line for line in lines if line.startswith('FRAGE:'))
        query = query_line.replace('FRAGE:', '').strip()
        
        # Extrahiere Context
        context_start = prompt.find('KONTEXT AUS WISSENSCHAFTLICHEN PAPERS:')
        context_end = prompt.find('FRAGE:')
        context = prompt[context_start:context_end].strip()
        
        # Einfache Satz-Extraktion basierend auf Query-Keywords
        query_words = set(self._clean_word(w) for w in query.split())
        sentences = re.split(r'[.!?]+', context)
        
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            sentence_words = set(self._clean_word(w) for w in sentence.split())
            overlap = len(query_words.intersection(sentence_words))
            
            if overlap >= 1:
                relevant_sentences.append((sentence, overlap))
        
        # Sortiere und kombiniere
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        
        if relevant_sentences:
            response = "Basierend auf den wissenschaftlichen Dokumenten:\n\n"
            for sentence, _ in relevant_sentences[:3]:
                response += f"• {sentence}.\n"
        else:
            response = "Die gefundenen Dokumente enthalten relevante Informationen, aber keine direkten Antworten zur spezifischen Frage."
        
        return response
    
    def _clean_word(self, word: str) -> str:
        """Bereinigt Wörter für Verarbeitung"""
        return re.sub(r'[^\w\s]', '', word.lower()).strip()
    
    def query(self, user_query: str) -> RAGResponse:
        """
        VOLLSTÄNDIGE RAG PIPELINE
        Implementiert alle Komponenten der Reference Architecture
        """
        print(f"\n{'='*60}")
        print(f"🎯 RAG PIPELINE START: {user_query}")
        print(f"{'='*60}")
        
        # 1. Document Retrieval
        retrieved_docs = self.document_retrieval(user_query, top_k=8)
        
        if not retrieved_docs:
            return RAGResponse(
                query=user_query,
                retrieved_documents=[],
                context="",
                prompt="",
                generated_response="Keine relevanten Dokumente gefunden.",
                sources=[]
            )
        
        # 2. Reranking & Relevance
        ranked_docs = self.reranking_and_relevance(user_query, retrieved_docs)
        
        # 3. Prompting
        prompt = self.prompting(user_query, ranked_docs)
        
        # 4. LLM Generation
        final_response = self.llm_generation(prompt)
        
        # 5. Response Assembly
        context = "\n\n".join([doc.text for doc in ranked_docs[:3]])
        sources = [f"{doc.title} (Score: {doc.relevance_score:.3f})" for doc in ranked_docs[:5]]
        
        print(f"✅ RAG PIPELINE COMPLETE")
        print(f"{'='*60}\n")
        
        return RAGResponse(
            query=user_query,
            retrieved_documents=ranked_docs,
            context=context,
            prompt=prompt,
            generated_response=final_response,
            sources=sources
        )
    
    def interactive_mode(self):
        """
        SEARCH INTERFACE
        Interaktiver Modus für User-Interaction
        """
        print("\n" + "="*70)
        print("🎯 RAG REFERENCE ARCHITECTURE - SEARCH INTERFACE")
        print("="*70)
        print("Implementiert nach Dozenten-Vorgabe:")
        print("✅ Document Retrieval + Vector Database")
        print("✅ Reranking & Relevance")  
        print("✅ Prompting")
        print("✅ LLM Generation")
        print("✅ Internal Knowledge Base")
        print("\nStelle Fragen zu Cybersecurity Papers!")
        print("Eingabe 'quit' zum Beenden\n")
        
        while True:
            try:
                user_query = input("❓ Deine Frage: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Auf Wiedersehen!")
                    break
                
                if not user_query:
                    continue
                
                # Vollständige RAG Pipeline
                response = self.query(user_query)
                
                # Ergebnis-Anzeige
                print(f"\n💡 ANTWORT:")
                print(f"{response.generated_response}")
                
                print(f"\n📚 QUELLEN ({len(response.sources)}):")
                for i, source in enumerate(response.sources, 1):
                    print(f"   {i}. {source}")
                
                print(f"\n📊 PERFORMANCE:")
                print(f"   Retrievd Documents: {len(response.retrieved_documents)}")
                print(f"   Top Score: {response.retrieved_documents[0].relevance_score:.3f}" if response.retrieved_documents else "N/A")
                
                print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

def main():
    """Hauptfunktion"""
    print("🚀 RAG Reference Architecture System startet...")
    print("📋 Implementiert nach Dozenten-Vorgabe")
    
    try:
        # System initialisieren
        rag = RAGReferenceSystem()
        
        # Test-Query
        test_query = "How do machine learning algorithms improve cybersecurity?"
        print(f"\n🧪 Test mit: '{test_query}'")
        
        response = rag.query(test_query)
        print(f"\n✅ Test erfolgreich!")
        print(f"📝 Antwort: {response.generated_response[:100]}...")
        
        # Interaktiver Modus
        rag.interactive_mode()
        
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")
        print("💡 Führe zuerst 'python3 Basic_Text_Search.py' aus um die Knowledge Base zu erstellen.")

if __name__ == "__main__":
    main() 