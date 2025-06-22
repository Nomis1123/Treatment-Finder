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

print(patient_df['PatientID'])




    