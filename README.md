# SAI3 - Cybersecurity RAG System 🛡️🤖

Ein intelligentes RAG (Retrieval-Augmented Generation) System für Cybersecurity-Forschung basierend auf 248 wissenschaftlichen Papers von arXiv.

## 🎯 Was ist das?

Dieses System ermöglicht es, natürlichsprachige Fragen zu Cybersecurity-Themen zu stellen und erhält präzise Antworten basierend auf aktueller wissenschaftlicher Literatur.

**Beispiel:**
```
❓ Frage: "Wie verbessert Machine Learning die Bedrohungserkennung?"
🤖 Antwort: "Basierend auf den wissenschaftlichen Dokumenten:
• Machine Learning Algorithmen werden zunehmend für automatisierte Bedrohungserkennung verwendet...
• KI-gesteuerte Systeme können unbekannte Angriffsmuster durch Verhaltensanalyse identifizieren..."
```

## 🚀 Quick Start

### 1. Repository klonen
```bash
git clone <repository-url>
cd SAI3/Data/Scripts
```

### ⭐ 2. PREMIUM: OpenAI Integration (empfohlen für beste Ergebnisse)
```bash
# Setze dein OpenAI API Key
export OPENAI_API_KEY="sk-your-api-key-here"

# Starte das Premium RAG System
python3 RAG_with_OpenAI.py
```

💰 **Kosten:** ~$0.001-0.005 pro Anfrage | 🔒 **Sicherheit:** Siehe [SECURITY.md](SECURITY.md)

### 3. Alternative: Lokales System (kostenfrei)
```bash
# Option 1: Vollständige Reference Architecture
python3 RAG_Reference_Implementation.py

# Option 2: Basic System (ohne Dependencies)
python3 Basic_Text_Search.py
```

### 4. Fragen stellen
```
❓ Deine Frage: machine learning cybersecurity
❓ Deine Frage: Was sind Zero-Day-Exploits?
❓ Deine Frage: threat detection algorithms
```

## ✨ Features

- 🔍 **Intelligente Suche** in 248 Cybersecurity-Papers
- 🤖 **RAG-Pipeline** mit Document Retrieval, Reranking & LLM Generation
- 💬 **Interaktiver Chat-Modus** für natürlichsprachige Fragen
- 📚 **Quellenangaben** für jede Antwort
- ⚡ **Schnelle Antworten** (< 1 Sekunde)
- 🔧 **Keine externe API erforderlich** (lokaler Fallback verfügbar)

## 📊 Daten

- **📄 248 PDF-Dateien** wissenschaftlicher Papers
- **📚 Quelle:** arXiv.org (Cryptography and Security)
- **📝 7.99 MB** extrahierter und bereinigter Text
- **🧩 10.079 intelligente Chunks** für optimale Suche

## 🛠️ Verfügbare RAG-Systeme

| System | Beschreibung | Qualität | Dependencies | Kosten |
|--------|--------------|----------|--------------|--------|
| **RAG_with_OpenAI.py** | Premium mit OpenAI GPT-4 | ⭐⭐⭐⭐⭐ | OpenAI API | ~$0.001-0.005/query |
| **RAG_Reference_Implementation.py** | Vollständige Dozenten-Architektur | ⭐⭐⭐⭐ | Optional: OpenAI | Kostenlos |
| **Basic_Text_Search.py** | Produktionsbereit, TF-IDF basiert | ⭐⭐⭐ | Keine | Kostenlos |
| **Simple_RAG_System.py** | Moderne Embeddings | ⭐⭐⭐⭐ | ChromaDB, Sentence-Transformers | Kostenlos |
| **RAG_LlamaIndex_Setup.py** | Enterprise Framework | ⭐⭐⭐⭐ | LlamaIndex, ChromaDB | Kostenlos |

## 🔧 Optional: Erweiterte Features

### Mit OpenAI Integration (bessere Antworten):
```bash
export OPENAI_API_KEY="your-api-key"
python3 RAG_Reference_Implementation.py
```

### Mit modernen Embeddings:
```bash
pip install chromadb sentence-transformers
python3 Simple_RAG_System.py
```

### Enterprise LlamaIndex:
```bash
pip install llama-index chromadb sentence-transformers
python3 RAG_LlamaIndex_Setup.py
```

## 📖 Beispiel-Nutzung

```python
# Programmatische Nutzung
from RAG_Reference_Implementation import RAGReferenceSystem

rag = RAGReferenceSystem()
response = rag.query("How does AI improve threat detection?")

print(f"Antwort: {response.generated_response}")
print(f"Quellen: {len(response.sources)}")
```

## 🎓 Für SAI3-Kurs

Dieses System wurde für den SAI3-Kurs entwickelt und deckt folgende Lernziele ab:
- ✅ Machine Learning Grundlagen
- ✅ Python Libraries & Data Processing  
- ✅ Information Retrieval & RAG-Systeme
- ✅ LLM Integration & Prompting
- ✅ Praktische AI-Anwendung

## 📂 Verzeichnisstruktur

```
SAI3/
├── README.md                 # Diese Datei
├── Data/
│   ├── Scripts/             # RAG-System Scripts
│   │   ├── RAG_Reference_Implementation.py  🏆
│   │   ├── Basic_Text_Search.py            ⭐
│   │   ├── Simple_RAG_System.py            🔬
│   │   ├── RAG_LlamaIndex_Setup.py         🏢
│   │   └── README.md        # Detaillierte Dokumentation
│   ├── combined_text.txt    # Extrahierter Text (7.99MB)
│   ├── text_index.json      # Suchindex (44MB)
│   └── PDF_Data/           # 248 PDF-Dateien
└── Projekt Infos/          # Zusätzliche Dokumentation
```

## 💡 Troubleshooting

**Problem:** `ModuleNotFoundError`
```bash
# Verwende das Basic System (keine Dependencies)
python3 Basic_Text_Search.py
```

**Problem:** Langsame Performance
```bash
# Das Basic System ist optimiert für große Datenmengen
python3 Basic_Text_Search.py
```

**Problem:** Text-Index nicht gefunden
```bash
# System neu initialisieren
python3 Basic_Text_Search.py
```

## 📚 Weitere Dokumentation

Für detaillierte Informationen siehe: [`Data/Scripts/README.md`](Data/Scripts/README.md)

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Committe deine Änderungen  
4. Erstelle einen Pull Request

---

**SAI3 Project Team 2025** | Intelligente Cybersecurity-Forschung mit RAG 🛡️🤖 