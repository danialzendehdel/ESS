# Calcola la FO per ogni individuo della popolazione

def calcola_FO_popolazione(funzione_obiettivo,copia_popolazione,
                           dati_modello):

    if funzione_obiettivo == 'globale':
        from FO.globale import globale
        # importa il modulo per passare variabili per valore 
        import copy
        import concurrent.futures
        from functools import partial
        import itertools
        import concurrent.futures
        from functools import partial
        import os
        
        # senza parallelizzazione
        # valori_FO=[]
        # for indice_individuo in range(len(copia_popolazione)):
        #     individuo=copia_popolazione[indice_individuo]
        #     copia_dati_modello=copy.deepcopy(dati_modello)
        #     fo=globale(individuo,copia_dati_modello)
        #     valori_FO=valori_FO+[fo]
        # return valori_FO
        
        

        # con parallelizzazione
        # NOTA IMPORTANTE:
        # CON PARALLELIZZAZIONE, DATI_MODELLO E INDIVIDUO NELLA 
        # FUNZIONE OBIETTIVO, DEVONO ESSERE SCAMBIATI DI POSTO QUANTO
        # VENGONO PASSATI AD ESSA COME ARGOMENTI
        valori_FO=[]
        curried_function=partial(funzione_obiettivo, dati_modello)
        # Creazione di un pool di thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            
            # Esecuzione parallela dei task
            risultati = list(executor.map(curried_function, copia_popolazione))

            # Stampa dei risultati
            for risultato in risultati:
                valori_FO=valori_FO+[risultato]
        return valori_FO 
    
    elif funzione_obiettivo == 'ECM':
        from FO.modello_ECM import modello_ECM
        # importa il modulo per passare variabili per valore 
        import copy
        
        # test singolo individuo senza parallelizzazione
        valori_FO=[]
        for indice_individuo in range(len(copia_popolazione)):
            individuo=copia_popolazione[indice_individuo]
            
            fo=modello_ECM(individuo,dati_modello)
            valori_FO=valori_FO+[fo]
        return valori_FO
    
    elif funzione_obiettivo == 'ECM_batch':
        from FO.modello_ECM import modello_ECM_batch
        import copy
        valori_FO=[]
        for indice_individuo in range(len(copia_popolazione)):
            individuo=copia_popolazione[indice_individuo]
            
            fo=modello_ECM_batch(individuo,dati_modello)
            valori_FO=valori_FO+[fo]
        return valori_FO



            
            