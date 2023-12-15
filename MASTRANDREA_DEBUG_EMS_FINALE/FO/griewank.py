# Funzione di Griewank
def griewank(variabili):
    import math
    valore_FO= (variabili[0]**2/4000) + (variabili[1]**2/4000)-math.cos(variabili[0]/((2)**0.5)) * math.cos(variabili[1]/((2)**0.5)) + 1
    return valore_FO