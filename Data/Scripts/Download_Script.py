import arxiv
import requests
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Fix für Unicode-Fehler
# Erstelle einen Ordner für die PDFs auf dem Desktop
save_directory = r"/Users/mdni/PycharmProjects/SAI3/Data/PDF_Data"
os.makedirs(save_directory, exist_ok=True)
# Suche nach den neuesten Papern zu einem Thema (z.B. "machine learning")
search = arxiv.Search(
   query="cyber security AND cat:cs.CR",
   max_results=250,
   sort_by=arxiv.SortCriterion.SubmittedDate
)
# Verwende die neue Methode `Client().results()`
from arxiv import Client
client = Client()
# PDFs herunterladen
for paper in client.results(search):
   pdf_url = paper.pdf_url
   print(f"PDF URL: {pdf_url}")  # Gibt die URL aus, bevor du die Datei herunterlädst
   # Bereinigung des Dateinamens
   pdf_filename = os.path.join(save_directory, f"{paper.title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('?', '_')}.pdf")
   try:
       response = requests.get(pdf_url)
       # Prüfe, ob der Download erfolgreich war
       if response.status_code == 200:
           with open(pdf_filename, "wb") as f:
               f.write(response.content)
           print(f"PDF gespeichert: {pdf_filename}")
       else:
           print(f"Fehler beim Herunterladen der Datei {pdf_filename}. Status Code: {response.status_code}")
   except Exception as e:
       print(f"Fehler beim Herunterladen der Datei {pdf_filename}: {e}")