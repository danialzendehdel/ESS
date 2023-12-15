import pandas as pd
from tqdm import tqdm
from BESS.classe_ECM import ECM
from GA.esegui_GA import esegui_GA
import json

##PULISCO DATASET 
#path = '/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/#myEMS/12_2_2015_Incremental OCV test_SP20-3.xlsx'
#PREP_DATA(path).prepare_calce(exp_type='incremental')

#CARICO TRAIN SET
train_set_path = '/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/myEMS/calce_low_filtered_10.xlsx'
train_set = pd.read_excel(train_set_path)
#CARICO METAPARAMETRI GA
with open('meta-dati.json') as file:
    file_meta_dati_ECM = json.load(file)

metaparametri = file_meta_dati_ECM['metaparametri_GA_ECM']

#Inizializzo modello batteria sapendo che SoC(t=0)=1
battery_capacity = 2 #Ah

BM = ECM(battery_capacity)
BM.Soc_0 = 1
BM.DoD_0 = 0
num_genes = BM.num_genes

x = [0,500]
lim_l=[]
lim_h=[]
parametri_GA_header = []
for i in range(num_genes):
    lim_l.append(x[0])
    lim_h.append(x[1])
    parametri_GA_header.append(str('a'+str(i)))
lim = [lim_l, lim_h]

stato = pd.DataFrame(columns=['SoC','Charge','Mode','Gen','FO'])
parametri_GA = pd.DataFrame(columns=parametri_GA_header)

C_o_D_past = ''
C_o_D_present = ''
for k in tqdm(range(1)):
    for i in tqdm(range(len(train_set))):
        pattern = train_set.loc[i]
        if i == 0:
            continue

        
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
        
        
        risultati_GA =  esegui_GA('ECM',lim, metaparametri,'modello_ECM', 1, BM)
        
        SoC = BM.compute_SoC()

        

        stato.loc[i-1] = [SoC, BM.mode, BM.Qr, risultati_GA[2], risultati_GA[0]]
        parametri_GA.loc[i-1] = risultati_GA[1]
        

    parametri_GA.to_csv('/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/MASTRANDREA_DEBUG_EMS/GA/Risultati/ECM/parametri_GA_'+str(BM.mode)+'.csv')   
    stato.to_csv('/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/MASTRANDREA_DEBUG_EMS/GA/Risultati/ECM/stato_GA_'+str(BM.mode)+'.csv')   
    
