# Calcola i limiti dei geni

# importa il pacchetto json 
import json

# carica il fis
dati_fis=[]
with open("fis.json") as file:
    dati_fis=json.load(file)

numero_geni_pesi=dati_fis["n_regole"]
numero_geni_conseguenti=dati_fis["n_output"]
numero_geni_per_MF=2
numero_geni_MF_i=dati_fis["n_MF_i"]*numero_geni_per_MF
numero_geni_MF_o=dati_fis["n_MF_o"]*numero_geni_per_MF
limitiInferioriGeniPesi = [0]*numero_geni_pesi
limitiInferioriGeniConseguenti = [1]*numero_geni_conseguenti
limitiSuperioriGeniPesi = [1]*numero_geni_pesi
limitiSuperioriGeniConseguenti = [5]*numero_geni_conseguenti
larghezzaDiRiferimentoMFTriInput = 0.30
larghezzaDiRiferimentoMFTriOutput = 0.30
limiteInferioreAlfa = 0.01
limiteSuperioreAlfaInput = 1/larghezzaDiRiferimentoMFTriInput
limiteSuperioreAlfaOutput = 1/larghezzaDiRiferimentoMFTriOutput
limiteInferioreBeta = 0.01
limiteSuperioreBeta = 1.99
limiteInferioreGammaInput = 0.04
limiteSuperioreGammaInput = 4
limiteInferioreGammaOutput = 0.04
limiteSuperioreGammaOutput= 4
limiteInferioreOmega = 0.01
limiteSuperioreOmega = 0.99
limitiInferioriGeniMFInput = [0]*numero_geni_MF_i
limitiSuperioriGeniMFInput = [0]*numero_geni_MF_i
for i in range(0,numero_geni_MF_i):
    # MF trapezoidali
    if i == 0 or i == 8: 
        limitiInferioriGeniMFInput[i] = round(limiteInferioreGammaInput,2)
        limitiInferioriGeniMFInput[i+1] = round(limiteInferioreOmega,2)
        limitiSuperioriGeniMFInput[i] = round(limiteSuperioreGammaInput,2)
        limitiSuperioriGeniMFInput[i+1] = round(limiteSuperioreOmega,2)
    # MF triangolari
    if i == 2 or i == 4 or i == 6:
        limitiInferioriGeniMFInput[i] = round(limiteInferioreAlfa,2)
        limitiInferioriGeniMFInput[i+1] = round(limiteInferioreBeta,2)
        limitiSuperioriGeniMFInput[i] = round(limiteSuperioreAlfaInput,2)
        limitiSuperioriGeniMFInput[i+1] = round(limiteSuperioreBeta,2)
limitiInferioriGenMFOutput=limitiInferioriGeniMFInput
limitiSuperioriGenMFOutput=limitiSuperioriGeniMFInput
limitiInferioriGeni = [limitiInferioriGeniMFInput,limitiInferioriGeniPesi, limitiInferioriGeniConseguenti]
limitiSuperioriGeni = [limitiSuperioriGeniMFInput,limitiSuperioriGeniPesi, limitiSuperioriGeniConseguenti]
# limitiInferioriGeni=round(limitiInferioriGeni,2)
# limitiSuperioriGeni=round(limitiSuperioriGeni,2)