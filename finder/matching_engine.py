import os
import pandas as pd


severity_map = {
    'critical': 'High',
    'severe': 'High',
    'serious': 'High',
    'life-threatening': 'High',
    
    'moderate': 'Medium',
    
    'low': 'Low',
    'mild': 'Low',
    'minor': 'Low',

    'chronic/stable': 'Chronic'
}

# Load the patient and hospital data from CSV files
file_path_patient = "./Data/patientData.csv"
file_path_hospital = "./Data/hospitalData.csv"

patient_df = pd.read_csv(file_path_patient)
temp_df = pd.read_csv(file_path_patient)
hospital_df = pd.read_csv(file_path_hospital)
print(patient_df['Severity'].value_counts())


def standardize_severity(raw_severity: str) -> str:
    """
    Takes a raw severity string, converts it to lowercase, and uses the 
    severity_map to return a standardized category.
    Returns 'Unknown' if the keyword is not found in the map.
    """
    return severity_map.get(raw_severity.lower(), 'Unknown')


# Standardize the 'Severity' column in the patient DataFrame
temp_df['Severity'] = temp_df['Severity'].apply(standardize_severity)
simple_patient_df = temp_df[['PatientID', 'AffectedBodyPart', 'Injury/Sickness', 'Severity']]
print(simple_patient_df['Severity'].value_counts())


def get_original_data(option: int) -> pd.DataFrame:
    """
    Returns a DataFrame containing basic hospital data.
    
    Args:
        option (int): The option to filter the data.
                       1 for all patients, 2 for all hospitals
    
    Returns:
        pd.DataFrame: A DataFrame with hospital data with only HospitalID, Name, and Location.
    """
    
    if option == 1:
        return patient_df
    elif option == 2:
        return hospital_df
    else:
        raise ValueError("Invalid option. Please choose 1 or 2.")


def get_patient_data_basic(option: int) -> pd.DataFrame:
    """
    Returns a DataFrame containing basic patient data.
    
    Args:
        option (int): The option to filter the patient data.
                       1 for all patients, 2 for patients with low-severity conditions, 
                       3 for moderate-severity, and 4 for high-severity conditions, and 5 for chronic conditions.
    
    Returns:
        pd.DataFrame: A DataFrame with patient data with only PatientID, Name, and AffectedBodyPart.
    """
    required_columns = ['PatientID', 'AffectedBodyPart', 'Injury/Sickness']
    
    if option == 1:
        return simple_patient_df[required_columns]
    elif option == 2:
        return simple_patient_df.loc[simple_patient_df['Severity'] == 'Low', required_columns]
    elif option == 3:
        return simple_patient_df.loc[simple_patient_df['Severity'] == 'Medium', required_columns]
    elif option == 4:
        return simple_patient_df.loc[simple_patient_df['Severity'] == 'High', required_columns]
    elif option == 5:
        return simple_patient_df.loc[simple_patient_df['Severity'] == 'Chronic', required_columns]
    else:
        raise ValueError("Invalid option. Please choose 1, 2, 3, or 4.")
    
    
    