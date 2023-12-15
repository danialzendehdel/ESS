# Funzione che esegue la selection di tipo 'tournament'

def selection (popolazione, dimensione_torneo, dimensioni_popolazione,
               numero_geni, numero_random_1):
        
    # sceglie casualmente l'indice il primo individuo partecipante al torneo
    indice_primo_individuo_torneo= round(0+numero_random_1*(dimensioni_popolazione-dimensione_torneo))


    # a partire dall'indice scelto, prende gli altri partecipanti
    individui_partecipanti=[[0]*(numero_geni+1) for _ in 
                            range(dimensione_torneo)]
    i=0
    for indice_partecipante in range(
            indice_primo_individuo_torneo,indice_primo_individuo_torneo+
            dimensione_torneo):
        individuo_partecipante=popolazione[indice_partecipante]
        individui_partecipanti[i]=individuo_partecipante
        i=i+1
    
    # trova l'individuo vincitore del torneo
    indice_FO=numero_geni
    individui_partecipanti = sorted(individui_partecipanti, 
                                    key=lambda x: x[indice_FO])
    individuo_vincitore=individui_partecipanti[0]
    return individuo_vincitore

