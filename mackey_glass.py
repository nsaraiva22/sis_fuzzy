# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:43:30 2022
@author: N.P.Saraiva

Este script utiliza fuzz para a previsão de series temprais.

Série temporal caótica de Mackey-Glass

INSTRUÇÕES:
-> linha 25: inserir o caminho onde os arquivos serão armazenados 
"""

import warnings
import os
from pyFTS.data import mackey_glass
from pyFTS.partitioners import Grid
from pyFTS.models import chen
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)

PATH = 'C:/Users/nsara/Documents/natalia_doutorado_ufma/periodos/2022.2/2022.02_sistemas_nebulosos/trabalho_capitulo'
os.chdir(PATH)

# gerando os valores de treinamento
train = mackey_glass.get_data(b=0.1, c=0.2, tau=30,\
    initial_values=np.linspace(0.5, 1.5, 18), iterations=600)

# gerando os valores de teste
test = mackey_glass.get_data(b=0.1, c=0.2, tau=30,\
    initial_values=np.linspace(0.5, 1.5, 18), iterations=300)

# plotando o grafico de treinamento
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10,5])
fig.suptitle('Seção da série temporal caótica de Mack-Glass', size=14)

ax.plot(train, 'navy')

fig.savefig('mackey_glass.png', dpi=200)

fig.show()

# universo de discurso
partitioner_1 = Grid.GridPartitioner(data=train, npart=7)
partitioner_2 = Grid.GridPartitioner(data=train, npart=15)

# cria um modelo vazio usando o método Chen(1996)
model_1 = chen.ConventionalFTS(partitioner=partitioner_1)
model_2 = chen.ConventionalFTS(partitioner=partitioner_2)

# o procedimento de treinamento é realizado pelo método fit
model_1.fit(train)
model_2.fit(train)

# refras do modelo
print(model_1)
print(model_2)

# o procedimento de previsão é realizado pelo método "prever"
forecasts_1 = model_1.predict(test)
forecasts_2 = model_2.predict(test)

# plotando o grafico de resultados
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[6,5])
fig.suptitle('Seção da série temporal caótica de Mack-Glass - Previstos', size=14)

ax.plot(test, 'navy', label='Dado original')
ax.plot(forecasts_1, 'goldenrod', label='Previsto (7 conjuntos fuzzy)')
ax.plot(forecasts_2, 'indianred', label='Previsto (15 conjuntos fuzzy)')
ax.legend(loc='lower right')

fig.savefig('mackey_glass_result.png', dpi=200)

fig.show()

# salvando os resultados
df = pd.DataFrame({'teste':test, 'prev_1':forecasts_1, 'prev_2':forecasts_2})
df.to_csv('mackey_glass_data.csv', index=False)

# calculo do coeficiente de correlação de pearson 
corr_1 = np.corrcoef(df['teste'], df['prev_1'])
corr_2 = np.corrcoef(df['teste'], df['prev_2'])

# gráfico de correlação
plt.rcParams['font.family'] = 'Times New Roman'

fig, axs = plt.subplots(1, 2, figsize=(9,4))
fig.suptitle('Correlação da série temporal caótica de Mack-Glass x Prevista'\
    , size=14)

a1, b1 = np.polyfit(df['teste'], df['prev_1'], 1)
a2, b2 = np.polyfit(df['teste'], df['prev_2'], 1)

axs[0].scatter(df['teste'], df['prev_1'], s=80, c='seagreen', alpha=0.5)
axs[0].plot(df['teste'], a1*df['teste'] + b1, linewidth=1, color='firebrick')
axs[0].set_title('7 conjuntos fuzzy', size=12)
axs[0].set_xlabel('Original', size=12)
axs[0].set_ylabel('Prevista', size=12)
axs[0].text(1, 0.4, 'r = %3f' %(corr_1[0,1]), size=10, ha='left')

axs[1].scatter(df['teste'], df['prev_2'], s=80, c='seagreen', alpha=0.5)
axs[1].plot(df['teste'], a1*df['teste'] + b1, linewidth=1, color='firebrick')
axs[1].set_title('15 conjuntos fuzzy', size=12)
axs[1].set_xlabel('Original', size=12)
axs[1].set_ylabel('Prevista', size=12)
axs[1].text(1, 0.4, 'r = %3f' %(corr_2[0,1]), size=10, ha='left')

fig.savefig('mackey_glass_correlacao.png', dpi=200)

fig.show()
