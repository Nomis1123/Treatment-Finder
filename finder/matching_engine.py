import os
import pandas as pd





class PatientDataHandler:
    """
    A class to handle patient data and hospital data for a hospital finder application.
    """
    
    SEVERITY_MAP = {
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
    
    def __init__(self, patient_file: str, hospital_file: str):
        """
        Initializes the PatientDataHandler with patient and hospital data from CSV files.
        """
        try:
            self.patient_df = pd.read_csv(patient_file)
            self.hospital_df = pd.read_csv(hospital_file)
            self.temp_df = self.patient_df.copy()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Data file not found: {e}")
        
        self.severity_map = self.SEVERITY_MAP
        
        self.simple_patient_df = self.__standardize_df()


    def __standardize_severity(self, raw_severity: str) -> str:
        """
        Takes a raw severity string, converts it to lowercase, and uses the 
        severity_map to return a standardized category.
        Returns 'Unknown' if the keyword is not found in the map.
        """
        if not isinstance(raw_severity, str):
            return 'Unknown'
        return self.severity_map.get(raw_severity.lower(), 'Unknown')


    def __standardize_df(self) -> pd.DataFrame:
    # Standardize the 'Severity' column in the patient DataFrame
        self.temp_df['Severity'] = self.temp_df['Severity'].apply(self.__standardize_severity)
        simple_patient_df = self.temp_df[['PatientID', 'AffectedBodyPart', 'Injury/Sickness', 'Severity']]
        return simple_patient_df


    def get_original_data(self, option: int) -> pd.DataFrame:
        """
        Returns a DataFrame containing basic hospital data.
        
        Args:
            option (int): The option to filter the data.
                        1 for all patients, 2 for all hospitals
        
        Returns:
            pd.DataFrame: A DataFrame with hospital data with only HospitalID, Name, and Location.
        """
        
        if option == 1:
            return self.patient_df
        elif option == 2:
            return self.hospital_df
        else:
            raise ValueError("Invalid option. Please choose 1 or 2.")


    def get_patient_data_basic(self, option: str) -> pd.DataFrame:
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
        
        if option == 'all':
            return self.simple_patient_df[required_columns]
        elif option == 'low':
            return self.simple_patient_df.loc[self.simple_patient_df['Severity'] == 'Low', required_columns]
        elif option == 'medium':
            return self.simple_patient_df.loc[self.simple_patient_df['Severity'] == 'Medium', required_columns]
        elif option == 'high':
            return self.simple_patient_df.loc[self.simple_patient_df['Severity'] == 'High', required_columns]
        elif option == 'chronic':
            return self.simple_patient_df.loc[self.simple_patient_df['Severity'] == 'Chronic', required_columns]
        else:
            raise ValueError("Invalid option. Please choose 1, 2, 3, or 4.")
        
        
    