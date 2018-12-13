"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

#Objetivos agrupados
matriz_rw = np.load("rwa-oa")
matriz_lf = np.load("lfa-oa")
matriz_o2e = np.load("o2e-oa")
