# Funzione che plotta i risultati e salva le figure
def plotta_risultati(best_FO,media_FO,nome_funzione_obiettivo,esecuzione,best_FO_corrente):

    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.title("Best-mean FO"+"-"+nome_funzione_obiettivo+"-Esec. "+str(esecuzione)
              +"\n"+"Best = "+str(round(best_FO_corrente,3)))
    plt.plot(best_FO, 'k*', label="best")
    plt.plot(media_FO,'b+',label="mean")
    plt.xlabel('gen')           
    plt.ylabel('FO')
    plt.legend()
    plt.show()
    fig.savefig("./GA/Risultati/"+"best-mean_plot_esec_"+str(esecuzione)+".pdf", format="pdf")