import os
import fitz  # PyMuPDF
import re

# Pfad zum Ordner mit PDFs
pdf_folder = "/Users/mdni/PycharmProjects/SAI3/Data/PDF_Data"

# Ausgabe-Datei
output_text_file = "/Data/combined_text.txt"

# Zielwortanzahl
word_limit = 1_200_000
total_words = 0
all_text = []

# Hilfsfunktion: Text aus PDF extrahieren
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Fehler beim Verarbeiten von {pdf_path}: {e}")
        return ""

# Durchlaufe PDFs im Ordner
for filename in sorted(os.listdir(pdf_folder)):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Verarbeite: {filename}")
        text = extract_text_from_pdf(pdf_path)

        # Wörter zählen
        words = re.findall(r"\b\w+\b", text)
        num_words = len(words)

        if total_words + num_words <= word_limit:
            all_text.append(text)
            total_words += num_words
        else:
            remaining_words = word_limit - total_words
            all_text.append(" ".join(words[:remaining_words]))
            total_words += remaining_words
            print(f"Limit erreicht mit Datei: {filename}")
            break

print(f"Gesamtanzahl Wörter: {total_words}")

# Speichern als TXT
with open(output_text_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_text))

print(f"Text gespeichert in: {output_text_file}")
