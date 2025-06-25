import pandas as pd

from finder.ai_funcs import GeminiClient as ac
from finder.analysis import SpecialtyAnalyzer as sa
from finder.hospital_finder import HospitalFinder as hf
from finder.matching_engine import PatientDataHandler as pdh



def main():
    
    
    try:
        ai_client = ac()
        analyzer = sa(ai_client)
        hospital_finder = hf("./Data/hospitalData.csv")
        data_handler = pdh("./Data/patientData.csv", "./Data/hospitalData.csv")
        print("All components initialized successfully.")
        
    except Exception as e:
        print(f"Error initializing components: {e}")
        return
    
    print(data_handler.get_patient_data_basic(2).head())


    



if __name__ == "__main__":
    main()
    
    