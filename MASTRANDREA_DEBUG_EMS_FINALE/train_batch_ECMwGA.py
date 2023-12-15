import pandas as pd 
from tqdm import tqdm
from BESS.classe_ECM import ECM
from BESS.classe_PREP_DATA import PREP_DATA
from GA.esegui_GA_debug import esegui_GA_debug
import json

def batch_opt(metaparametri,rate,mode, past_best=[]):
    ##PULISCO DATASET 
    #path = '/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/MASTRANDREA_DEBUG_EMS/DATA'
    #PREP_DATA(path).prepare_calce('/Users/luca/Downloads/10_16_2015_Initial capacity_SP20-3.xls',k=50)

    #CARICO TRAIN SET
    train_set_path = './DATA/ECM_DATA_dataset.xlsx'
    lookup_table_path = './DATA/ECM_DATA_lookup.xlsx'
    lookup_table = pd.read_excel(lookup_table_path)
    
 


    #Inizializzo modello batteria sapendo che SoC(t=0)=1
    battery_capacity = 2 #Ah

    BM = ECM(battery_capacity)
    BM.charge_lookup_table = lookup_table[lookup_table['Mode']=='C']
    BM.discharge_lookup_table = lookup_table[lookup_table['Mode']=='D']
    BM.rate = rate
    BM.mode = mode
    BM.Soc_0 = 1
    BM.DoD_0 = 0
    num_genes = BM.num_genes

    x = [-300,300]
    lim_l=[]
    lim_h=[]
    parametri_GA_header = []
    for i in range(num_genes):
        lim_l.append(x[0])
        lim_h.append(x[1])
        parametri_GA_header.append(str('a'+str(i)))
    lim = [lim_l, lim_h]

   
    
    risultati_GA =  esegui_GA_debug('ECM_batch',lim, metaparametri,'modello_ECM_batch', 1, BM,past_best)
    
    return risultati_GA
if __name__ == '__main__':

    dim_pop = 300
    co_fraction = 0.1
    m_prob = 0.1
    att_mut = 0.3
    max_gen = 10
    toll = 0.01
    num_elite = 20
    dim_torneo = 10
    frazione_figli = 0.1
    #[300, 0.5, 0.9, 0.5, 'FO_thresh', 2000, 50, 0.01, 50, 10, 0.9]
    #DISCHpast_best = [745.2667937158546, 456.90660070178126, 910.4785677165121, 394.06599235696814, 90.51795126326894, 401.9195431311089, 188.8164283319053, 362.8820438544554, 353.5593405585662, 668.414365523268, 637.7168942007313, 724.6066944265402, 466.75682040824574, 325.15094803726936, 64.94503458710777, 284.3604353042442, 700.3471166757454, 42.121414765051654, 841.5770555538946, 260.52199156138073, 630.1582654738992, 582.0310534101808, 318.50450480885723, 294.1368567476246, 166.49274994001235, 75.19612271316154, 0.017489740262152085, 0.021371273618492163, 0.018464474095900033, 550.2193679751568, 541.7317437601653,0]
    #CHRG
    past_best  = [-249.11138745354629, 299.96497928726274, 299.9999999999933, 77.02470182016796, -42.22468038382437, 198.62384914579394, 168.10984993001534, -87.16752742085225, 216.4860598680812, -78.57381931218916, -97.83710579388864, -73.63690891337555, 54.123732604402974, -41.01887582633482, 30.79680656173172, -217.92707049276157, 292.23334689896274, 290.8382779534078, 299.6462745692892, -182.3477496562711, -169.77978712822022, 299.9975226330797, -117.38021082941938, -288.4114567676975, 295.5688555505237, -82.5921688700113, -34.914231721968605, -31.8022839960855, 206.8754039963872, 40.33583520526396, -47.64330051156962, 0]
    FO = 10000
    #past_best = None
    while FO > toll:
        
        metaparametri = [dim_pop,co_fraction,m_prob,att_mut,'FO_thresh',10, 50,toll,num_elite,dim_torneo,frazione_figli]
        risultati = batch_opt(metaparametri,0.5,'D',past_best)
        FO = risultati[0]
        print(FO)
        past_best = risultati[1] + [0]
        print(past_best)