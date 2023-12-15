import pandas as pd
import numpy as np

class PREP_DATA:

    def __init__(self,  dest_path,):

        self.path_to_data = dest_path
        
        self.norm_param = []

    def prepare_calce(self,path, norm_type = 'None', step = 1, k = 100):
        #NOT IN THE SCOPE Step 1: Resting , 2-3: charging, 4&9: resistance measures 
        #

        raw = pd.read_excel(path,sheet_name=1, usecols=['Data_Point', 'Test_Time(s)',  'Step_Index', 'Current(A)', 'Voltage(V)', 'Charge_Capacity(Ah)','Discharge_Capacity(Ah)'])

        #print(raw)
        if step != 0:
           raw = raw[~raw['Step_Index'].isin([1,2,3,4,5,8,9,12])]

        if norm_type == 'Z-Score':
            self.norm_param = [raw.mean(), raw.std()]
            self.df = (raw-raw.mean())/raw.std()
            self.df['Data_Point', 'Test_Time(s)',  'Step_Index'] = raw['Data_Point', 'Test_Time(s)',  'Step_Index']
            self.df['Data_Point'] = raw['Data_Point']
            self.df['Test_Time(s)'] = raw['Test_Time(s)']
            self.df['Step_Index'] = raw['Step_Index']

        elif norm_type == 'min-max':
            self.norm_param = [raw.min(), raw.max()]
            self.df = (raw - raw.min()) / (raw.max()-raw.min())
            self.df['Data_Point'] = raw['Data_Point']
            self.df['Test_Time(s)'] = raw['Test_Time(s)']
            self.df['Step_Index'] = raw['Step_Index']
        else:
            self.df = raw
            self.df['SoC(%)']= (self.df['Charge_Capacity(Ah)']-self.df['Discharge_Capacity(Ah)'])/2
        
        self.df1 = pd.DataFrame(columns=['SoC(%)', 'Test_Time(s)',  'Step_Index', 'Current(A)', 'Voltage(V)', 'Charge_Capacity(Ah)','Discharge_Capacity(Ah)'])
        self.df2 = pd.DataFrame(columns=['SoC(%)', 'Voltage(V)','Current(A)','Mode', 'Test_Time(s)', 'Capacity(Ah)'])
        for i in range(k+1,self.df.shape[0]):
            if [self.df['Step_Index'].iloc[i-kk] for kk in range(k)] == [self.df['Step_Index'].iloc[i-kk-1] for kk in range(k)]:
                if (i-1)%k == 0 :
                    TT = self.df['Test_Time(s)'].iloc[i-1]
                    
                    V = self.df['Voltage(V)'].iloc[i-1]
                    SI = self.df['Step_Index'].iloc[i-1]
                    CC= self.df['Charge_Capacity(Ah)'].iloc[i-1]
                    DC = self.df['Discharge_Capacity(Ah)'].iloc[i-1]
                    Q = CC-DC
                    SoC = self.df['SoC(%)'].iloc[i-1]
                    A = np.mean([self.df['Current(A)'].iloc[i-kk-1] for kk in range(k)])
                    if A >= 0:
                        M = 'C'
                    elif A<0:
                        M = 'D'
                    self.df1.loc[(i//k)-1,:] = [SoC,TT,SI,A,V,CC,DC]
                    self.df2.loc[(i//k)-1,:] = [SoC,V,A,M,TT,Q]
        
        self.df1.to_excel(self.path_to_data+'_dataset.xlsx')
        self.df2.to_excel(self.path_to_data+'_lookup.xlsx')

   
if __name__ == "__main__":
    root = '/Users/luca/Desktop/UNIVERSITA/EMS_TESINA/MASTRANDREA_DEBUG_EMS/DATA/ECM_DATA'
    df_path = '/Users/luca/Downloads/10_16_2015_Initial capacity_SP20-3.xls'
    PREP_DATA(root).prepare_calce(df_path)
