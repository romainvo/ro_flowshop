#prend une liste de job et renvoie cette meme liste ordonnée selon la première étape de la méthode NEH.
def OrdonnerListe(ListeJob):
    ListeNEH=[ListeJob[0]];
    for J in ListeJob:
        i=0;
        while(J.duree()<ListeNEH[i].duree()) :
            i=i+1
        ListeNEH.insert(i,J)
    return ListeNEH

#deuxieme etape de la méthode
def MethodeNEH(Flowshop):
