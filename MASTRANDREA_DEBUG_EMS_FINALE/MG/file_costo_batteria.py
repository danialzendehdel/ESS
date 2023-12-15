# funzione che calcola il costo operazionale della batteria 
# The following model refers to eq [7] of "A practical wear model for EV charging application", Han
# and is dopendant of the SoC
#B : Battery price in eur
#Q : Battery size
#eta: cycle efficiency of the battery
#a,b : battery dependant parameters aquired through misurements

def calcola_costo_operazionale_batteria(SoC_k_prec,SoC_K,eta,B,Q,b,a,p_S_k,delta_t):
    
    # densità costo operazionale batteria in k-1 [€/kWh]
    W_SoC_k_prec=(B/(2*Q*eta))*(b*pow((1-SoC_k_prec),(b-1)))/a  
    # densità costo operazionale batteria in k [€/kWh]
    W_SoC_k=(B/(2*Q*eta))*(b*pow((1-SoC_K),(b-1)))/a 
    # costo operazionale della batteria in k [€]
    C_b_k=((delta_t/2)*(W_SoC_k_prec+W_SoC_k))*(abs(p_S_k)) 
    
    return C_b_k