## Evaluation of Open-Source OCR and NER Models on German Social Media Event Sharepics 

This repository contains the source code and evaluation framework for my **Bachelor's Thesis**. The project focuses on benchmarking various open-source models for Optical Character Recognition (OCR) and Named Entity Recognition (NER) specifically applied to German-language event "sharepics" (social media announcement images).

### Project Overview
Event sharepics present unique challenges for automated information extraction due to complex layouts, diverse typography, and noisy backgrounds. This research evaluates the performance of state-of-the-art open-source tools in extracting relevant event metadata (e.g., dates, locations, titles).

* **Objective:** Benchmark OCR and NER pipelines for German event announcements.
* **Dataset:** German-language event sharepics from various social media channels.
* **Evaluation Strategy:** To isolate the performance of the extraction models, **NER and LLM evaluations were conducted on Ground Truth text**. This ensures that the results reflect the models' natural language understanding independently of OCR-related errors.
* **Key Focus:** Accuracy (WER/CER, F1-Score) and robustness against complex layouts and diverse typography.


### Evaluated Models

#### OCR Engines
* **Tesseract OCR (v5.5.0):** Tested with various Page Segmentation Modes (`psm 1, 3, 11`).
* **EasyOCR:** Deep learning approach using **CRAFT** and **CRNN**, optimized for irregular fonts and complex backgrounds.

#### NER Models (Tested on Ground Truth)
Evaluated on **Span-Level** (exact match of text and position required).
* **spaCy:** Efficient CNN-based models (`de_core_news_md/lg`) designed for high-speed CPU performance.
* **Flair:** SOTA library utilizing **contextual string embeddings** to resolve semantic ambiguities.
  * `ner-german-large`: High-performance general German NER.
  * `ner-german-legal`: Specialized model trained on legal data. Used to test if fine-grained classes (`STADT`, `STR`) mapped to `LOC` improve detection in address-heavy sharepic texts.

#### Large Language Models (LLM)
* **Gemma 2 2B:** Evaluated for instruction-based extraction using a deterministic `user–model` prompt structure and JSON output.

### Methodology & Metrics

#### Quantitative Evaluation
1. **OCR:** CER and WER calculated via `jiwer`. Layout shifts were addressed using a **Levenshtein-based line matching** algorithm (0.4 threshold).
2. **NER:** Precision, Recall, and F1-Score.
   * **Strict Matching:** Any deviation in character spans (e.g., "Seestr" vs "Seestr.") or labels results in a false detection.
3. **LLM:** Semantic matching of entities (content-based correctness) in structured JSON.


#### Qualitative Evaluation
Systematic error analysis focusing on:
* **OCR:** Impact of unusual typography and noisy backgrounds on recognition rates.
* **NER:** Analysis of False Positives, partial detections, and model-specific weaknesses in informal social media language.

---

### Repository Structure
```text
├── data/                # Images, annotations, evaluation results
├── data_preparation/    # Scripts for preprocessing and format conversion
├── notebooks/           # OCR, NER, and LLM experiment notebooks
├── utils/               # Helper functions for Levenshtein matching, WER/CER
├── requirements.txt     # General environment (spaCy, Tesseract, etc.)
└── requirements-flair.txt # Flair-specific environment (PyTorch-compatible)
```

### Environments & Setup

Due to conflicting torch dependencies, this project uses two separate Python environments:

**1. General Environment** (requirements.txt)  
    **Use case:** Tesseract, EasyOCR, spaCy, and general analysis.  
    **Python Version:** 3.10 (recommended)

```bash
pip install -r requirements.txt
python -m spacy download de_core_news_lg
python -m spacy download de_core_news_md
```

**2. Flair Environment** (requirements-flair.txt)  
    **Use case:** Exclusively for Flair notebooks.  
    **Python Version:** 3.11 (recommended)

```bash
pip install -r requirements-flair.txt
```

## Bachelor's Thesis
Developed as part of my Bachelor's degree at **[HTW Berlin - University of Applied Science]**.
* **Author:** [Nicole Driebe]
* **Supervisors:** [Prof. Dr. Helena Mihaljevic, Elisabeth Steffen]
* **Date:** 2025

---
License: [MIT]

