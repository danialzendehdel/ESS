from BESS.classe_ECM import ECM

def modello_ECM(individuo, BM):
    
    if BM.model_dim == 'small':
        if BM.mode == 'C':
            OCV = BM.compute_ECM_small(BM.rate,BM.SoC[-1],individuo)
            fo = abs(BM.OCV_c_th[-1]-OCV)
        elif BM.mode == 'D':
            OCV = BM.compute_ECM_small(BM.rate,(1-BM.SoC[-1]),individuo)
            fo = abs(BM.OCV_d_th[-1]-OCV)
    if BM.model_dim == '':
        if BM.mode == 'C':
            OCV = BM.compute_ECM(BM.rate,BM.SoC[-1],individuo)
            fo = abs(BM.OCV_c_th[-1]-OCV)
        elif BM.mode == 'D':
            OCV = BM.compute_ECM(BM.rate,(1-BM.SoC[-1]),individuo)
            fo = abs(BM.OCV_d_th[-1]-OCV)
    
    return fo
def modello_ECM_batch(individuo,BM):
    import itertools

    fo = 0

    if BM.model_dim == '':
        if BM.mode == 'C':
            table =BM.charge_lookup_table
            fo = []            
            for i in range(1,table.shape[0]):
                pattern = table.loc[table.index[i]]
                V = pattern['Voltage(V)']
                SoC = pattern['SoC(%)']
                BM.dt = pattern['Test_Time(s)']-table.loc[table.index[i-1]]['Test_Time(s)']
                BM.Qr = pattern['Capacity(Ah)']
                BM.I =  pattern['Current(A)']
                OCV = BM.compute_ECM(BM.rate,SoC,individuo)
                fo =fo + [(V-OCV)**2]
            fo = max(fo)
        
        if BM.mode == 'D':
            table =BM.discharge_lookup_table
            fo = []            
            for i in range(1,table.shape[0]):
                pattern = table.loc[i]
                V = pattern['Voltage(V)']
                DoD = 1-pattern['SoC(%)']
                BM.dt = pattern['Test_Time(s)']-table.loc[i-1]['Test_Time(s)']
                BM.Qr = pattern['Capacity(Ah)']
                BM.I =  pattern['Current(A)']
                OCV = BM.compute_ECM(BM.rate,DoD,individuo)
                fo =fo + [(V-OCV)**2]
            fo = max(fo)
            
        return fo
    
    if BM.model_dim == 'small':
        if BM.mode == 'C':
            table =BM.charge_lookup_table
            fo = []            
            for i in range(1,table.shape[0]):
                pattern = table.loc[i]
                V = pattern['Voltage(V)']
                DoD = pattern['SoC(%)']
                BM.dt = pattern['Test_Time(s)']-table.loc[i-1]['Test_Time(s)']
                BM.Qr = pattern['Capacity(Ah)']
                BM.I =  pattern['Current(A)']
                OCV = BM.compute_ECM_small(BM.rate,DoD,individuo)
                fo =fo + [(V-OCV)**2]
            fo = max(fo)
        
        if BM.mode == 'D':
            table =BM.discharge_lookup_table
            fo = []            
            for i in range(1,table.shape[0]):
                pattern = table.loc[i]
                V = pattern['Voltage(V)']
                DoD = 1-pattern['SoC(%)']
                BM.dt = pattern['Test_Time(s)']-table.loc[i-1]['Test_Time(s)']
                BM.Qr = pattern['Capacity(Ah)']
                BM.I =  pattern['Current(A)']
                OCV = BM.compute_ECM_small(BM.rate,DoD,individuo)
                fo =fo + [(V-OCV)**2]
            fo = max(fo)
        return fo
    

    
    