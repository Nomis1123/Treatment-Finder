
import pandas as pd
import spacy
import json
import time
from ai_funcs import setup_gemini, generate_text
import matching_engine as me


SPACY_SPECIALTY_MAP = {
    'Cardiology': ['heart', 'cardio', 'aorta', 'infarction', 'angina', 'stenosis', 'fibrillation', 'embolism', 'pericarditis'],
    'Neurology': ['brain', 'neuro', 'stroke', 'aneurysm', 'seizure', 'epilepsy', 'als', "parkinson's", 'dementia', 'meningioma', 'hematoma', 'neuralgia'],
    'Orthopedics': ['fracture', 'osteoarthritis', 'joint', 'bone', 'skeletal', 'scoliosis', 'sprain', 'disc', 'dislocated', 'hip'],
    'Oncology': ['cancer', 'tumor', 'leukemia', 'lymphoma', 'melanoma', 'sarcoma', 'glioblastoma', 'myeloma'],
    'Gastroenterology': ['gastro', 'crohn', 'colitis', 'liver', 'hepatitis', 'pancreas', 'bowel', 'esophageal', 'ulcerative'],
    'Nephrology/Urology': ['kidney', 'renal', 'nephritis', 'bladder', 'prostate'],
    'Pulmonology': ['lungs', 'respiratory', 'pulmonary', 'copd', 'asthma', 'fibrosis', 'pneumonia'],
    'Dermatology': ['skin', 'burn', 'psoriasis', 'dermatitis', 'eczema', 'acne'],
    'Psychiatry': ['psychiatric', 'psychosis', 'schizophrenia', 'anorexia', 'bulimia', 'bipolar', 'anxiety', 'ocd'],
    'Rheumatology/Immunology': ['arthritis', 'lupus', 'scleroderma', 'vasculitis', 'immune', 'fibromyalgia'],
    'Endocrinology': ['endocrine', 'diabetes', 'thyroid', 'adrenal'],
    'Gynecology/Reproductive': ['reproductive', 'uterus', 'ovaries', 'pcos', 'endometriosis', 'pregnancy'],
    'Ophthalmology': ['eye', 'retina', 'macular', 'glaucoma'],
    'General/Minor Care': ['headache', 'cold', 'constipation', 'gout', 'strain']
}

# spaCy setup
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

# Gemini setup
try:
    setup_gemini()
except ValueError as e:
    print(e)
    exit()
    
GEMINI_JSON_PROMPT = """
You are an expert medical data processor. Analyze the patient's injury description
and return ONLY a valid JSON object with the key "medical_specialty".

Patient Injury Description: '{injury_description}'
"""

def get_specialty_spacy(description: str) -> str | None:
    """
    Uses spaCy to analyze the injury description and return the most relevant medical specialty.
    
    Args:
        injury_description (str): The description of the patient's injury.
        
    Returns:
        str: The identified medical specialty or 'General/Minor Care' if no match is found.
    """
    doc = nlp(description)
    imp_words = []
    
    for chunk in doc.noun_chunks:
        text = (chunk.root).text
        final_text = text.lower().strip()
        imp_words.append(final_text)
    
    full_text = description.lower().strip()
    all_words = set(imp_words + full_text.split())
    
    for word in all_words:
        for specialty, keywords in SPACY_SPECIALTY_MAP.items():
            if word in keywords:
                return specialty
            
    return None
    
        
