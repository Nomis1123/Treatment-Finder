import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import csv

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

file_path_patient = "./Data/patientData.csv"
file_path_hospital = "./Data/hospitalData.csv"

patient_df = pd.read_csv(file_path_patient)
hospital_df = pd.read_csv(file_path_hospital)

print(patient_df.info())


