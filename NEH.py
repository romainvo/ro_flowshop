import job,ordonnancement,flowshop
#prend une liste de job et renvoie cette meme liste ordonnée selon 
#la première étape de la méthode NEH.

def OrdonnerListe(ListeJob):
    ListeNEH=[ListeJob[0]]
    for j in range(1,len(ListeJob)):
        J = ListeJob[j]
        i = 0
        while (J.duree_job < ListeNEH[i].duree_job and i < len(ListeNEH)-1) :
            i=i+1
        """ J'evite comme je peux l'index out of range dûe a l'augmentation de i qui est aussi dans la condition"""
        if (J.duree_job < ListeNEH[i].duree_job):
            i=i+1
        ListeNEH.insert(i,J)
    return ListeNEH

"""Methode de copie profonden d'une liste de jobs"""
def CopyJobs(copie) :
    copieur=[]
    for job in copie :
        copieur.append(job)
    return copieur

#deuxieme etape de la méthode
def MethodeNEH(Flowshop):
    ListeJob=OrdonnerListe(Flowshop.l_job)
    NbJob = Flowshop.nb_jobs
    NbMachine=Flowshop.nb_machines

    OrdoFinal=[]
    OrdoTest=[]
    OrdoTestmin=[]
    DureeMin=0
    """boucle sur les Jobs"""
    for i in range(0,NbJob):
        """boucle sur les emplacements possibles"""
        for j in range(0,i+1):
            OrdoTest = CopyJobs(OrdoFinal)
            if j == 0:
                """initialisation du premier test qui est au début posé comme le minimum des tests pour cette étape"""
                OrdoTestmin.insert(j, ListeJob[i])
                Test=ordonnancement.Ordonnancement(NbMachine)
                Test.ordonnancer_liste_job(OrdoTestmin)
                DureeMin =Test.duree
            else :
                OrdoTest.insert(j, ListeJob[i])
                Test = ordonnancement.Ordonnancement(NbMachine)
                Test.ordonnancer_liste_job(OrdoTest)
                DureeTest= Test.duree
                if DureeMin < DureeTest :
                    OrdoTestmin = OrdoTest
                    DureeMin = DureeTest
        """OrdoFinal= ordo le plus performant à cette étape"""

        OrdoFinal = CopyJobs(OrdoTestmin)

    Flowshop.l_job = OrdoFinal
    OrdonnancementComplet = (ordonnancement.Ordonnancement(NbMachine))
    OrdonnancementComplet.ordonnancer_liste_job(OrdoFinal)
    OrdonnancementComplet.afficher()
    return OrdonnancementComplet
