#2da. Librería
#María Gabriela Ramírez Castillo
# Fecha: 26 de noviembre de 2025

import pandas as pd
import numpy as np
import string
import seaborn as sns
from collections import Counter
from matplotlib import pyplot as plt
from scipy.stats import zscore
from scipy.stats import median_abs_deviation
from pyod.models.mad import MAD
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN


class HyAIA3:
    def __init__(self, df):
        self.data = df
        self.column = df.column
        self.df_M_IQR = self.MetodoIQR()
        self.df_M_StD = self.Metodo_StDev()
        self.df_M_ZSC = self.Metodo_Z_score()
        self.df_M_ZSCM = self.Metodo_Z_ScoreMod()

    
#***************************************************************************************************************    
    #Creación de la función para obtener los outliers por el metodo IQR
    def MetodoIQR (df,n,features):
        outlier_list = []
    
        for column in features:
            # 1st quartile (25%)
            Q1 = np.percentile(df[column], 25)
            # 3er quartile (75%)
            Q3 = np.percentile(df[column], 75)
    
            #Calcular el IQR
            IQR = Q3-Q1
            
            outlier_limit = 1.5*IQR    
            #Limimite inferior de iqr
            Li = Q1-outlier_limit
            #Limimite superior de iqr
            Ls = Q3+outlier_limit
    
            #determinar la lista de outliers
            outlier_list_column = df[(df[column] < Li) | (df[column] > Ls)].index
            #Agregar a lista de outliers
            outlier_list.extend(outlier_list_column)
    
        #Seleccionar las observaciones que contienen más de cierto nuymero de outliers
        outlier_list = Counter(outlier_list)
        print(outlier_list)
        multiple_outliers = list(k for k,v in outlier_list.items() if v>=n)
        
        return multiple_outliers
        
#***************************************************************************************************************
    
    def Metodo_StDev(df,n,features):
        outlier_indices = []
        for column in features:
            #Calculamos la media y la desviacion estandar de todo el dataframe
            data_mean = df[column].mean()
            data_std = df[column].std()
    
            #Calculando el corte de la desviacion estandar
            cut_off = 3*data_std
            #Determinamos los indices de los outliers
            outlier_list_column = df[(df[column] < data_mean - cut_off) | (df[column] > data_mean + cut_off)].index
            #Agregamnos los indices de los outliers obtenidos
            outlier_indices.extend(outlier_list_column)
    
        #Seleccionamos las observaciones que continenen mas de ciertos nums de outliers
        outlier_ind = Counter(outlier_indices)
        multiple_outliers = list(k for k,v in outlier_ind.items() if v>=n)
        return multiple_outliers

#***************************************************************************************************************

    # Agregar a nuestra librería
    def Metodo_Z_score (df,n,features):
        outlier_list = []
        for column in features:
            #Calculamos la media y la desviacion estandar de todo el dataframe
            data_mean = df[column].mean()
            data_std = df[column].std()
            threshold = 3
            
            #Calculando el z_score
            z_score = abs((df[column]-data_mean)/data_std)
            
            #Determinamos los indices de los outliers
            outlier_list_column = df[z_score > threshold].index
            #Agregamnos los indices de los outliers obtenidos
            outlier_list.extend(outlier_list_column)
    
        #Seleccionamos las observaciones que continenen mas de ciertos nums de outliers
        outlier_list = Counter(outlier_list)
        multiple_outliers = list(k for k,v in outlier_list.items() if v>=n)
        return multiple_outliers

#**************************************************************************************************************

    def Metodo_Z_ScoreMod (df,n,features): #Agregar a nuestra librería
        outlier_list = []
        for column in features:
            #Calculamos la media y la desviacion estandar de todo el dataframe
            data_median = df[column].median()
            data_std = df[column].std()
            threshold = 3
            
            #Calculando el mad z_score
            MAD = median_abs_deviation
            
            z_score = abs(0.6745*(df[column]-data_median)/MAD(df[column]))
            
            #Determinamos los indices de los outliers
            outlier_list_column = df[z_score > threshold].index
            #Agregamnos los indices de los outliers obtenidos
            outlier_list.extend(outlier_list_column)
    
        #Seleccionamos las observaciones que continenen mas de ciertos nums de outliers
        outlier_list = Counter(outlier_list)
        multiple_outliers = list(k for k,v in outlier_list.items() if v>=n)
        return multiple_outliers

#*************************************************************************************************************

