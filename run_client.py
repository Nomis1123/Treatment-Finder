from finder import matching_engine as me
from finder import ai_funcs as ac
from finder import analysis as an

'''
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
'''
symp_list = ['Febrile seizure', "Bulimia Nervosa with electrolyte imbalance", "Acute appendicitis with peritonitis"]
ret_list = []
for item in symp_list:
    ret_list.append(an.get_specialty(item))

print('\n')
print(ret_list)
