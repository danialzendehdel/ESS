# Classe che definisce l'ottimizzatore
class EMS:
    

    
    # inizializza l'oggetto 
    def __init__(self, funzione_obiettivo, limiti_variabili, 
                 algoritmo_di_ottimizzazione, metaparametri
                 ,nome_funzione_obiettivo,numero_esecuzioni):
        self.funzione_obiettivo=funzione_obiettivo
        self.limiti_variabili=limiti_variabili
        self.algoritmo_di_ottimizzazione=algoritmo_di_ottimizzazione
        self.metaparametri=metaparametri
        self.nome_funzione_obiettivo=nome_funzione_obiettivo
        self.numero_esecuzioni=numero_esecuzioni
        self.risultati=[]
        
    # esegue l'ottimizzazione  
    def esegui_ottimizzazione(self):
        # importa la funzione per calcolare la media
        from statistics import variance
        from statistics import mean
        # importa il pacchetto per salvare i file
        import os
        # se l'algoritmo di ottimizzazione è l'Algoritmo Genetico
        if self.algoritmo_di_ottimizzazione == "GA":
            # importa la funzione che esegue l'Algoritmo Genetico
            from GA.esegui_GA import esegui_GA
            # contempla più esecuzioni
            for esecuzione in range(1,self.numero_esecuzioni+1):
                print("Esecuzione numero: "+str(esecuzione))
                # esegue l'Algoritmo Genetico
                risultati_esecuzione=esegui_GA(self.funzione_obiettivo, 
                                         self.limiti_variabili, self.metaparametri
                                         ,self.nome_funzione_obiettivo, esecuzione)
                self.risultati=self.risultati+[risultati_esecuzione]
            # calcola medie, varianze dei risultati, tempo impiegato e li salva
            valori_best_FO=[]
            soluzioni=[]
            tempi_esecuzione=[]
            for esecuzione in range(self.numero_esecuzioni):
                risultati_esecuzione=self.risultati[esecuzione]
                valore_best_FO=risultati_esecuzione[0][1]
                soluzione=risultati_esecuzione[0][2][0]
                tempo_esecuzione=risultati_esecuzione[1]
                valori_best_FO=valori_best_FO+valore_best_FO
                soluzioni=soluzioni+[soluzione]
                tempi_esecuzione=tempi_esecuzione+[tempo_esecuzione]
            media_best_FO=mean(valori_best_FO)
            varianza_best_FO=variance(valori_best_FO)
            media_tempi_esecuzione=mean(tempi_esecuzione)
            numero_variabili=len(self.limiti_variabili[0])
            medie_soluzioni=[]
            varianze_soluzioni=[]
            for gene in range(numero_variabili):
                geni_parziali=[]
                for row in soluzioni:
                    geni_parziali=geni_parziali+[row[gene]]
                medie_soluzioni=medie_soluzioni+[mean(geni_parziali)]
                varianze_soluzioni=varianze_soluzioni+[variance(geni_parziali)]   
            tempo_totale=sum(tempi_esecuzione)
            risultati_ordinati=[media_best_FO,varianza_best_FO,
                                medie_soluzioni,varianze_soluzioni,tempo_totale,[self.numero_esecuzioni]]
            file_path = os.path.join("./GA/Risultati"
                                     ,"risultati_finali_"+self.nome_funzione_obiettivo+".txt")
            with open(file_path, "w") as file:
                file.write(str(risultati_ordinati))
            print(str(medie_soluzioni))
        # se l'algoritmo di ottimizzazione è di altro tipo
        else:
            print("Non ci sono altri algoritmi implementati!")

 