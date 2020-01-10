from flowshop import Flowshop
import job
import ordonnancement

import random
import numpy as np

pb = Flowshop()           #associe à pb la classe Flowshop
pb.definir_par("jeu1.txt")      #défini pb par le jeu1
for i in range(pb.nb_jobs):
    j = pb.liste_jobs(i)
    j.afficher()
N = pb.nombre_jobs()    #nombre de jobs
F = N                   #nombre de fourmis
"""print (N,F)

visiterIterAvant = [[0 for j in range(N)] for i in range(F)]
print (visiterIterAvant)

visiterIterNow = [[0 for j in range(N)] for i in range(F)]
print (visiterIterNow)

avisiter #liste des jobs restants à être visités pour chaque fourmi

visibilite = np.zeros((N,N))
# remplir la matrice visibilite avec l'inverse des durées pour chaque job et chaque operation

pheromones = np.zeros((N,N)) #initialement il n'y a pas de pheromones déjà déposées entre les jobs

pherotrajet = np.zeros((N,N))  #initialement il n'y a pas de pheromones à déposer entre les jobs

probadevisite = [1 for i in range(N)]  #initialement chaque job a une proba de 1 de visite pour chaque fourmi"""

class Fourmi():
    def __init__(self,jobsNonVisites,jobsVisites,m_flowshop,cmax,passageSurArc,piste):
        self.jobsNonVisites = jobsNonVisites
        self.jobsVisites = jobsVisites
        self.m_flowshop = m_flowshop
        self.cmax = cmax
        self.passageSurArc = passageSurArc
        self.piste = piste

    def jobsNV(self):
        return self.jobsNonVisites

    def jobsV(self):
        return self.jobsVisites

    def completion(self):
        return self.cmax

    def passeSurArc(self):
        return self.passageSurArc

    def chemin(self):
        return self.piste

    def Fourmi(m_flowshop,piste):
        self.piste = piste
        self.m_flowshop = m_flowshop
        self.jobsNonVisites = []
        for i in range N:
            self.jobsNonVisites.append(i)
        self.jobsVisites = []
        self.passageSurArc = [[0 for i in range N] for j in range N]
        for i in range N:
            for j in range i+1:
                self.passageSurArc[i][j]=0
                self.passageSurArc[j][i]=0

    def getPiste():
        return self.piste

    def getJobsNonVisites():
        return self.jobsNonVisites

    def getJobsVisites():
        return self.jobsVisites

    def getPassage():
        return self.passageSurArc

    def getCmax():
        return self.cmax

    def getFlowshop():
        return self.m_flowshop

    def ajouterJobsVisites(numeroJob):
        if self.getDernierJobVisite()!=-1:
            self.getPassage()[self.getDernierJobVisite()][numeroJob]=1
        self.jobsVisites.append(numeroJob)
        indice = self.jobsNonVisites.index(numeroJob)
        del self.jobsNonVisites[indice]

    def getDernierJobVisite():
        if len(self.getJobsVisites())==0:
            return -1
        else:
            return self.getJobsVisites()[-1]

    def setProchainJob():
        test = false
        x = random.random()
        sommeDesProba = 0
        k = 0
        while test!=true and k<len(self.getJobsNonVisites):
            sommeDesProba = sommeDesProba + self.getProbaIaJ(self.getDernierJobVisite(),self.getJobsNonVisites[k])
            if x<=sommeDesProba:
                self.ajouterJobsVisites(self.getJobsNonVisites[k])
                test = true
            k+= 1
    
    def getProbaIaJ(i,j):
        l = Ordonnancement(self.pb.nombre_machines())
        l.ordonnancer_liste_job([i,j])
        self.cmax = l.duree()
        num = pow(self.getPiste().getPheromoneSurArc()[i][j],Piste.ALPHA)*pow(1.0/self.m_flowshop.,Piste.BETA)
        den = 0
        for numJob in self.getJobsNonVisites():
#            den = den + pow(self.getPiste().getPheromoneSurArc()[i][numJob],Piste.ALPHA)*pow(1.0/self.####################,Piste.BETA)
        return (num/den)

    def setCmax():
        l = Ordonnancement(self.pb.nombre_machines())
        l.ordonnancer_liste_job(self.getJobsVisites)
        self.cmax = l.duree()