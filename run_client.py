import pandas as pd

from finder.ai_funcs import GeminiClient as ac
from finder.analysis import SpecialtyAnalyzer as sa
from finder.hospital_finder import HospitalFinder as hf
from finder.matching_engine import PatientDataHandler as pdh


def setup():
    global ai_client, analyzer, hospital_finder, data_handler
    
    try:
        ai_client = ac()
        analyzer = sa(ai_client)
        hospital_finder = hf("./Data/hospitalData.csv") 
        data_handler = pdh("./Data/patientData.csv", "./Data/hospitalData.csv")
        print("All components initialized successfully.")
        print(25*'-')
    
    except Exception as e:
        print(f"Error during setup: {e}")
        raise
    
def get_results_single(name: str, injury_desc: str):
    """
    Takes a patient's name and injury description, determines the specialty needed,
    and finds hospitals that can treat the injury.
    
    Args:
        name (str): The name of the patient.
        injury_desc (str): A description of the patient's injury or sickness.
        
    Returns:
        None
    """
    
    determined_speciality = analyzer.get_specialty(injury_desc)
    
    if 'Error' in determined_speciality:
        print(f"Error determining specialty for '{name}': {determined_speciality}")
        return
    
    hospital_names = hospital_finder.get_hospital_by_specialty(determined_speciality)
    
    if not hospital_names:
        print(f"No hospitals found for specialty '{determined_speciality}' for patient '{name}'.")
        return
    
    print(f"Patient: {name}")
    print(f"Injury/Sickness: {injury_desc}")
    print(f"Determined Specialty: {determined_speciality}")
    print("Recommended Hospital(s):")
    
    for hospital in hospital_names:
        print(f"- {hospital}")

def get_results_csv():
    patient_data = data_handler.get_patient_data_basic('all')
    
    if patient_data is None:
        print("No patient data found. Exiting.")
        return
     
    print("Patient data loaded successfully.")
    print(f"Number of patients: {len(patient_data)}")
    print(25*'-')
    
    results_list = []
    
    for index, row in patient_data.head(10).iterrows():
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
    setup()
    get_results_single("John Doe", "Severe headache and dizziness")
    
    
    