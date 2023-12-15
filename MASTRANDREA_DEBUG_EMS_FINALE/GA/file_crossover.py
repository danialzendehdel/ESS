# Funzione che esegue il crossover di tipo 'convex'

def crossover(individui_crossover,numero_geni, numero_individui_crossover,numero_casuale_2):
    
    
    
    individui_figli=[[0]*(numero_geni+1) for _ in range(
        numero_individui_crossover)]     
    for contatore_individui in range(0,numero_individui_crossover-1):
        primo_genitore=individui_crossover[contatore_individui]
        secondo_genitore=individui_crossover[contatore_individui+1]
        primo_figlio=[0]*(numero_geni+1)
        secondo_figlio=[0]*(numero_geni+1)
        for indice_geni in range(numero_geni):      
            primo_figlio[indice_geni]=numero_casuale_2*primo_genitore[indice_geni]+(1-numero_casuale_2)*secondo_genitore[indice_geni]
            secondo_figlio[indice_geni]=numero_casuale_2*secondo_genitore[indice_geni]+(1-numero_casuale_2)*primo_genitore[indice_geni]
        primo_figlio[numero_geni]=0   # azzera la FO
        secondo_figlio[numero_geni]=0 # azzera la FO
        individui_figli[contatore_individui]=primo_figlio
        individui_figli[contatore_individui+1]=secondo_figlio
    return individui_figli
        
    