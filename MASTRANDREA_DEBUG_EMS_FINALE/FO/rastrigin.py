# Funzione di Rastrigin
def rastrigin(variabili):
    import math
    valore_FO=20+variabili[0]**2+variabili[1]**2-10*(math.cos(2*math.pi*variabili[0]) + math.cos(2*math.pi*variabili[1]))
    return valore_FO