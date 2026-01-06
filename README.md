# Evaluation of Open-Source OCR and NER Models on German Social Media Event Sharepics

This repository contains the source code and evaluation framework for my **Bachelor's Thesis**. The project benchmarks various open-source models for Optical Character Recognition (OCR) and Named Entity Recognition (NER) specifically applied to German-language "sharepics".

## Project Overview
In modern communication, visual content like **event sharepics** (images with embedded text) has become a crucial medium for political engagement, public mobilization, and social movements. Unlike standardized internet memes, these sharepics vary significantly in layout, typography, and background complexity, making automated information extraction a significant challenge for traditional systems.

### Motivation & Goals
* **Social Relevance:** Information on protest actions or campaigns remains largely inaccessible to automated analysis. This project aims to bridge this gap for NGOs, researchers, and civil society initiatives.
* **Open Source & Privacy:** Instead of relying on proprietary, high-cost, or privacy-invasive vision-language models, this work evaluates **resource-efficient open-source alternatives**.
* **Objective:** Benchmark the reliability of OCR and NER models in extracting metadata (titles, locations, dates) to derive requirements for a software solution that runs on **limited hardware** (CPU-based).

### Key Research Questions
1. How reliably can open-source models extract structured information from heterogeneous sharepic layouts?
2. What are the requirements for a resource-efficient software solution for automated social media monitoring?

--- 
## Dataset
Since no suitable dataset was available, a custom collection of **200 German event sharepics** was curated and manually annotated for this thesis.

### Data Collection & Diversity
The images were collected from public social media channels (primarily Instagram and Telegram) of cultural institutions and NGOs. The dataset covers a wide spectrum of design styles, categorized by visual complexity:
* **Simple:** Clear layout, horizontal text, high contrast (65 images).
* **Fancy:** Unusual or decorative fonts (54 images).
* **Skewed:** Tilted, vertical, or distorted text (31 images).
* **Noisy:** Complex backgrounds or overlapping graphic elements (30 images).
* **Photo:** Real-world photographs of posters and flyers (20 images).

### Ground Truth & Annotation
* **Text Ground Truth:** Generated via a multi-step process involving OCR-assistance (ChatGPT-4o) followed by rigorous manual correction to ensure 100% accuracy in spelling and line structure.
* **Entity Annotation:** Manual span-level annotation of five categories:
  * `EVENT`: Type of event (e.g., "Kundgebung", "Tanz Demo").
  * `TOPIC`: Slogan or theme (e.g., "Gemeinsam gegen Gewalt").
  * `DATE` / `TIME`: Temporal information.
  * `LOC`: Granular location data (streets, cities, venues).
* **Format:** Data is provided in **JSON and CSV** formats, including character offsets (start/end positions) for precise NER evaluation.

---
## Evaluated Models

### OCR Engines
* **Tesseract OCR (v5.5.0):** Tested with various Page Segmentation Modes (`psm 1, 3, 11`).
* **EasyOCR:** Deep learning approach using **CRAFT** and **CRNN**, optimized for irregular fonts and complex backgrounds.

### NER Models (Tested on Ground Truth)
Evaluated on **Span-Level** (exact match of text and position required).
* **spaCy:** Efficient CNN-based models (`de_core_news_md/lg`) designed for high-speed CPU performance.
* **Flair:** SOTA library utilizing **contextual string embeddings** to resolve semantic ambiguities.
  * `ner-german-large`: High-performance general German NER.
  * `ner-german-legal`: Specialized model trained on legal data. Used to test if fine-grained classes (`STADT`, `STR`) mapped to `LOC` improve detection in address-heavy sharepic texts.

### Large Language Models (LLM)
* **Gemma 2 2B:** Evaluated for instruction-based extraction using a deterministic `user–model` prompt structure and JSON output.

## Methodology & Metrics

### Quantitative Evaluation
1. **OCR:** CER and WER calculated via `jiwer`. Layout shifts were addressed using a **Levenshtein-based line matching** algorithm (0.4 threshold).
2. **NER:** Precision, Recall, and F1-Score.
   * **Strict Matching:** Any deviation in character spans (e.g., "Seestr" vs "Seestr.") or labels results in a false detection.
3. **LLM:** Semantic matching of entities (content-based correctness) in structured JSON.


### Qualitative Evaluation
Systematic error analysis focusing on:
* **OCR:** Impact of unusual typography and noisy backgrounds on recognition rates.
* **NER:** Analysis of False Positives, partial detections, and model-specific weaknesses in informal social media language.

---

## Repository Structure
```text
├── data/                # Images, annotations, evaluation results
├── data_preparation/    # Scripts for preprocessing and format conversion
├── notebooks/           # OCR, NER, and LLM experiment notebooks
├── utils/               # Helper functions for Levenshtein matching, WER/CER
├── requirements.txt     # General environment (spaCy, Tesseract, etc.)
└── requirements-flair.txt # Flair-specific environment (PyTorch-compatible)
```

## Environments & Setup

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

