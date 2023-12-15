# Salva i risultati

def salva_risultati(risultati,esecuzione,nome_funzione_obiettivo):
    import os
    file_path = os.path.join("./GA/Risultati","risultati_esec_"
                             +str(esecuzione)+nome_funzione_obiettivo+"_"".txt")
    with open(file_path, "w") as file:
        file.write(str(risultati))
    
    