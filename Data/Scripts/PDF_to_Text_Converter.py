"""
PDF to Text Converter for RAG Project
====================================
Converts multiple PDF files from the PDF_Data directory into a single combined text file.
Limits the output to 1.2 million words as required for the RAG project.

Author: SAI3 Project Team
Date: 2025
"""

import os
import re
import sys
import unicodedata

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 nicht installiert. Installiere mit: pip install PyPDF2")
    sys.exit(1)

def clean_text(text):
    """Bereinigt Text von problematischen Unicode-Zeichen"""
    # Entferne Surrogates und andere problematische Zeichen
    text = ''.join(char for char in text if ord(char) < 0xD800 or ord(char) > 0xDFFF)
    # Normalisiere Unicode
    text = unicodedata.normalize('NFKD', text)
    # Entferne nicht-druckbare Zeichen
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    return text

def extract_text_from_pdf(pdf_path):
    """Extrahiert Text aus einer PDF-Datei"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        # Text bereinigen
        text = clean_text(text)
        return text
    except Exception as e:
        print(f"Fehler beim Verarbeiten von {pdf_path}: {e}")
        return ""

def main():
    """Hauptfunktion für die PDF-zu-Text Konvertierung"""
    # Dynamischer Pfad basierend auf aktuellem Script-Verzeichnis
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_folder = os.path.join(script_dir, "..", "PDF_Data")
    pdf_folder = os.path.abspath(pdf_folder)

    # Ausgabe-Datei
    output_text_file = os.path.join(script_dir, "..", "combined_text.txt")
    output_text_file = os.path.abspath(output_text_file)

    print(f"📁 PDF Ordner: {pdf_folder}")
    print(f"📄 Ausgabe-Datei: {output_text_file}")

    # Konfiguration
    word_limit = 1_200_000  # Projektanforderung: 1.2M Wörter
    total_words = 0
    all_text = []

    # Prüfen ob PDF Ordner existiert
    if not os.path.exists(pdf_folder):
        print(f"❌ FEHLER: PDF Ordner nicht gefunden: {pdf_folder}")
        sys.exit(1)

    # Durchlaufe PDFs im Ordner
    pdf_files = [f for f in sorted(os.listdir(pdf_folder)) if f.endswith(".pdf")]
    print(f"📚 Gefundene PDF Dateien: {len(pdf_files)}")
    print("🔄 Starte Verarbeitung...\n")

    for filename in pdf_files:
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"📖 Verarbeite: {filename}")
        text = extract_text_from_pdf(pdf_path)

        if text and text.strip():  # Nur wenn Text extrahiert wurde und nicht leer ist
            # Wörter zählen
            words = re.findall(r"\b\w+\b", text)
            num_words = len(words)
            
            if total_words + num_words <= word_limit:
                all_text.append(f"=== {filename} ===\n{text}")
                total_words += num_words
                print(f"  ✅ {num_words:,} Wörter hinzugefügt (Gesamt: {total_words:,})")
            else:
                remaining_words = word_limit - total_words
                if remaining_words > 0:
                    all_text.append(f"=== {filename} ===\n" + " ".join(words[:remaining_words]))
                    total_words += remaining_words
                    print(f"  🔚 Limit erreicht mit Datei: {filename}")
                break

    print(f"\n📊 Gesamtanzahl Wörter: {total_words:,}")

    # Speichern als TXT mit besserer Fehlerbehandlung
    try:
        combined_text = "\n\n".join(all_text)
        # Nochmal bereinigen vor dem Speichern
        combined_text = clean_text(combined_text)
        
        with open(output_text_file, "w", encoding="utf-8", errors='ignore') as f:
            f.write(combined_text)
        print(f"✅ Text erfolgreich gespeichert in: {output_text_file}")
        
        # Dateigröße anzeigen
        file_size = os.path.getsize(output_text_file)
        print(f"📏 Dateigröße: {file_size / (1024*1024):.2f} MB")
        print(f"🎯 Projektanforderungen erfüllt: {total_words:,} Wörter extrahiert!")
        
    except Exception as e:
        print(f"❌ FEHLER beim Speichern der Datei: {e}")

if __name__ == "__main__":
    main() 