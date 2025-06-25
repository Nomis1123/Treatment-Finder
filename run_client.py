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
        print(25*'-')
        
    except Exception as e:
        print(f"Error initializing components: {e}")
        return
    
    
    patient_data = data_handler.get_patient_data_basic(1)
    
    if patient_data is None:
        print("No patient data found. Exiting.")
        return
     
    print("Patient data loaded successfully.")
    print(f"Number of patients: {len(patient_data)}")
    print(25*'-')
    
    results_list = []
    
    for index, row in patient_data.head(100).iterrows():
        patient_id = row['PatientID']
        injury = row['Injury/Sickness']
        
        determined_speciality = analyzer.get_specialty(injury)
        
        if 'Error' not in determined_speciality:
            hospital_names = hospital_finder.get_hospital_by_specialty(determined_speciality)
        
        results_list.append(
            {
                'PatientID': patient_id,
                'Injury': injury,
                'Determined_Speciality': determined_speciality,
                'Hospital(s)': hospital_names
            }
        )
    
    results_df = pd.DataFrame(results_list)
    print("\n\n--- FINAL ANALYSIS & RECOMMENDATION REPORT ---")
    
    # Set pandas display options for better viewing in the terminal
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(results_df)
        
                
                
    

    



if __name__ == "__main__":
    main()
    
    