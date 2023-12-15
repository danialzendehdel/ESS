import pandas as pd
from tqdm import tqdm
from BESS.classe_ECM import ECM
from GA.esegui_GA_debug import esegui_GA_debug
import json
import math
from BESS.classe_PREP_DATA import PREP_DATA

def ottimizza(metaparametri):
    

    #CARICO TRAIN SET
    train_set_path = './DATA/ECM_DATA_dataset.xlsx'
    train_set = pd.read_excel(train_set_path)
    lookup_table_path = './DATA/ECM_DATA_lookup.xlsx'
    lookup_table = pd.read_excel(lookup_table_path)
    

    #Inizializzo modello batteria sapendo che SoC(t=0)=1
    battery_capacity = 2 #Ah

    BM = ECM(battery_capacity)
    BM.charge_lookup_table = lookup_table[lookup_table['Mode']=='C']
    BM.discharge_lookup_table = lookup_table[lookup_table['Mode']=='D']
    BM.Soc_0 = 1
    BM.DoD_0 = 0
    num_genes = BM.num_genes

    x = [0,100]
    lim_l=[]
    lim_h=[]
    parametri_GA_header = []
    for i in range(num_genes):
        lim_l.append(x[0])
        lim_h.append(x[1])
        parametri_GA_header.append(str('a'+str(i)))
    lim = [lim_l, lim_h]

    stato = pd.DataFrame(columns=['SoC_t','SoC','Error','Charge','Mode','Gen','FO'])
    parametri_GA = pd.DataFrame(columns=parametri_GA_header)


    err = []
    for i in tqdm(range(train_set.shape[0])):
        pattern = train_set.loc[i]
        if i == 0 :
            SoC_past=1
            BM.SoC = BM.SoC + [1]
            BM.DoD = BM.DoD + [1- (pattern['Charge_Capacity(Ah)']-pattern['Discharge_Capacity(Ah)'])/battery_capacity]
            continue

        SoC_t = pattern['SoC(%)']
        BM.dt = pattern['Test_Time(s)']-train_set.loc[i-1]['Test_Time(s)']
        I = pattern['Current(A)']
        if I < 0:
            BM.mode = 'D'
            BM.OCV_d_th.append(pattern['Voltage(V)'])
        elif I > 0:
            BM.mode = 'C'
            BM.OCV_c_th.append(pattern['Voltage(V)'])
            
        else:
            continue


        BM.I = abs(I)
        BM.Qr = pattern['Charge_Capacity(Ah)']-pattern['Discharge_Capacity(Ah)']
        BM.rate = BM.I/BM.Qr
        
        if parametri_GA.shape[0] > 1:
            risultati_GA =  esegui_GA_debug('ECM',lim, metaparametri,'modello_ECM', 1, BM, risultati_GA[1]+[0])

        else:
            risultati_GA =  esegui_GA_debug('ECM',lim, metaparametri,'modello_ECM', 1, BM)
        
        
        OCV = BM.compute_ECM(BM.rate,SoC_past,risultati_GA[1])
        SoC_pred = BM.compute_SoC(SoC_past)
         
        
        err = SoC_t-SoC_pred

        stato.loc[i-1] = [SoC_t,SoC_pred,err, BM.Qr, BM.mode, risultati_GA[2], risultati_GA[0]]
        parametri_GA.loc[i-1] = risultati_GA[1]

        SoC_past = SoC_t

    RES = pd.concat([stato, parametri_GA], axis=1)
            

    RES.to_csv('/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/MASTRANDREA_DEBUG_EMS/GA/Risultati/ECM/ris_ottimizz_'
               +str(metaparametri[1]) +'_'+str(metaparametri[2]) +'_'+str(metaparametri[3])+'_'
               +str(metaparametri[-3])+'_'+str(metaparametri[-2])+'_'+str(metaparametri[-1])
               +str(metaparametri[7])+'.csv')   
        
if __name__ == '__main__':

    #TEST B
    metaparametri = [200,0.3,0.1,0.05,'FO_thresh',300,50,1e-7,50,10,0.5,'']

    ottimizza(metaparametri)

    ##TEST A
    #k = 50  #granularita dataset k=50 --> 126 linee per scarica
    #dim_pop = 200
    #co_fraction = [0.1,0.5]
    #m_prob = [0.1,0.5]
    #att_mut = [0.05,0.3]
    #max_gen = 1000
    #toll = [0.01]
    #num_elite = [20,50]
    #dim_torneo = [10,20,50]
    #frazione_figli = [0.3,0.5 ]
    #0.1,0.1,0.05,50,20,0.3

    #for a in co_fraction:
    #    for b in m_prob:
    #        for c in att_mut:
    #            for e in num_elite:
    #                for f in dim_torneo:
    #                    for g in frazione_figli:
    #                        if e >= f:
    #                            metaparametri = [dim_pop,a,b,c,'FO_thresh',max_gen,50,toll,e,f,g]
    #                            ottimizza(metaparametri)

    