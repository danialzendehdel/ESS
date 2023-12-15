# Funzione che esegue la mutation 'uniform'

def mutation(individui_da_mutare,numero_geni,prob_mutazione, limiti_geni
             ,decadimento_mutazione, generazione, numero_individui_mutation):
    
    import numpy as np
    import math
    
    individui_mutati=[[0]*(numero_geni+1) for _ in range(numero_individui_mutation)]
    
    for indice_individuo in range(len(individui_da_mutare)):
        individuo_mutato=[0]*(numero_geni+1)
        for indice_gene in range(numero_geni):
            limite_inferiore_gene=limiti_geni[0][indice_gene]
            limite_superiore_gene=limiti_geni[1][indice_gene]
            massimo_delta_superiore=limite_superiore_gene-individui_da_mutare[indice_individuo][indice_gene]
            massimo_delta_inferiore=individui_da_mutare[indice_individuo][indice_gene]-limite_inferiore_gene
            k=np.random.random()
            delta=0
            if k<=prob_mutazione:
                numero_random_3=round(np.random.random(),2)
                if numero_random_3>=0 and numero_random_3<=0.5:
                    delta=massimo_delta_superiore-(numero_random_3/0.5)*massimo_delta_superiore
                if numero_random_3>=0.51 and numero_random_3<=1:
                    delta=-massimo_delta_inferiore*(numero_random_3-0.5)/0.5
            individuo_mutato[indice_gene]=individui_da_mutare[indice_individuo][indice_gene]+delta*decadimento_mutazione           
            individui_mutati[indice_individuo] = individuo_mutato
    return individui_mutati
            
        
    