

# Funzione che esegue l'Algoritmo Genetico 
def esegui_GA_debug(funzione_obiettivo, limiti_geni, metaparametri
              ,nome_funzione_obiettivo,esecuzione,dati_modello,best_individuo_past_gen=[]):
    
    # importa le funzioni degli operatori
    from GA.file_selection import selection
    from GA.file_crossover import crossover
    from GA.file_mutation import mutation
    # importa la funzione che calcola la FO per tutta la popolazione
    from GA.file_calcola_FO_popolazione import calcola_FO_popolazione
    # importa le funzioni per i salvataggi
    from GA.file_salva_risultati import salva_risultati
    from GA.file_salva_popolazione import salva_popolazione
    from GA.file_plotta_risultati import plotta_risultati
    # importa la funzione per la misura del tempo di esecuzione
    import time
    # importa la funzione per calcolare la media
    from statistics import mean
    # importa il modulo per generare numeri pseudocasuali
    import random
    # importa il modulo per passare variabili per valore 
    import copy
    # importa il modulo per plottare i grafici
    import matplotlib.pyplot as plt
    # DEBUG (stesso seed di matlab=rng(1337))
    import numpy as np
    from tqdm import tqdm
    np.random.seed(1337)
    # misura l'istante iniziale
    start_time=time.time()
    
    # estrae informazioni dagli input
    dimensioni_popolazione=metaparametri[0]
    numero_geni=len(limiti_geni[0])
    crossover_fraction=metaparametri[1]
    prob_mutazione=metaparametri[2]
    attenuazione_mutazione=metaparametri[3]
    stopping_condition=metaparametri[4]
    max_gen=metaparametri[5]
    max_stall=metaparametri[6]
    tolleranza=metaparametri[7]
    numero_individui_elite=metaparametri[8]
    dimensione_torneo=metaparametri[9]
    frazione_figli_da_mutare=metaparametri[10]
    numero_individui_crossover=round(crossover_fraction*dimensioni_popolazione)
    numero_individui_mutation=dimensioni_popolazione-numero_individui_elite-numero_individui_crossover
    
    # genera la popolazione iniziale vuota e dichiara/inizializza alcune variabili  
    # (l'ultimo vettore contiene i valori di FO che, per ora, sono nulli)
    popolazione=[[0]*(numero_geni+1) for _ in range(dimensioni_popolazione)]
    best_FO=[]
    media_FO=[]
    indice_FO=numero_geni
    if (funzione_obiettivo == 'ECM' or funzione_obiettivo == 'ECM_batch') and best_individuo_past_gen:
        for indice_individuo in range(dimensioni_popolazione):
            popolazione[indice_individuo][:] = best_individuo_past_gen

        for indice_individuo in range((dimensioni_popolazione-1),dimensioni_popolazione):
            for indice_gene in range(numero_geni):
                limite_inferiore_gene=limiti_geni[0][indice_gene]
                limite_superiore_gene=limiti_geni[1][indice_gene]
                numero_random=np.random.random()
                allele=limite_inferiore_gene+numero_random*(limite_superiore_gene-limite_inferiore_gene)
                popolazione[indice_individuo][indice_gene]=allele
            indice_individuo=0
    else:
        # genera la prima popolazione con alleli pseudocasuali
        for indice_individuo in range(dimensioni_popolazione):
            for indice_gene in range(numero_geni):
                limite_inferiore_gene=limiti_geni[0][indice_gene]
                limite_superiore_gene=limiti_geni[1][indice_gene]
                numero_random=np.random.random()
                allele=limite_inferiore_gene+numero_random*(limite_superiore_gene-limite_inferiore_gene)
                popolazione[indice_individuo][indice_gene]=allele
            indice_individuo=0
    


            
    # inizia il ciclo delle generazioni
    for generazione in (range(max_gen)):
        
        #print('Gen:   '+str(generazione))
        
        # calcola il decadimento della mutazione
        decadimento_mutazione=(1-generazione/max_gen)**attenuazione_mutazione
        

        # calcola il valore della FO per la popolazione
        copia_popolazione_per_FO=copy.deepcopy(popolazione)
        fo=calcola_FO_popolazione(funzione_obiettivo,copia_popolazione_per_FO,
                                   dati_modello)
        trasposta_popolazione=[[fila[i] for fila in copia_popolazione_per_FO] for i 
                               in range(len(copia_popolazione_per_FO[0]))]
        trasposta_popolazione[len(trasposta_popolazione)-1]=fo 
        popolazione=[[fila[i] for fila in trasposta_popolazione] for i 
                 in range(len(trasposta_popolazione[0]))]

            
        # ordina la popolazione per valori di FO crescenti
        copia_popolazione_per_ordinamento=copy.deepcopy(popolazione)
        popolazione_ordinata = sorted(copia_popolazione_per_ordinamento, key=lambda x: x[indice_FO])
        
        # pesca il miglior individuo e il suo valore della FO per le generazione corrente
        best_FO_corrente=min([row[numero_geni] for row in popolazione])
        
        media_FO_corrente=mean([row[numero_geni] for row in popolazione])
        best_FO=best_FO+[best_FO_corrente]
        media_FO=media_FO+[media_FO_corrente]
        miglior_individuo_corrente=[]
        for row in popolazione:
            if row[numero_geni] == best_FO_corrente:
                miglior_individuo_corrente=row
        
        # resa grafica
        # fig = plt.figure()
        # plt.title("Best-mean FO"+"-"+nome_funzione_obiettivo+"-Esec. "+str(esecuzione)
        #           +"\n"+"Best = "+str(round(best_FO_corrente,3)))
        # plt.plot(best_FO, 'k*', label="best")
        # plt.plot(media_FO,'b+',label="mean")
        # plt.xlabel('gen')           
        # plt.ylabel('FO')
        # plt.legend()
        # plt.draw()
        # plt.show()
        
        # controlla la stopping contidion "max_stall"
        risultati=[]
        
        if stopping_condition == "FO_thresh":  
            if best_FO_corrente < tolleranza:
                risultati =[best_FO_corrente,miglior_individuo_corrente[0:len(miglior_individuo_corrente)-1],generazione,stopping_condition]
                return risultati
            if generazione == max_gen-1 and best_FO_corrente > tolleranza:
                risultati =[best_FO_corrente,miglior_individuo_corrente[0:len(miglior_individuo_corrente)-1],generazione,stopping_condition]
                print('max gen-raggiunta')
                return risultati
            
        if stopping_condition=="max_stall":
            l=len(best_FO)
            if l>=50:
                ultime_best_FO=best_FO[l-50:l]
                differenze_parziali=[]
                for indice_best_FO in range(len(ultime_best_FO)-1):
                    differenza_parziale=abs(ultime_best_FO[indice_best_FO]-ultime_best_FO[indice_best_FO+1])
                    differenze_parziali=differenze_parziali+[differenza_parziale]
                if mean(differenze_parziali)<=tolleranza:
                    risultati=[[nome_funzione_obiettivo],[best_FO_corrente],[miglior_individuo_corrente[0:len(miglior_individuo_corrente)-1]],[generazione]
                               ,[stopping_condition]]
                    # salva i risultati
                    salva_risultati(risultati,esecuzione, nome_funzione_obiettivo)
                    # plotta e salva le figure
                    plotta_risultati(best_FO,media_FO, nome_funzione_obiettivo,esecuzione, best_FO_corrente)
                    # misura il tempo di esecuzione [s]
                    end_time=time.time()
                    tempo_esecuzione=end_time-start_time
                    # restituisce la FO del miglior individuo in assoluto (la soluzione)
                    soluzione=[risultati]+[tempo_esecuzione]
                    
                    fig = plt.figure()
                    plt.title("Best-mean FO"+"-"+nome_funzione_obiettivo+"-Esec. "+str(esecuzione)
                              +"\n"+"Best = "+str(round(best_FO_corrente,3)))
                    plt.plot(best_FO, 'k*', label="best")
                    plt.plot(media_FO,'b+',label="mean")
                    plt.xlabel('gen')           
                    plt.ylabel('FO')
                    plt.legend()
                    plt.draw()
                    plt.show()
                    plt.savefig('best-mean.eps',format='eps')
                    
                    
                    return soluzione
        # controlla la stopping condition "max_gen"
        if stopping_condition=="max_gen":
            if generazione==max_gen-1:
                risultati=[[nome_funzione_obiettivo],[best_FO_corrente],[miglior_individuo_corrente[0:len(miglior_individuo_corrente)-1]],[generazione]
                           ,[stopping_condition]]
                # salva i risultati
                salva_risultati(risultati,esecuzione,nome_funzione_obiettivo)
                # plotta e salva le figure
                plotta_risultati(best_FO,media_FO, nome_funzione_obiettivo,esecuzione, best_FO_corrente)
                # misura il tempo di esecuzione [s]
                end_time=time.time()
                tempo_esecuzione=end_time-start_time
                # restituisce la FO del miglior individuo in assoluto (la soluzione)
                soluzione=[risultati]+[tempo_esecuzione]
                
                fig = plt.figure()
                plt.title("Best-mean FO"+"-"+nome_funzione_obiettivo+"-Esec. "+str(esecuzione)
                          +"\n"+"Best = "+str(round(best_FO_corrente,3)))
                plt.plot(best_FO, 'k*', label="best")
                plt.plot(media_FO,'b+',label="mean")
                plt.xlabel('gen')           
                plt.ylabel('FO')
                plt.legend()
                plt.draw()
                plt.show()
                plt.savefig('best-mean.eps',format='eps')
                
                return soluzione
        
        # trova gli individui di elite 
        copia_popolazione_per_elitismo=copy.deepcopy(popolazione_ordinata)
        individui_elite=[[0]*(numero_geni+1) for _ in 
                         range(numero_individui_elite)]
        for indice_individuo_elite in range(numero_individui_elite):
            individuo_elite=copia_popolazione_per_elitismo[indice_individuo_elite]
            individui_elite[indice_individuo_elite]=individuo_elite
            
        # effettua la selection nella popolazione non ordinata
        copia_popolazione_per_selection=copy.deepcopy(popolazione)
        individui_crossover=[[0]*(numero_geni+1) for _ in range(numero_individui_crossover)]
        for contatore_individui_selezionati in range(numero_individui_crossover):
            numero_random_1=np.random.random()
            individuo_selezionato=selection(copia_popolazione_per_selection,dimensione_torneo,dimensioni_popolazione,numero_geni,numero_random_1)
            individui_crossover[contatore_individui_selezionati]=individuo_selezionato
            
        # sceglie gli individui da mutare nella popolazione non ordinata
        copia_popolazione_per_selezione_mutanti=copy.deepcopy(popolazione)
        individui_da_mutare=[[0]*(numero_geni+1) for _ in range(numero_individui_mutation)]
        indice_individuo_da_mutare=int(numero_individui_elite+numero_individui_crossover*(1-frazione_figli_da_mutare))
        for indice_individui_mutation in range(numero_individui_mutation):
            individuo_da_mutare=copia_popolazione_per_selezione_mutanti[indice_individuo_da_mutare]
            individui_da_mutare[indice_individui_mutation]=individuo_da_mutare
            indice_individuo_da_mutare=indice_individuo_da_mutare+1

        # azzera a FO di tutti gli individui da incrociare e mutare (non considera quelli di elite)
        for riga_crossover in  individui_crossover :
            riga_crossover[numero_geni]=0
        for riga_mutation in  individui_da_mutare :
            riga_mutation[numero_geni]=0
            
        # effettua il crossover
        numero_casuale_2=np.random.random()
        individui_figli=crossover(individui_crossover,numero_geni,numero_individui_crossover, numero_casuale_2)
        
        # effettua la mutation
        individui_mutati=mutation(individui_da_mutare,numero_geni,prob_mutazione, limiti_geni, decadimento_mutazione,generazione, numero_individui_mutation)
       
        # compone la nuova popolazione 
        nuova_popolazione=[miglior_individuo_corrente for i in individui_elite]+individui_figli+individui_mutati
        
        # controlla che gli alleli rispettino i limiti
        for indice_individuo in range(0,len(nuova_popolazione)):
            for indice_gene in range(0,len(nuova_popolazione[indice_individuo])-1):
                allele=nuova_popolazione[indice_individuo][indice_gene]
                limite_inferiore=limiti_geni[0][indice_gene]
                limite_superiore=limiti_geni[1][indice_gene]
                if allele<limite_inferiore :
                    allele = limite_inferiore
                    #print('Allele posto a lim INFERIORE')
                if allele >limite_superiore:
                    allele = limite_superiore
                    #print('Allele posto a lim SUPERIORE')
                
              
                
        # salva la popolazione per la generazione corrente (per backup)
        # salva_popolazione(generazione,popolazione)
        #print("Fine generazione "+str(generazione))
        
        #a ggiorna la popolazione
        print(best_FO_corrente)
        popolazione=nuova_popolazione
        

    

