import math
import numpy as np
import pandas as pd

class ECM:

    def __init__(self,battery_capacity=2, battery_price=9000, a0=0, a1=0, a2=0, model_dim = '', SoC_0 = 1, DoD_0 = 0): 
        
        self.mode = ''
        self.model_dim = model_dim
        
        self.battery_price = battery_price

        self.a0 = a0
        self.a1 = a1
        self.a2 = a2

        self.OCV = float()
        self.OCV_c = []
        self.OCV_d = []
        self.OCV_c_th = []
        self.OCV_d_th = []
        
        self.capacity = battery_capacity

        self.I = 0
        self.SoC = []
        self.SoC_0 = SoC_0
        self.Qr = SoC_0 * battery_capacity

        self.DoD = []
        self.DoD_0 = DoD_0
        
        self.rate = 0
        self.dt = 0


        if model_dim == 'small':
            self.num_genes = 20
        elif model_dim == '':
            self.num_genes = 31
        
        self.lookup_table = [[]]
        self.charge_lookup_table = [[]]
        self.discharge_lookup_table = [[]]
   

    def compute_ECM(self,x,y, param): #x = Cr or Dr y=  current SoC or 1-current DoD
        
        self.R1 = (param[0]+param[1]*x+param[2]*pow(x,2))    *math.exp(-param[3] *y)+(param[4]  +param[5] *x+param[6]*pow(x,2))
        self.R2 = (param[7]+param[8]*x+param[9]*pow(x,2))    *math.exp(-param[10]*y)+(param[11]+param[12]*x+param[13]*pow(x,2))
        self.C = -(param[14]+param[15]*x+param[16]*pow(x,2))  *math.exp(-param[17]*y)+(param[18]+param[19]*x+param[20]*pow(x,2))
        self.V0 = (param[21]+param[22]*x+param[23]*pow(x,2)) *math.exp(-param[24]*y)+(param[25]+param[26]*y+param[27]*pow(y,2)+param[28]*pow(y,3))-param[29]*x-param[30]*pow(x,2)
        try:
            OCV =((self.Qr/self.C + self.I*self.R2)*math.exp(-self.dt/(self.R2*self.C)))+ self.V0 - (self.I*(self.R1+self.R2))
        except OverflowError:
            OCV =float('inf')
        return OCV
    
    def compute_ECM_small(self,x,y,param):
        self.OCV = 0
        self.R1 = (param[0]+param[1]*x+param[2]*pow(x,2))*math.exp(-param[3]*y) + param[4]
        self.R2 = (param[5]+param[6]*x+param[7]*pow(x,2))*math.exp(-param[8]*y)+ param[9]
        self.C = (param[10]+param[11]*x+param[12]*pow(x,2))*math.exp(-param[13]*y)+ param[14]
        self.V0 = (param[15]+param[16]*x+param[17]*pow(x,2))*math.exp(-param[18]*y) + param[19]
        try:
            OCV =((self.Qr/self.C + self.I*self.R2)*math.exp(-self.dt/(self.R2*self.C)))+ self.V0 - (self.I*(self.R1+self.R2))
        except OverflowError:
            OCV =float('inf')
        return OCV
        

    def compute_SoC(self,SoC):
        dQ = (self.rate*self.dt/3600)

        if self.mode == 'C':
            SoC = SoC + dQ
            return SoC
        
        elif self.mode =='D':
            SoC = SoC - dQ
            return SoC
    
    def lookup_SoC(self,OCV,table):
        
        array = table['Voltage(V)'].to_numpy()
        idx = (np.abs(array - OCV)).argmin()
        return table['SoC(%)'].loc[idx]


    def calcola_costo_operazionale_BESS(self,SOC,SOC_new):
        w1 =  ((1-SOC_new)**self.a1)*math.e**(self.a2*(1-SOC_new))
        w2 =  ((1-SOC)**self.a1)*math.e**(self.a2*(1-SOC))

        cost = (self.battery_price/(2*self.a0))*abs(w1-w2)

        return cost
