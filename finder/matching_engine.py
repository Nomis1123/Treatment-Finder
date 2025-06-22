import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)








file_path_patient = "./Data/patientData.csv"
file_path_hospital = "./Data/hospitalData.csv"

patient_df = pd.read_csv(file_path_patient)
hospital_df = pd.read_csv(file_path_hospital)


def get_patient_data_basic(option: int) -> pd.DataFrame:
    """
    Returns a DataFrame containing basic patient data.
    
    Args:
        option (int): The option to filter the patient data.
                       1 for all patients, 2 for patients with low-severity conditions, 
                       3 for moderate-severity, and 4 for high-severity conditions.
    
    Returns:
        pd.DataFrame: A DataFrame with patient data with only PatientID, Name, and AffectedBodyPart.
    """
    required_columns = ['PatientID', 'Name', 'AffectedBodyPart']
    
    if option == 1:
        return patient_df[required_columns]
    elif option == 2:
        raise NotImplementedError("Filtering for low-severity (option 2) is not yet implemented.")
    elif option == 3:
        raise NotImplementedError("Filtering for moderate-severity (option 3) is not yet implemented.")
    elif option == 4:
        raise NotImplementedError("Filtering for high-severity (option 4) is not yet implemented.")
    else:
        raise ValueError("Invalid option. Please choose 1, 2, 3, or 4.")
    
    
    