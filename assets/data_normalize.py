import numpy as np; import pandas as pd

data = pd.read_csv('assets\clean_data.csv',sep='|',low_memory=False)
#data = pd.read_csv('assets\df_sample.csv',sep='|')

def normalizar():
    global data
    data.profesion.fillna('SIN ESPECIFICAR', inplace=True)


    data.fillna('SIN ESPECIFICAR', inplace=True)

    data.sitlabor = [data.sitlabor.iloc[i].upper() for i in range(len(data))]
    data.niveleduc = [data.niveleduc.iloc[i].upper() for i in range(len(data))]
    data.ecivil = [data.ecivil.iloc[i].upper() for i in range(len(data))]
    data.region = [data.region.iloc[i].upper() for i in range(len(data))]

    data.loc[data.antiguedad == 'SIN ESPECIFICAR','antiguedad'] = 0
    data.loc[data.edad == 'SIN ESPECIFICAR', 'edad'] = 0
    data.loc[data.riesgo == 'SIN ESPECIFICAR', 'riesgo'] = 0
    data.loc[data.exigencia == 'SIN ESPECIFICAR', 'exigencia'] = 0


    return [data.antiguedad.min(),data.antiguedad.max()],\
           data.profesion.unique(), \
           data.sitlabor.unique(),\
           data.niveleduc.unique(),\
           [data.edad.min(),data.edad.max()], \
           data.ecivil.unique(), \
           data.region.unique(), \
           (data.riesgo.min(),data.riesgo.max()), \
           (data.exigencia.min(),data.exigencia.max()),