# OTTIMIZZA IL FIS 

def ottimizzaFIS(dati_modello,funzione_obiettivo, 
                       limiti_geni, metaparametri,nome_funzione_obiettivo, 
                       esecuzione):
    
    
    # importa la funzione che avvia il GA
    from GA.esegui_GA import esegui_GA
    # importa il modulo per passare variabili per valore 
    import copy
    
    # crea una copia dei dati delle MG per il GA
    copia_dati_MG=copy.deepcopy(dati_modello[1])


    # ottimizza il fis
    risultati_ottimizzazione=esegui_GA(funzione_obiettivo,
                                           limiti_geni, 
                                           metaparametri,
                                           nome_funzione_obiettivo, 
                                           esecuzione,
                                           dati_modello)
    
    
    
     
    return risultati_ottimizzazione
    


 







