# Salva la popolazione per la generazione corrente (per backup)

def salva_popolazione(generazione,popolazione):
    import os
    file_path = os.path.join("./GA/Stato"
                             ,"popolazione_"+"generazione_"+str(generazione)+".txt")
    with open(file_path, "w") as file:
        file.write(str(popolazione))
    