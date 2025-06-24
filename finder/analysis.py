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
        You are an expert medical data processor. Analyze the patient's injury description
        and return ONLY a valid string with the most relevant medical specialty.
        If the description does not match any specific specialty, return 'General/Minor Care'.

        Patient Injury Description: '{injury_description}'
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


        
