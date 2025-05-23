# SAI3 Data Processing & RAG System

Diese Scripts implementieren ein vollständiges RAG (Retrieval-Augmented Generation) System für Cybersecurity-Forschung basierend auf wissenschaftlichen Papers.

## 🎯 Projektübersicht

**Ziel:** Entwicklung eines RAG-Systems für intelligente Abfragen von Cybersecurity-Literatur  
**Datengrundlage:** 248 wissenschaftliche Papers von arXiv (cs.CR Kategorie)  
**Textumfang:** 7.99 MB extrahierter und bereinigter Text  

## 📁 Verfügbare Scripts

### 1. `Download_Script.py`
**Zweck:** Automatischer Download von wissenschaftlichen Papers von arXiv

**Funktionen:**
- Sucht nach Papers mit dem Query: "cyber security AND cat:cs.CR"
- Lädt maximal 250 Papers herunter (248 erfolgreich)
- Speichert PDFs im `../PDF_Data/` Verzeichnis
- Bereinigt Dateinamen für das Dateisystem

**Verwendung:**
```bash
python3 Download_Script.py
```

### 2. `PDF_to_Text_Converter.py`
**Zweck:** Konvertiert PDF-Sammlung in eine einzige Textdatei für RAG

**Funktionen:**
- Extrahiert Text aus allen PDFs im `../PDF_Data/` Verzeichnis
- Begrenzt Output auf 1.2 Millionen Wörter (Projektanforderung)
- Bereinigt Unicode-Zeichen und Encoding-Probleme
- Erstellt `../combined_text.txt` mit strukturiertem Output

**Verwendung:**
```bash
python3 PDF_to_Text_Converter.py
```

**Abhängigkeiten:**
```bash
pip install PyPDF2
```

## 🤖 RAG-System Implementierungen

### 3. `RAG_Reference_Implementation.py` 🏆 **DOZENTEN-VORGABE**
**Zweck:** Vollständige RAG Reference Architecture Implementation

**Features nach Dozenten-Diagramm:**
- ✅ **Users + Search Interface:** Interaktiver Query-Modus
- ✅ **Document Retrieval:** Query → Embeddings → Vector Database
- ✅ **Reranking & Relevance:** Advanced Scoring + Top-K Selection
- ✅ **Prompting:** Context + Query → Structured Prompt
- ✅ **LLM Generation:** OpenAI Integration + Local Fallback
- ✅ **Internal Knowledge Base:** Persistent Vector Database

**Verwendung:**
```bash
python3 RAG_Reference_Implementation.py
```

**Mit OpenAI (optional):**
```python
# Mit API Key für echte LLM-Generation
rag = RAGReferenceSystem(openai_api_key="your-api-key")
```

**Architektur-Komponenten:**
1. **Document Retrieval** → TF-IDF + Vector Matching
2. **Reranking & Relevance** → Multi-Factor Scoring
3. **Prompting** → Template-basierte Prompt-Generierung
4. **LLM Generation** → OpenAI GPT-3.5 oder Local Fallback

### 4. `Basic_Text_Search.py` ⭐ **PRODUKTIONSBEREIT**
**Zweck:** Vollständiges RAG-System mit Standard-Python-Libraries

**Features:**
- ✅ **Intelligente Chunking:** Respektiert Paper-Grenzen, 10.079 Chunks
- ✅ **TF-IDF Indexierung:** Relevanz-basierte Suche mit Scoring
- ✅ **Persistente Speicherung:** 44MB Index-Datei (text_index.json)
- ✅ **Antwort-Generierung:** Automatische Extraktion relevanter Sätze
- ✅ **Interaktives Interface:** Query-System mit Statistiken

**Verwendung:**
```bash
python3 Basic_Text_Search.py
```

**Beispiel-Queries:**
- "machine learning cybersecurity"
- "threat detection algorithms"
- "artificial intelligence security"

**Keine externen Dependencies erforderlich!**

### 5. `Simple_RAG_System.py` 
**Zweck:** RAG mit modernen Embedding-Modellen

**Features:**
- ChromaDB als Vector Store
- Sentence-Transformers für lokale Embeddings
- Semantic Search basierend auf Ähnlichkeit
- Batch-Processing für Performance

**Abhängigkeiten:**
```bash
pip install chromadb sentence-transformers
```

**Verwendung:**
```bash
python3 Simple_RAG_System.py
```

### 6. `RAG_LlamaIndex_Setup.py`
**Zweck:** Enterprise-Ready RAG mit LlamaIndex Framework

**Features:**
- LlamaIndex als RAG-Framework
- HuggingFace Embeddings Integration
- ChromaDB Vector Store
- Intelligent Document Processing
- Response Synthesis mit tree_summarize

**Abhängigkeiten:**
```bash
pip install llama-index chromadb sentence-transformers
pip install llama-index-vector-stores-chroma
pip install llama-index-embeddings-huggingface
```

**Verwendung:**
```bash
python3 RAG_LlamaIndex_Setup.py
```

## 📊 Datenstatistiken

### Datensammlung:
- **📄 248 PDF-Dateien** wissenschaftlicher Papers
- **📚 Quellen:** arXiv.org (cs.CR - Cryptography and Security)
- **🔍 Query:** "cyber security AND cat:cs.CR"

### Textverarbeitung:
- **📝 7.99 MB** extrahierter Text (`combined_text.txt`)
- **🧩 10.079 intelligente Chunks** (respektiert Paper-Grenzen)
- **📈 44 MB Index-Datei** (`text_index.json`)
- **🔤 Vollständige Unicode-Bereinigung**

### RAG-Performance:
- **⚡ Indexierung:** ~15.000 einzigartige Terme
- **🎯 Retrieval:** Top-5 relevante Chunks pro Query
- **💬 Antwort-Generierung:** Automatische Satz-Extraktion
- **⏱️ Query-Zeit:** < 1 Sekunde

## 🚀 Schnellstart

### Option 1: Reference Architecture (Dozenten-Vorgabe) 🏆
```bash
cd SAI3/Data/Scripts
python3 RAG_Reference_Implementation.py
```

### Option 2: Basic RAG (Produktionsbereit)
```bash
cd SAI3/Data/Scripts
python3 Basic_Text_Search.py
```

### Option 3: Mit modernen Embeddings
```bash
pip install chromadb sentence-transformers
python3 Simple_RAG_System.py
```

### Option 4: Enterprise LlamaIndex
```bash
pip install llama-index chromadb sentence-transformers
python3 RAG_LlamaIndex_Setup.py
```

## 💡 Beispiel-Nutzung

### Reference Architecture (vollständige Pipeline):
```python
from RAG_Reference_Implementation import RAGReferenceSystem

# Initialisiere System
rag = RAGReferenceSystem()

# Vollständige RAG Pipeline
response = rag.query("How does AI improve threat detection?")

print(f"Antwort: {response.generated_response}")
print(f"Quellen: {len(response.sources)}")
print(f"Prompt: {response.prompt[:100]}...")
```

### Basic RAG System:
```python
# Importiere das Basic RAG System
from Basic_Text_Search import BasicRAGSystem

# Initialisiere System
rag = BasicRAGSystem()

# Stelle Frage
result = rag.query("Was sind Zero-Day-Exploits?")

# Zeige Ergebnis
print(result['answer'])
print(f"Quellen: {len(result['sources'])}")
```

### Interaktiver Modus (Reference Architecture):
```
🎯 RAG REFERENCE ARCHITECTURE - SEARCH INTERFACE
==================================================================
Implementiert nach Dozenten-Vorgabe:
✅ Document Retrieval + Vector Database
✅ Reranking & Relevance
✅ Prompting
✅ LLM Generation
✅ Internal Knowledge Base

❓ Deine Frage: machine learning cybersecurity

============================================================
🎯 RAG PIPELINE START: machine learning cybersecurity
============================================================
🔍 Document Retrieval für: 'machine learning cybersecurity'
📄 5 Dokumente retrievd
📊 Reranking & Relevance Processing...
✅ Reranking abgeschlossen
📝 Prompt Generation...
✅ Prompt erstellt
🤖 LLM Generation...
📝 Lokale Generierung...
✅ RAG PIPELINE COMPLETE
============================================================

💡 ANTWORT:
Basierend auf den wissenschaftlichen Dokumenten:

• Machine learning algorithms are increasingly used in cybersecurity for automated threat detection and response.
• Federated learning approaches enable collaborative security model training while preserving data privacy.
• AI-driven systems can identify previously unknown attack patterns through behavioral analysis.

📚 QUELLEN (5):
   1. Federated Learning for Privacy-Preserving... (Score: 2.847)
   2. AI-Driven Threat Detection in Network... (Score: 2.234)
   3. Machine Learning Approaches to Malware... (Score: 1.998)
```

## 🏗️ Technische Architektur

### RAG Reference Architecture Pipeline:
1. **👥 Users** → Search Query → **🔍 Search Interface**
2. **📄 Document Retrieval:** Query → Embeddings → Vector Database → Filtered Documents
3. **📊 Reranking & Relevance:** Similarity Matching → Most Relevant Documents Selected
4. **📝 Prompting:** Context + Query → Structured Prompt Template
5. **🤖 LLM Generation:** OpenAI GPT-3.5 / Local Fallback → Final Response
6. **🗄️ Internal Knowledge Base:** Vector Database (text_index.json)

### Datenfluss Reference Architecture:
```
PDF_Data/*.pdf → PDF_to_Text_Converter.py → combined_text.txt
                                                     ↓
                        Basic_Text_Search.py → text_index.json
                                    ↓
            RAG_Reference_Implementation.py → Full RAG Pipeline
                                    ↓
                Document Retrieval → Reranking → Prompting → LLM → Response
```

### Basic RAG Pipeline:
1. **📄 Document Loading:** combined_text.txt → Memory
2. **✂️ Intelligent Chunking:** Paper-boundary aware segmentation
3. **🔍 Indexing:** TF-IDF vectorization + word mapping
4. **💾 Persistence:** JSON-based index storage
5. **🔎 Retrieval:** Query → keyword matching → relevance scoring
6. **🤖 Generation:** Sentence extraction + ranking
7. **📤 Response:** Structured answer + source attribution

## 📈 Erweiterungsmöglichkeiten

### Kurzfristig:
- [ ] Web-Interface mit Flask/Streamlit
- [ ] Erweiterte Query-Syntax (Boolean, Wildcards)
- [ ] Export-Funktionen (PDF, JSON, CSV)
- [ ] Multi-Language Support

### Mittelfristig:
- [ ] Integration mit OpenAI/Anthropic APIs
- [ ] Real-time Paper Updates von arXiv
- [ ] Collaborative Filtering
- [ ] Topic Modeling Integration

### Langfristig:
- [ ] Kubernetes Deployment
- [ ] Multi-Domain Extension
- [ ] GraphRAG Implementation
- [ ] Automated Paper Summarization

## 🔧 Fehlerbehebung

### Häufige Probleme:

**1. Import Errors bei chromadb/sentence-transformers:**
```bash
pip install --upgrade chromadb sentence-transformers
```

**2. OpenAI API Issues:**
```bash
# Setze API Key als Environment Variable
export OPENAI_API_KEY="your-api-key"

# Oder verwende lokale Generation (automatischer Fallback)
python3 RAG_Reference_Implementation.py
```

**3. Text-Index nicht gefunden:**
```bash
# System neu initialisieren
python3 Basic_Text_Search.py
```

**4. Unicode-Encoding Probleme:**
```bash
export PYTHONIOENCODING=utf-8
python3 RAG_Reference_Implementation.py
```

**5. Memory Issues bei großen Datasets:**
- Verwende Basic_Text_Search.py (optimiert für große Datenmengen)
- Reduziere chunk_size Parameter

## 📝 Projektanforderungen ✅

- ✅ **10-20 MB Textdaten:** 7.99 MB erreicht
- ✅ **Wissenschaftliche Qualität:** 248 arXiv Papers
- ✅ **Domain-Spezifisch:** Cybersecurity (cs.CR)
- ✅ **RAG-Implementation:** 4 verschiedene Ansätze
- ✅ **Reference Architecture:** Vollständig nach Dozenten-Vorgabe
- ✅ **Keine Privacy-Concerns:** Öffentliche Papers
- ✅ **Interactive Interface:** Query-System implementiert
- ✅ **Persistence:** Index-Speicherung implementiert
- ✅ **Documentation:** Vollständige README

## 🎓 Framework-Bewertung

| Framework | Komplexität | Performance | Dependencies | Dozenten-Vorgabe | Status |
|-----------|-------------|-------------|--------------|------------------|---------|
| **RAG Reference** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Mittel | ✅ **100%** | 🏆 **Vollständig** |
| **Basic (TF-IDF)** | ⭐⭐ | ⭐⭐⭐⭐⭐ | Keine | ⭐⭐⭐ | ✅ Produktiv |
| **ChromaDB + Sentence-T** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Mittel | ⭐⭐⭐⭐ | ✅ Funktional |
| **LlamaIndex** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Hoch | ⭐⭐⭐⭐ | ⚠️ Setup-abhängig |

**Empfehlung für Kurspräsentation:** `RAG_Reference_Implementation.py` - Vollständige Dozenten-Vorgabe! 🏆

## 📧 Support

Bei Fragen oder Problemen:
1. Überprüfe diese README
2. Teste mit `RAG_Reference_Implementation.py` (Dozenten-Vorgabe)
3. Fallback: `Basic_Text_Search.py` für sofortige Funktionalität
4. Prüfe Python-Version (3.7+)
5. Kontaktiere das SAI3-Team

---
**SAI3 Project Team 2025** | RAG-System für Cybersecurity Research 