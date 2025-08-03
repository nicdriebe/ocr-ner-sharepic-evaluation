import re
import Levenshtein
from PIL import Image
import pytesseract
import jiwer
from jiwer import wer, cer

###################################
# Funktionen für die OCR Evaluation
###################################

CER_THRESHOLD = 0.4 # ← Maximaler Fehlerwert für Match (40% Fehler erlaubt)

# Textextraktion mit tesseract zeilenweise Ausgabe
def extract_ocr_lines(image_path):
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, lang='deu', output_type=pytesseract.Output.DATAFRAME)
    lines = data[data['level'] == 5] 
    grouped = lines.groupby(['block_num', 'par_num', 'line_num'])
    # erzeugt Liste mit den einzelen Zeilen in denen der Text bereinigt von NAN Werten als einzelner String zuammengefasst wurde
    line_texts = grouped['text'].apply(lambda x: ' '.join(x.dropna())).tolist() 
    return line_texts
    
# Textextraktion mit tesseract zeilenweise Ausgabe
def extract_ocr_lines_psm1(image_path):
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, lang='deu', config="--psm 1", output_type=pytesseract.Output.DATAFRAME)
    lines = data[data['level'] == 5] 
    grouped = lines.groupby(['block_num', 'par_num', 'line_num'])
    # erzeugt Liste mit den einzelen Zeilen in denen der Text bereinigt von NAN Werten als einzelner String zuammengefasst wurde
    line_texts = grouped['text'].apply(lambda x: ' '.join(x.dropna())).tolist() 
    return line_texts


# CER fürs Matching der Zeilen ground truth und OCR
def cer_for_matching(gt, pred):
    gt = re.sub(r"\s+", "", gt) # entfernt ALLE whitespaces, auch tabs und Zeilenumbrüche, macht merh als strip()
    pred = re.sub(r"\s+", "", pred)
    if not gt:
        return 0.0 if not pred else 1.0
    return Levenshtein.distance(gt, pred) / len(gt)


# Zeilen matchen mit minimalen CER
def match_gt_to_ocr(gt_lines, ocr_lines, max_cer_threshold=CER_THRESHOLD):  
    matched = []
    used_ocr_indices = set()

    for gt_idx, gt_line in enumerate(gt_lines):
        best_score = float('inf')
        best_ocr_idx = None
        best_ocr_line = ""

        for ocr_idx, ocr_line in enumerate(ocr_lines):
            if ocr_idx in used_ocr_indices:
                continue
            cer = cer_for_matching(gt_line, ocr_line)
            if cer < best_score:
                best_score = cer
                best_ocr_idx = ocr_idx
                best_ocr_line = ocr_line

        if best_score <= max_cer_threshold:
            matched.append((gt_idx, best_ocr_idx))
            used_ocr_indices.add(best_ocr_idx)
        else:
            matched.append((gt_idx, None))
    return matched


def calculate_char_accuracy(gt, pred):
    gt = re.sub(r"\s+", "", gt) 
    pred = re.sub(r"\s+", "", pred)
    if not gt:
        return 1.0 if not pred else 0.0
    acc = 1 - (Levenshtein.distance(gt, pred) / len(gt))
    return max(0.0, acc)

def calculate_word_accuracy(gt, pred):
    gt_words = gt.strip().split()
    pred_words = pred.strip().split()
    if not gt_words:
        return 1.0 if not pred_words else 0.0
    correct = sum(1 for g, p in zip(gt_words, pred_words) if g == p)
    return correct / len(gt_words)

def calculate_wer(gt, pred):
    word_error = wer(gt, pred)
    return word_error
    
def calculate_cer(gt, pred):
    char_error = cer(gt, pred)
    return char_error

#################################