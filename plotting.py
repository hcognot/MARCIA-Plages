import numpy as np
import matplotlib.pyplot as plt

"""Fonctions de tracé"""  
""" plotting of a (x, y) set of points with a label"""
def trace(x_data, y_data, texte) :
    plt.figure(figsize=(6, 4))
    plt.scatter(x_data, y_data, label=texte)
    plt.legend(loc='best')

""" Fonction de tracé : données initiales et courbe ajustée """ 
""" plotting of a (x, y) set of points alongside a function , with a label """   
def trace_ajuste(x_data, y_data, y_calc, texte) :
    plt.figure(figsize=(6, 4))
    plt.scatter(x_data, y_data, label=texte)
    plt.plot(x_data, y_calc)
    plt.legend(loc='best')