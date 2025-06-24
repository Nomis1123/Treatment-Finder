import pandas as pd


class HospitalFinder:
    """
    A class to handle hospital data and patient data for a hospital finder application.
    """
    
    HOSPITAL_TO_SPECIALTIES_MAP = {
    'Toronto General Hospital':        ['Cardiology', 'Trauma/Critical Care', 'Gastroenterology', 'Nephrology/Urology', 'Pulmonology'],
    'Toronto Western Hospital':        ['Neurology', 'Orthopedics', 'Rheumatology/Immunology'],
    'Mount Sinai Hospital':            ['Gastroenterology', 'Rheumatology/Immunology', 'Endocrinology', 'Pediatrics', 'Women\'s Health/Gynecology'],
    'Hennick Bridgepoint Hospital':    ['Rehabilitation', 'Geriatrics', 'Ophthalmology'],
    'St. Michael\'s Hospital':          ['Cardiology', 'Neurology', 'Trauma/Critical Care', 'Nephrology/Urology'],
    'St. Joseph\'s Health Centre':     ['Orthopedics', 'Psychiatry', 'General/Minor Care'],
    'North York General Hospital':     ['Gastroenterology', 'General/Minor Care'],
    'Michael Garron Hospital':         ['Pulmonology', 'General/Minor Care'],
    'Sunnybrook Health Sciences Centre': ['Cardiology', 'Neurology', 'Oncology', 'Orthopedics', 'Trauma/Critical Care', 'Women\'s Health/Gynecology'],
    'The Hospital for Sick Children (SickKids)': ['Pediatrics'],
    'Humber River Hospital':           ['Cardiology', 'Oncology', 'General/Minor Care'],
    'Centre for Addiction and Mental Health (CAMH)': ['Psychiatry'],
    'Women\'s College Hospital':        ['Endocrinology', 'Women\'s Health/Gynecology', 'Dermatology'],
    'Baycrest Health Sciences':        ['Rehabilitation', 'Geriatrics']
}
    

    def __init__(self, hospital_file: str):
        """
        Initializes the HospitalFinder with patient and hospital data from CSV files.
        
        Args:
            hospital_file (str): Path to the hospital data CSV file.
        """
        self.hospital_df = pd.read_csv(hospital_file)
        
    def get_hospital_data(self) -> pd.DataFrame:
        """
        Returns the hospital data as a DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame containing hospital data.
        """
        return self.hospital_df
    
    def get_hospital_by_specialty(self, specialty: str) -> pd.DataFrame:
        """
        Filters the hospital data by a specific medical specialty.
        
        Args:
            specialty (str): The medical specialty to filter by.
            
        Returns:
            pd.DataFrame: A DataFrame containing hospitals that match the specialty.
        """
        
        
        
