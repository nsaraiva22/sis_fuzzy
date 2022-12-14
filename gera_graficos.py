# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 18:22:39 2022
@author: N.P.Saraiva

This script 

INSTRUÇÕES:
-> linha 20: inserir o caminho do arquivo a ser lido
-> linha 23: inserir o nome no arquivo a ser lido
-> 
"""

import warnings
import os
import unidecode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

PATH = 'E:/2022.02_sistemas_nebulosos/trabalho/dados_e_resultados'
os.chdir(PATH)

# escolhendo a cidade
cidade = 'Alto Parnaíba'
#cidade = 'Turiaçu'
local = unidecode.unidecode(cidade).lower().replace(' ', '_')

arquivo_1 = 'saida_' + local + '.csv'
arquivo_2 = 'razao_h_pre_' + local + '.csv'

df = pd.read_csv(arquivo_1, sep=',', encoding='unicode_escape')
razao_h_prev = pd.read_csv(arquivo_2, sep=',', encoding='unicode_escape')

df['razao_h_p'] = razao_h_prev

df['h_p'] = df['razao_h_p']*df['h_0']

df['h_p_a'] = df['razao_h_p']*(df['h_0']/1.5)

# calculo do coeficiente de correlação de pearson 
corr_p = np.corrcoef(df['h'], df['h_p'])
corr_p_a = np.corrcoef(df['h'], df['h_p_a'])

# gráfico de correlação
plt.rcParams['font.family'] = 'Times New Roman'

fig, axs = plt.subplots(1, 2, figsize=(9,4))
fig.suptitle('Correlação da irradiação [MJ/m².dia]' + ' - ' + cidade, size=14)

xticks = np.arange(int(df['h'].min()), int(df['h'].max())+1, 1)
yticks = np.arange(int(min(df['h_p'].min(), df['h_p_a'].min())),\
    int(max(df['h_p'].max(), df['h_p_a'].max()))+1, 2)

a0, b0 = np.polyfit(df['h'], df['h_p'], 1)
a1, b1 = np.polyfit(df['h'], df['h_p_a'], 1)

axs[0].scatter(df['h'], df['h_p'], s=80, c='seagreen', alpha=0.5)
axs[0].plot(df['h'], a0*df['h'] + b0, linewidth=1, color='firebrick')
axs[0].set_xlabel('Medida', size=12)
axs[0].set_ylabel('Prevista', size=12)
axs[0].set_xticks(xticks)
axs[0].set_yticks(yticks)
axs[0].text(df['h'].max()-2, df['h_p'].min()+1, 'r = %3f' %(corr_p[0,1]),\
    size=10, ha='left')

axs[1].scatter(df['h'], df['h_p_a'], s=80, c='seagreen', alpha=0.5)
axs[1].plot(df['h'], a1*df['h'] + b1, linewidth=1, color='firebrick')
axs[1].set_xlabel('Medida', size=12)
axs[1].set_ylabel('Prevista e Ajustada', size=12)
axs[1].set_xticks(xticks)
axs[1].set_yticks(yticks)
axs[1].text(df['h'].max()-2, df['h_p_a'].min()+1, 'r = %3f' %(corr_p_a[0,1]),\
    size=10, ha='left')

fig.savefig(local + '_correlacao.png', dpi=200)

fig.show()

# gráfico comparação
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(8,5))
fig.suptitle('Irradiação [MJ/m².dia]' + ' - ' + cidade, size=14)

ax.plot(df['mes'], df['h'], 'o', label='Medida')
ax.plot(df['mes'], df['h_p'], 'tomato', label='Prevista')
ax.plot(df['mes'], df['h_p_a'], 'lightsalmon', label='Prevista e Ajustada')
ax.legend(loc='upper left')

fig.savefig(local + '_comparacao.png', dpi=200)

fig.show()
