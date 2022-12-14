# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 12:40:52 2022
@author: N.P.Saraiva

Este script calcula as razões T/T0, S/S0 e H/H0

INSTRUÇÕES:
-> linha 21: inserir o caminho do arquivo a ser lido
-> linha 24: inserir o nome no arquivo a ser lido
-> linha 29: inerir a latitude da cidade
"""

import warnings
import os
import pandas as pd
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

PATH = 'E:/2022.02_sistemas_nebulosos/trabalho/dados_e_resultados'
os.chdir(PATH)

arquivo = 'turiacu.csv'

df = pd.read_csv(arquivo, sep=',', encoding='unicode_escape')

# latitude (φ) [°]
phi = -1.67

# constante solar (Gsc) [W/m²]
g_sc = 1367

# declinação (δ) [°]
df['delta'] = 23.45*np.sin(np.radians(360*((284+df['dia_j'])/365)))

# ângulo horário do pôr do sol ou nascer do sol (ωs) [°]
df['omega_s'] = np.degrees(np.arccos(-np.tan(np.radians(phi))*\
    np.tan(np.radians(df['delta']))))

# radiação extraterrestre diária em uma superfície horizontal (H0) [MJ/m²]
df['h_0'] = ((24*3600*g_sc/np.pi)*(1+0.033*np.cos(360*df['dia_j']/365))*\
    ((np.cos(np.radians(phi))*np.cos(np.radians(df['delta']))*\
    np.sin(np.radians(df['omega_s'])))+((np.pi*df['omega_s']/180)*\
    np.sin(np.radians(phi))*np.sin(np.radians(df['delta'])))))/10**6

# horas diárias médias mensais de sol brilhante (S0)
df['s_0'] = (2/15)*df['omega_s']
                                        
# razão da temperatura (T/T0)
df['razao_t'] = df['t_ar']/df['t_max']

# fração média de horas de sol possíveis (S/S0)
df['razao_s'] = df['s']/df['s_0']

# índice de claridade (H/H0)
df['razao_h'] = df['h']/df['h_0']

# salva arquivo
df.to_csv('saida_'+arquivo, index=False)
