# Calcola il valore della la Funzione Obiettivo (FO)
# INPUT: 
    # is_CER; vale 0 se è un AUC oppure 1 se è una CER
    # matrice_input_predizioni; la generica colonna contiene i valori
          # predetti per un timeslot k, [P_G_k, P_L1_k, P_L2_k]; le colonne sono i 
          # i timeslot
    # matrice_variabili_decisioni; la generica colonna contiene i valori
          # delle variabili deciisonali per k, [P_N_k, P_S_k, P_GS_k, P_GL1_k, P_GL2_k, P_NL1_k,P_SL1_k]; 
          # le colonne sono i timeslot; LE ULTIME 4 VARIABILI DECISIONALI DEVONO ESSERE POSITIVE!
    # SoC_0; valore iniziale dello Stato di Carica della batteria
# OUTPUT: stampa a video del valore della FO per tutto lìorizzonte temporale

# NOTA: Condizioni violate che non dipendono dalle direttive dell'operatore ma da errori
# nell'uso della funzione (es. valori di input passati col segno meno quando sono
# ammessi solo valori positivi) lanciano eccezioni; invece, la violazione di 
# condizioni desiderate dall'operatore come ad esempio che la SoC si mantenga 
# entro uncerto intervallo, comportano una penalità che consiste in un valore
# di default della FO pari a 99999


def calcola_FO(is_CER, matrice_input_predizioni, matrice_variabili_decisioni, SoC_0):
   
    
    # fattori di conversione
    e_on_MWh_TO_e_on_kWh = 0.001
    
    
    # costanti (parametri del modello fissati)
    delta_t=0.083  # lunghezza del timeslot k (5 minuti) [h]
    TP_CE = 0  # tariffa premio [€/MWh]
    if is_CER:  # se si tratta di una CER
        TP_CE=110
    else:  # se non si tratta di una CER, quindi si tratta di un AUC
        TP_CE=100      
    TRAS_e=7.61  # tariffa di trasmissione definita per le utenze in bassa tensione [€/MWh]
    max_BTAU_m=0.61  # valore maggiore della componente variabile di distribuzione [€/MWh]
    CPR=0.026  # coefficiente delle perdite di rete evitate [-]
    Pz=3.2  # prezzo zonale orario [€/MWh]
    PR_3=150  # prezzo dell'energia per il ritiro dedicato [€/MWh]
    Z_k=0.03  # canone impianto PV [€/kWh]
    SoC_0=SoC_0  # Stato di Carica della batteria all'inizio
    eta=0.94  # rendimento della batteria
    SoC_min=0.15  # Stato di Carica minimo della batteria 
    SoC_max=0.95  # Stato di Carica massimo della batteria
    Q=20  # Capacità della batteria [kWh]
    P_S_max=5  # massima Potenza di carica/scarica della batteria [kW]
    B=18873  # prezzo della batteria [€]
    a=1589  # parametro della curva cicli/DoD della batteria
    b=1.428  # parametro della curva cicli/DoD della batteria
    
    
    # calcola il valore della FO nel timeslot k
    FO=0  # inizializza il valore della FO per tutto l'orizzonte temporale T
    T = len(matrice_input_predizioni)  # orizzonte temporale (288 timeslot ovvero 24 h)
    list_FO_k=[0];  # inizializza la list dei valori di FO per ogni k
    list_SoC_k=[SoC_0]; # inizializza la list dei valori di SoC per ogni k
    for timeslot in range(T):  # scorri ogni timeslot k
        # estrai i valori di input
        input_per_k=matrice_input_predizioni[timeslot]
        P_G_k=input_per_k[0]
        P_L1_k=input_per_k[1]
        P_L2_k=input_per_k[2]
        # estrai i valori delle variabili decisionali
        decisioni_per_k=matrice_variabili_decisioni[timeslot]
        P_N_k=decisioni_per_k[0]
        P_S_k=decisioni_per_k[1]
        P_GS_k=decisioni_per_k[2]
        P_GL1_k=decisioni_per_k[3]
        P_GL2_k=decisioni_per_k[4]
        P_NL1_k=decisioni_per_k[5]
        P_SL1_k=decisioni_per_k[6]        
        # calcola le quantità derivate dalle variabili decisionali
        P_GN_k=P_G_k-(P_GS_k+P_GL1_k+P_GL2_k)
        P_NL2_k=abs(P_N_k)-P_NL1_k-P_GN_k
        P_SL2_k=abs(P_S_k)-P_SL1_k-P_GS_k
        # controlla la corretteza del segno dei flussi di Potenza
        if P_GS_k<0 or P_GL1_k<0 or P_GL2_k<0 or P_NL1_k<0 or P_NL2_k<0 or P_SL1_k<0 or P_SL2_k<0 or P_GN_k<0:
            raise Exception("I flussi di Potenza non possono essere negativi!")
        # controlla la corretteza del segno della Potenza generata
        if P_G_k<0:
            raise Exception("La Potenza generata non può essere negativa!")
        # controllo la corretteza del segno della Potenza assorbitadai carichi
        if P_L1_k>0 or P_L2_k>0:
            raise Exception("La Potenza assorbita dai carichi non può essere positiva!")
        # controllo del vincolo sulla Potenza scambiata dalla batteria
        if abs(P_S_k)>P_S_max:
            print("Vincolo sulla Potenza scambiata dalla batteria violato!")
            FO=99999
            return
        # calcola altre quantità necessarie
        E_prod_k=delta_t*(P_GN_k+P_GS_k+P_GL1_k+P_GL2_k)  # energia prodotta [kWh]
        E_prel_k=delta_t*(P_GL1_k+P_GL2_k+P_GS_k+P_SL1_k+P_SL2_k)  # energia prelevata [kWh]
        E_cond_k=min(E_prod_k, E_prel_k)  # energia condivisa [kWh]
        I_rit_k=PR_3*e_on_MWh_TO_e_on_kWh*delta_t*P_GN_k  # contributo per il ritiro dell'energia immessa in N [€/kWh]
        CU_af_m=(TRAS_e+max_BTAU_m)*e_on_MWh_TO_e_on_kWh  # consumo unitario del corrispettivo forfettario mensile [€/kWh]    
        I_rest_k=0  # restituzione componenti tariffarie [€]
        if is_CER==1:  # se si tratta di una CER
            I_rest_k=CU_af_m*E_cond_k  
        else:  # se non si tratta di una CER, quindi si tratta di un AUC
            I_rest_k=CU_af_m*E_cond_k+CPR*Pz*e_on_MWh_TO_e_on_kWh*E_cond_k
        I_cond_k =TP_CE*e_on_MWh_TO_e_on_kWh*E_cond_k  # incentivazione energia condivisa [€]
        R_k=I_cond_k+I_rest_k+I_rit_k  # ricavo in k [€]
        if timeslot==0:
            if P_S_k>=0:  # la batteria è in fase di scarica
                SoC_k=SoC_0+(P_S_k*delta_t/(eta*Q))
            else:  # la batteria è in fase di carica
                SoC_k=SoC_0+(eta*P_S_k*delta_t/Q)    
        else:
            if P_S_k>=0:  # la batteria è in fase di scarica
                SoC_k=list_SoC_k[timeslot-1]+(P_S_k*delta_t/(eta*Q))
            else:  # la batteria è in fase di carica
                SoC_k=list_SoC_k[timeslot-1]+(eta*P_S_k*delta_t/Q)
        list_SoC_k.append(SoC_k)  # aggiorna la list dei valori di SoC per ogni k
        if timeslot ==0:
            W_SoC_k_prec=(B/(2*Q*eta))*(b*pow((1-SoC_0),(b-1)))/a  # densità costo operazionale batteria in k-1 [€/kWh]
            W_SoC_k=(B/(2*Q*eta))*(b*pow((1-SoC_0),(b-1)))/a  # densità costo operazionale batteria in k [€/kWh]
        else:
            W_SoC_k_prec=(B/(2*Q*eta))*(b*pow((1-list_SoC_k[timeslot-1]),(b-1)))/a  # densità costo operazionale batteria in k-1 [€/kWh]
            W_SoC_k=(B/(2*Q*eta))*(b*pow((1-SoC_k),(b-1)))/a  # densità costo operazionale batteria in k [€/kWh]
        C_b_k=((delta_t/2)*(W_SoC_k_prec+W_SoC_k))*(abs(P_S_k)) # costo operazionale della batteria in k [€]
        C_k=Z_k+C_b_k  # costi in k [€]
        FO_k=R_k-C_k  # valore della FO in k [€]
        list_FO_k.append(FO_k) # aggiorna la list dei valori di FO per ogni k
        # controlla il vincol)o sul bilancio energetico in k
        bilancio_energetico=delta_t*(P_G_k+P_N_k+P_S_k+P_L1_k+P_L2_k)  # [kWh]
        if round(bilancio_energetico,2)!=0:
            raise Exception("Il bilancio energetico è diverso da 0!")
        # controlla il vincolo sulla Potenza assorbita dai carichi
        bilancio_energia_assorbita_L1=P_L1_k+(P_GL1_k+P_NL1_k+P_SL1_k)  # [kWh]
        bilancio_energia_assorbita_L2=P_L2_k+(P_GL2_k+P_NL2_k+P_SL2_k)  # [kWh]
        if round(bilancio_energia_assorbita_L1,2)!=0 or round(bilancio_energia_assorbita_L2,2)!=0:
            raise Exception("Il bilancio di energia assorbita dai carichi è diverso da 0!")
        # controlla il vincolo sullo SoC della batteria
        if round(SoC_k,2)>SoC_max or round(SoC_k,2)<SoC_min:
            print("Vincolo sullo Stato di Carica violato!")
            FO=99999
            return
        # controlla il rispetto dei vincoli sulla contemporaneità di alcuni flussi di Potenza
        if P_GN_k>0 and P_NL1_k!=0:  # vincolo 1
            print("Vincolo #1 non rispettato!")
            FO=99999
            return
        if P_GN_k>0 and P_NL2_k!=0:  # vincolo 2
            print("Vincolo #2 non rispettato!")    
            FO=99999
            return
        if P_GS_k>0 and P_SL1_k!=0:  # vincolo 3
            print("Vincolo #3 non rispettato!")
            FO=99999
            return
        if P_GS_k>0 and P_SL2_k!=0:  # vincolo 4
            print("Vincolo #4 non rispettato!")   
            FO=99999
            return
            
    # calcola e stampa a video il valore della FO per tutto l'orizzonte temporale T
    FO=sum(list_FO_k)   # valore della FO [€]
    print("La FO per tutto l'orizzonte temporale vale (un valore positivo indica una spesa mentre un valore negativo indica un guadagno): ", FO, "","[€]")
    


    # Testa la funzione 
    # (orizzonte temporale di 2 timeslot)
    is_CER=1
    SoC_0=0.5
    matrice_input_predizioni=[[3,-0.5,-0.21], [0,-2,-3]]
    matrice_variabili_decisioni=[[0,-2.29,2.29,0.5,0.21,0,0],[5,0,0,0,0,2,0]]
    calcola_FO(is_CER, matrice_input_predizioni, matrice_variabili_decisioni, SoC_0)


    # Genera un input e una matrice di decisioni i cui valori sono ragionevoli
    # ma non necessariamente ammissibili rispetto ai vincoli definiti dentro la FO
    import numpy as np
    n_timeslot = 288    
    max_potenza_PV=6  # [kW]
    max_potenza_assorbita=3  # [kW]
    max_potenza_N=5  # [kWh]
    max_potenza_S=5  # [kWh]
    max_potenza_singolo_flusso=5  # [kWh]
    vettore_produzione=np.random.uniform(max_potenza_PV, size=(n_timeslot))
    vettore_consumi_L1=-np.random.uniform(max_potenza_assorbita, size=(n_timeslot))
    vettore_consumi_L2=-np.random.uniform(max_potenza_assorbita, size=(n_timeslot))
    matrice_input_predizioni=[vettore_produzione,vettore_consumi_L1,vettore_consumi_L2]
    vettore_variabile_P_N_k=np.random.uniform(low=-max_potenza_N,high=max_potenza_N,size=(n_timeslot))
    vettore_variabile_P_S_k=np.random.uniform(low=0,high=max_potenza_S,size=(n_timeslot))
    vettore_variabile_P_GS_k=np.random.uniform(low=0,high=max_potenza_singolo_flusso,size=(n_timeslot))
    vettore_variabile_P_GL1_k=np.random.uniform(low=0,high=max_potenza_singolo_flusso,size=(n_timeslot))
    vettore_variabile_P_GL2_k=np.random.uniform(low=0,high=max_potenza_singolo_flusso,size=(n_timeslot))
    vettore_variabile_P_NL1_k=np.random.uniform(low=0,high=max_potenza_singolo_flusso,size=(n_timeslot))
    vettore_variabile_P_SL1_k=np.random.uniform(low=0,high=max_potenza_singolo_flusso,size=(n_timeslot))
    matrice_variabili_decisioni=[vettore_variabile_P_N_k,vettore_variabile_P_S_k,vettore_variabile_P_GS_k,
                             vettore_variabile_P_GL1_k,vettore_variabile_P_GL2_k,vettore_variabile_P_NL1_k,
                             vettore_variabile_P_SL1_k]
    is_CER=1
    SoC_0=0.5
    # calcola_FO(is_CER, matrice_input_predizioni, matrice_variabili_decisioni, SoC_0)

