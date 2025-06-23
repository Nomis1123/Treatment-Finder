from finder import matching_engine as me
from finder import ai_funcs as ac


print('\n')
print(me.get_patient_data_basic(1).head())
print('\n')
print(me.get_patient_data_basic(2).head())
print('\n')
print(me.get_patient_data_basic(3).head())
print('\n')
print(me.get_patient_data_basic(4).head())
print('\n')
print(me.get_patient_data_basic(5).head())

print('\n')
print('\n')
print('\n')

ac.setup_gemini()
ac.generate_text("Explain the concept of 'dark matter' to a 10-year-old.")
print('\n')


