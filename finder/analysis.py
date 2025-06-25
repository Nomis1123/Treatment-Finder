import spacy
import time     


class SpecialtyAnalyzer:
    """
    Orchestrates the classification of medical descriptions into specialties.

    This class implements a cost-effective hybrid strategy. It first attempts
    to classify a description using a fast, local spaCy model with a curated
    keyword map. If this local method fails to produce a confident result,
    it escalates the task to a more powerful Generative AI model (Gemini)
    for advanced analysis.
    """
    
    VALID_SPECIALTIES_LIST = [
        # --- Broad, High-Level Categories ---
        'Cardiology',                # For all heart, major blood vessel, and circulation issues.
        'Neurology',                 # For brain, spine, nerve, and muscle control issues.
        'Oncology',                  # For all types of cancer and tumors.
        'Orthopedics',               # For bones, joints, ligaments, and fractures.
        'Gastroenterology',          # For the entire digestive system: esophagus, stomach, liver, pancreas, intestines.
        'Pulmonology',               # For lungs and breathing issues.
        'Nephrology/Urology',        # For kidneys, bladder, and urinary tract issues.
        'Psychiatry',                # For mental health, behavioral, and addiction disorders.
        'Rheumatology/Immunology',   # For autoimmune diseases (Lupus, RA) and systemic inflammation.
        'Endocrinology',             # For hormonal and metabolic issues (Diabetes, Thyroid).
        'Pediatrics',                # A crucial category for all childhood-specific illnesses.
        
        # --- More Specific & Surgical Categories ---
        'Trauma/Critical Care',      # For severe, multi-system injuries, shock, and life support.
        'General Surgery',           # A catch-all for common surgical needs (appendicitis, hernias, gallbladder).
        'Vascular Surgery',          # For issues with arteries and veins not directly involving the heart.
        'Plastic Surgery',           # For burns, complex wound repair, and reconstruction.
        'Infectious Disease',        # For complex infections like HIV/AIDS, sepsis, resistant bacteria.
        
        # --- Population-Specific Categories ---
        'Geriatrics',                # For conditions primarily affecting the elderly.
        'Women\'s Health/Gynecology', # For reproductive health, pregnancy, and related issues.
        
        # --- Sensory & Outpatient Specialties ---
        'Ophthalmology',             # For all eye-related conditions.
        'Dermatology',               # For skin conditions.
        'Pain Management',           # For chronic pain conditions like CRPS.
        'Rehabilitation',            # For post-injury/stroke recovery and physical therapy.
        
        # --- Fallback Categories ---
        'General/Minor Care',        # For low-acuity issues, primary care follow-up.
        'Genetics'                   # For inherited disorders.
    ]
    
    # The rest of the class remains the same...
    VALID_SPECIALTIES_STR = ", ".join(VALID_SPECIALTIES_LIST)

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
    
    GEMINI_JSON_PROMPT = """
        You are an expert medical data processor. Your task is to classify the
        following patient injury description into one of the approved medical specialties.

        **Instructions:**
        1. Analyze the 'Patient Injury Description'.
        2. Choose the SINGLE best-fitting specialty from the 'Approved Specialties' list.
        3. Your response MUST be ONLY the name of the chosen specialty and nothing else.

        **Approved Specialties:**
        {VALID_SPECIALTIES_STR}

        **Patient Injury Description:**
        '{injury_description}'
        """
    

    def __init__(self, ai_client):
        self.nlp = spacy.load("en_core_web_sm")
        self.ai_client = ai_client
        
        
    def get_specialty(self, description: str) -> str | None:
        """
        Determines the medical specialty for a given injury description using spaCy or Gemini.
        
        Args:
            description (str): The description of the patient's injury.
            
        Returns:
            str: The identified medical specialty or 'General/Minor Care' if no match is found.
        """
        specialty = self.__get_specialty_spacy(description)
        
        if specialty:
            return specialty
        else:        
            print("spaCy did not find a match, trying Gemini...")
            time.sleep(0.5)  # Adding a delay to avoid hitting API rate limits
            specialty = self.__get_specialty_gemini(description)
            if specialty:
                return specialty
            else:
                print("Gemini did not find a match, returning 'General/Minor Care'")
                return "General/Minor Care"
        
        
    def __get_specialty_spacy(self, description: str) -> str | None:
        """
        Uses spaCy to analyze the injury description and return the most relevant medical specialty.
        
        Args:
            injury_description (str): The description of the patient's injury.
            
        Returns:
            str: The identified medical specialty or 'General/Minor Care' if no match is found.
        """
        doc = self.nlp(description)
        imp_words = []
        
        for chunk in doc.noun_chunks:
            text = (chunk.root).text
            final_text = text.lower().strip()
            imp_words.append(final_text)
        
        full_text = description.lower().strip()
        all_words = set(imp_words + full_text.split())
        
        for word in all_words:
            for specialty, keywords in self.SPACY_SPECIALTY_MAP.items():
                if word in keywords:
                    return specialty
                
        return None

    
    def __get_specialty_gemini(self, description: str) -> str | None:
        """
        Uses Gemini to analyze the injury description and return the most relevant medical specialty.
        
        Args:
            injury_description (str): The description of the patient's injury.
            
        Returns:
            str: The identified medical specialty or 'General/Minor Care' if no match is found.
        """
        prompt = self.GEMINI_JSON_PROMPT.format(injury_description=description)
        
        response = self.ai_client.generate_text(prompt, model_name="gemini-2.5-flash")
        
        if response:
                return response.strip()
        else:
            return "Gemini-API-Error"
