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
        try:
            self.hospital_df = pd.read_csv(hospital_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Hospital data file '{hospital_file}' not found.")
        
    def get_hospital_data(self) -> pd.DataFrame:
        """
        Returns the hospital data as a DataFrame.
        
        Returns:
            pd.DataFrame: A DataFrame containing hospital data.
        """
        return self.hospital_df
    
    def get_hospital_by_specialty(self, specialty: str) -> list[str] | None:
        """
        Filters the hospital data by a specific medical specialty.
        
        Args:
            specialty (str): The medical specialty to filter by.
            
        Returns:
            list: A list containing hospitals that match the specialty.
            None: If no hospitals match the specialty.
        """
        matching_hospitals = []
        
        for hospital, specialties in self.HOSPITAL_TO_SPECIALTIES_MAP.items():
            if specialty in specialties:
                matching_hospitals.append(hospital)
                
        if not matching_hospitals:
            return None
        
        return matching_hospitals
    
    def sort_hospitals_by_busyness(self, hospital_list: list[str]) -> list[str]:
            """
            Takes a list of hospital names and sorts them from least busy to most busy.
            
            Args:
                hospital_list (list[str]): A list of hospital names to be sorted.

            Returns:
                A sorted list of hospital names.
            """
            if self.hospitals_df.empty or not hospital_list:
                return hospital_list 

            filtered_df = self.hospitals_df[self.hospitals_df['name'].isin(hospital_list)]
            
            sorted_df = filtered_df.sort_values(by='busy', ascending=True)
            return sorted_df['name'].tolist()
            
            
            
        
