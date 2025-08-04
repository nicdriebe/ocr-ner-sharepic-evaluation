## OCR und NER Evaluation bestehender Open Source Modelle

Ziel des Projekts war die Evaluation verschiedener OCR- und NER-Modelle 
hinsichtlich ihrer Leistungsfähigkeit auf einem Datensatz von deutschsprachigen Veranstaltungs-Sharepics.

### Projektstruktur
├── data/                     # Bilddaten und Annotationen (Sharepics, Labels)
├── data_preparation/        # Skripte zur Datenvorverarbeitung und Formatkonvertierung
├── image_dataset_overview.ipynb  # Visuelle Übersicht und Analyse des Datensatzes
├── notebooks/               # Experimente und Evaluationen (OCR, NER)
├── requirements.txt         # Allgemeine Umgebung (SpaCy, Tesseract, OCR)
├── requirements-flair.txt   # Separate Umgebung für Flair (Torch-kompatibel)
├── utils/                   # Hilfsfunktionen, z. B. für Evaluation oder Visualisierung



### Umgebungen

Zwei getrennte Python-Umgebungen wurden verwendet:

#### 1. `requirements.txt` (allgemeine Umgebung)
- Für die meisten Notebooks
- Beinhaltet:
  - spaCy (`spacy==3.8.7`)
  - OCR mit Tesseract (`pytesseract`)
  - `easyocr`
  - Weitere Tools für NER, Textanalyse, Visualisierung
- Läuft stabil mit **Python 3.10**

#### 2. `requirements-flair.txt` (spezielle Umgebung für Flair)
- Nur für Notebooks, die **Flair** verwenden
- Gründe: inkompatible `torch`-Versionen
- Beinhaltet:
  - `flair==0.15.1`
  - `easyocr`
- Empfohlen mit **Python 3.11**

### Nutzung

```bash
# Allgemeine Umgebung
pip install -r requirements.txt

# Flair-Umgebung
pip install -r requirements-flair.txt
