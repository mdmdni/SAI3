# 🔐 Sicherheitsleitfaden für OpenAI Integration

## ⚠️ Wichtige Sicherheitshinweise

**NIEMALS** API Keys in Code-Dateien speichern oder in Git committen!

## ✅ Sichere API Key Verwendung

### Option 1: Environment Variable (Empfohlen)
```bash
# Terminal/Shell
export OPENAI_API_KEY="sk-your-api-key-here"
python3 RAG_with_OpenAI.py
```

### Option 2: .env Datei (für lokale Entwicklung)
```bash
# Erstelle .env Datei (wird von .gitignore ignoriert)
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# Lade in Python (falls python-dotenv installiert)
from dotenv import load_dotenv
load_dotenv()
```

### Option 3: User Input (im Script integriert)
```bash
# Script fragt automatisch nach API Key
python3 RAG_with_OpenAI.py
# Eingabe: sk-your-api-key-here
```

## 🛡️ Was GitHub Push Protection verhindert

GitHub erkennt automatisch:
- ✅ OpenAI API Keys (sk-...)
- ✅ AWS Access Keys
- ✅ Database Connection Strings
- ✅ Private SSH Keys
- ✅ Andere sensitive Daten

## 🔧 Falls versehentlich committed

### 1. API Key sofort widerrufen
```bash
# Gehe zu https://platform.openai.com/api-keys
# Lösche den kompromittierten Key
# Erstelle einen neuen Key
```

### 2. Git History bereinigen
```bash
# Letzten Commit rückgängig machen
git reset --soft HEAD~1

# Oder BFG Repo-Cleaner verwenden für komplette History
# https://rtyley.github.io/bfg-repo-cleaner/
```

## 💡 Best Practices

1. **Environment Variables verwenden**
2. **.gitignore konfigurieren**
3. **Secrets nur lokal speichern**
4. **Keys regelmäßig rotieren**
5. **Minimale Permissions vergeben**

## 📚 Weiterführende Links

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OpenAI API Key Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Environment Variables Guide](https://12factor.net/config) 