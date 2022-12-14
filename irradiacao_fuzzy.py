# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:04:13 2022
@author: N.P.Saraiva

This script 

INSTRUÇÕES:
-> 
-> 
"""
import warnings
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

# parâmetro: razão de temperatura (T/T0) ######################################
# criando as variáveis do problema
t_t0 = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'razão de temperatura')

# criando as funções de pertinência
t_t0['baixa']       = fuzz.trimf(t_t0.universe, [0,0,0.25])
t_t0['baixa/media'] = fuzz.trimf(t_t0.universe, [0,0.25,0.5])
t_t0['media']       = fuzz.trimf(t_t0.universe, [0.25,0.5,0.75])
t_t0['media/alta']  = fuzz.trimf(t_t0.universe, [0.5,0.75,1])
t_t0['alta']        = fuzz.trimf(t_t0.universe, [0.75,1,1])

# vizualizando
t_t0.view()

# parâmetro: fração de horas de Sol possíveis (S/S0) ##########################
# criando as variáveis do problema
s_s0 = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'fração de horas de Sol')

# criando as funções de pertinência
s_s0['baixa']        = fuzz.trapmf(s_s0.universe, [0,0,0.1,0.2])
s_s0['baixa/normal'] = fuzz.trimf(s_s0.universe, [0.15,0.25,0.35])
s_s0['normal']       = fuzz.trapmf(s_s0.universe, [0.3,0.4,0.6,0.7])
s_s0['normal/alta']  = fuzz.trimf(s_s0.universe, [0.65,0.75,0.85])
s_s0['alta']         = fuzz.trapmf(s_s0.universe, [0.8,0.9,1,1])

# vizualizando
s_s0.view()

# parâmetro: índice de claridade (H/H0) #######################################
# criando as variáveis do problema
h_h0 = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'índice de claridade')

# criando as funções de pertinência
h_h0['baixo']       = fuzz.trimf(h_h0.universe, [0,0,0.25])
h_h0['baixo/medio'] = fuzz.trimf(h_h0.universe, [0,0.25,0.5])
h_h0['medio']       = fuzz.trimf(h_h0.universe, [0.25,0.5,0.75])
h_h0['medio/alto']  = fuzz.trimf(h_h0.universe, [0.5,0.75,1])
h_h0['alto']        = fuzz.trimf(h_h0.universe, [0.75,1,1])

# vizualizando
h_h0.view()

# Criando as regras de decisão fuzzy ##########################################
rule01 = ctrl.Rule(t_t0['baixa']       & s_s0['baixa'],        h_h0['baixo'])
rule02 = ctrl.Rule(t_t0['baixa']       & s_s0['baixa/normal'], h_h0['baixo/medio'])
rule03 = ctrl.Rule(t_t0['baixa']       & s_s0['normal'],       h_h0['medio'])
rule04 = ctrl.Rule(t_t0['baixa']       & s_s0['normal/alta'],  h_h0['medio/alto'])
rule05 = ctrl.Rule(t_t0['baixa']       & s_s0['alta'],         h_h0['medio/alto'])

rule06 = ctrl.Rule(t_t0['baixa/media'] & s_s0['baixa'],        h_h0['baixo'])
rule07 = ctrl.Rule(t_t0['baixa/media'] & s_s0['baixa/normal'], h_h0['baixo/medio'])
rule08 = ctrl.Rule(t_t0['baixa/media'] & s_s0['normal'],       h_h0['medio'])
rule09 = ctrl.Rule(t_t0['baixa/media'] & s_s0['normal/alta'],  h_h0['medio/alto'])
rule10 = ctrl.Rule(t_t0['baixa/media'] & s_s0['alta'],         h_h0['alto'])

rule11 = ctrl.Rule(t_t0['media']       & s_s0['baixa'],        h_h0['baixo/medio'])
rule12 = ctrl.Rule(t_t0['media']       & s_s0['baixa/normal'], h_h0['medio'])
rule13 = ctrl.Rule(t_t0['media']       & s_s0['normal'],       h_h0['medio/alto'])
rule14 = ctrl.Rule(t_t0['media']       & s_s0['normal/alta'],  h_h0['medio/alto'])
rule15 = ctrl.Rule(t_t0['media']       & s_s0['alta'],         h_h0['alto'])

rule16 = ctrl.Rule(t_t0['media/alta'] & s_s0['baixa'],        h_h0['baixo/medio'])
rule17 = ctrl.Rule(t_t0['media/alta'] & s_s0['baixa/normal'], h_h0['medio'])
rule18 = ctrl.Rule(t_t0['media/alta'] & s_s0['normal'],       h_h0['medio/alto'])
rule19 = ctrl.Rule(t_t0['media/alta'] & s_s0['normal/alta'],  h_h0['alto'])
rule20 = ctrl.Rule(t_t0['media/alta'] & s_s0['alta'],         h_h0['alto'])

rule21 = ctrl.Rule(t_t0['alta']       & s_s0['baixa'],        h_h0['medio'])
rule22 = ctrl.Rule(t_t0['alta']       & s_s0['baixa/normal'], h_h0['medio/alto'])
rule23 = ctrl.Rule(t_t0['alta']       & s_s0['normal'],       h_h0['medio/alto'])
rule24 = ctrl.Rule(t_t0['alta']       & s_s0['normal/alta'],  h_h0['alto'])
rule25 = ctrl.Rule(t_t0['alta']       & s_s0['alta'],         h_h0['alto'])

# criando e simulando um controlador fuzzy
h_h0_ctrl = ctrl.ControlSystem([rule01, rule02, rule03, rule04, rule05,\
    rule06, rule07, rule08, rule09, rule10, rule11, rule12, rule13, rule14,
    rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23,\
    rule24, rule25])

h_h0_simulador = ctrl.ControlSystemSimulation(h_h0_ctrl)

# entrando com alguns valores
h_h0_simulador.input['razão de temperatura'] = 0.863
h_h0_simulador.input['fração de horas de Sol'] = 0.445

# computando o resultado
h_h0_simulador.compute()
print(h_h0_simulador.output['índice de claridade'])

# mostrando graficamente o resultado
t_t0.view(sim=h_h0_simulador)
s_s0.view(sim=h_h0_simulador)
h_h0.view(sim=h_h0_simulador)
