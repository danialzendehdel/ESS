# MAIN

# importa il pacchetto json 
import json
# importa la classe Ottimizzatore
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
folder_ottimizzatore_path = os.path.join(current_dir, 'EMS')
sys.path.append(folder_ottimizzatore_path)
from EMS.file_classe_EMS import EMS
from EMS.file_ottimizza_FIS import ottimizzaFIS
# importa la classe della microgride2
from MG.file_classe_microgrid import MG
# importa il modulo per generare numeri random
import numpy as np
np.random.seed(1337)
# importa il modulo per plottare
import matplotlib.pyplot as plt
# importa il modulo per calcoalre il fis ottimizzato
from FO.globale_fine_ottimizzazione import globale_fine_ottimizzazione




# SIMULAZIONE INTERNA PER AUTOCONSUMO

# parametri comuni a tutte le microgrid
PR_3=150  # prezzo dell'energia per il ritiro dedicato [€/MWh]
TRAS_e=7.61  # tariffa di trasmissione definita per le utenze in bassa tensione [€/MWh]
max_BTAU_m=0.61  # valore maggiore della componente variabile di distribuzione [€/MWh]
CPR=0.026  # coefficiente delle perdite di rete evitate [-]
Pz=3.2  # prezzo zonale orario [€/MWh]
PR_3=150  # prezzo dell'energia per il ritiro dedicato [€/MWh]



# microgrid 1
is_CER=1
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.5
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=10  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_1=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 2
is_CER=1
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.2
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=25  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_2=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 3
is_CER=1
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.6
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=15  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_3=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 3
is_CER=1
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.8
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=8  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_4=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 5
is_CER=0
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.9
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=9  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_5=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 6
is_CER=1
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=1
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=5  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_6=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)

# microgrid 7
is_CER=0
TP_CE=110 # tariffa premio [€/MWh]: 110, se si tratta di una CER; 100, se si tratta di un AUC
P_G_predetta=4
P_L_predetta=1
SoC_0=0.15
eta=0.94  # rendimento della batteria
SoC_min=0.15  # Stato di Carica minimo della batteria 
SoC_max=0.95  # Stato di Carica massimo della batteria
Q=7  # Capacità della batteria [kWh]
P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
B=18873  # prezzo della batteria [€]
a=1589  # parametro della curva cicli/DoD della batteria
b=1.428  # parametro della curva cicli/DoD della batteria
u=842.71 # costo unitario batteria [€/kWh]
MG_7=MG(is_CER, SoC_0, Q, P_S_max,eta, SoC_min,SoC_max,PR_3,B,a,b,CPR,
             Pz,TP_CE, TRAS_e, max_BTAU_m,u,SoC_0)



# LEGGE I METADATI PER L'OTTIMIZZAZIONE
with open("meta-dati.json") as file:
    file_meta_dati=json.load(file)
nome_funzione_obiettivo=file_meta_dati["FO"]
limiti_variabili=[]
metaparametri=[]
funzione_obiettivo=None
numero_esecuzioni=file_meta_dati["numero_esecuzioni"]
if nome_funzione_obiettivo=="globale":
    from FO.globale import globale
    funzione_obiettivo=globale
    limiti_variabili=file_meta_dati["limiti_variabili_globale"]
if nome_funzione_obiettivo=="modello_CER_AUC":
    from FO.modello_CER_AUC import modello_CER_AUC
    funzione_obiettivo=modello_CER_AUC
    limiti_variabili=file_meta_dati["limiti_variabili_CER_AUC"]
if nome_funzione_obiettivo=="rastrigin":
    from FO.rastrigin import rastrigin
    funzione_obiettivo=rastrigin
    limiti_variabili=file_meta_dati["limiti_variabili_rastrigin"]
    algoritmo_di_ottimizzazione=file_meta_dati["algoritmo_di_ottimizzazione"]
if nome_funzione_obiettivo=="rosenbrock":
    from FO.rosenbrock import rosenbrock
    funzione_obiettivo=rosenbrock
    limiti_variabili=file_meta_dati["limiti_variabili_rosenbrock"]
    algoritmo_di_ottimizzazione=file_meta_dati["algoritmo_di_ottimizzazione"]
if nome_funzione_obiettivo=="sferica":
    from FO.sferica import sferica
    funzione_obiettivo=sferica
    limiti_variabili=file_meta_dati["limiti_variabili_sferica"]
    algoritmo_di_ottimizzazione=file_meta_dati["algoritmo_di_ottimizzazione"]
if nome_funzione_obiettivo=="schwefel":
    from FO.schwefel import schwefel
    funzione_obiettivo=schwefel
    limiti_variabili=file_meta_dati["limiti_variabili_schwefel"]
    algoritmo_di_ottimizzazione=file_meta_dati["algoritmo_di_ottimizzazione"]
if nome_funzione_obiettivo=="griewank":
    from FO.griewank import griewank
    funzione_obiettivo=griewank
    limiti_variabili=file_meta_dati["limiti_variabili_griewank"]
algoritmo_di_ottimizzazione=file_meta_dati["algoritmo_di_ottimizzazione"]
if algoritmo_di_ottimizzazione=="GA":
    metaparametri=file_meta_dati["metaparametri_GA"]
else:
    print("Non ci sono altri algoritmi implementati!")



# OTTIMIZZAZIONE DEL FIS

# popolamento del training set
# simulazione di predizione
numero_MG=7
p_G_predetta=np.random.uniform(0,4,numero_MG)
p_L_predetta=np.random.uniform(0,4,numero_MG)
training_set=[p_G_predetta,p_L_predetta]


# dati sulle MG (modello fisico simulato)
dati_MG=[MG_1,
         MG_2,
         MG_3,
         MG_4,
         MG_5,
         MG_6,
         MG_7]

# carica il fis
dati_fis=[]
with open("fis.json") as file:
    dati_fis=json.load(file)
    
dati_modello=[dati_fis, dati_MG, training_set]
   
# ottimizza il fis
esecuzione=1
risultati_ottimizzazione=ottimizzaFIS(dati_modello,
                       funzione_obiettivo, 
                       limiti_variabili, 
                       metaparametri,
                       nome_funzione_obiettivo, 
                       esecuzione)
fis_ottimo=risultati_ottimizzazione[0][2][0]
fo_ottima=risultati_ottimizzazione[0][1][0]
fis_ottimo.append(fo_ottima)
risultati_finali=globale_fine_ottimizzazione(fis_ottimo, dati_modello)


print("fine")










