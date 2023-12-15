# Funzione di Schwefel
def schwefel(variabili):
    import math
    valore_FO=418.9829*2 - (variabili[0] * math.sin((abs(variabili[0]))**0.5) +
                            variabili[1] * math.sin((abs(variabili[1]))**0.5))
    return valore_FO