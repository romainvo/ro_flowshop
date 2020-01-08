import job,ordonnancement,flowshop
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
    ListeJob=OrdonnerListe(Flowshop.l_job)
    NbJob = Flowshop.nombre_jobs()
    NbMachine=Flowshop.nombre_machines()

    OrdoFinal=[]
    OrdoTest=[]
    OrdoTestmin=[]
    DureeMin=0
    """boucle sur les Jobs"""
    for i in range(0,NbJob) :
        """boucle sur les emplacements possibles"""
        for j in range(0,i+1) :
            OrdoTest = OrdoFinal
            if i==0 :
                OrdoTestmin.insert(0,ListeJob[i])
                DureeMin = ((ordonnancement.Ordonnancement(NbMachine)).ordonnancer_liste_job(OrdoTestmin)).duree()
            else :
                OrdoTest.insert(j, ListeJob[i])
                DureeTest=((ordonnancement.Ordonnancement(NbMachine)).ordonnancer_liste_job(OrdoTest)).duree()
                if DureeMin < DureeTest :
                    OrdoTestmin = OrdoTest
                    DureeMin = DureeTest
        """OrdoFinal= ordo le plus performant à cette étape"""
        OrdoFinal = OrdoTestmin
    Flowshop.l_job = OrdoFinal
    OrdonnancementComplet = (ordonnancement.Ordonnancement(NbMachine)).ordonnancer_liste_job(OrdoFinal)
    OrdonnancementComplet.afficher();