from flowshop import Flowshop
import job
import ordonnancement

import numpy as np

pb = Flowshop()           #associe à pb la classe Flowshop
pb.definir_par("jeu1.txt")      #défini pb par le jeu1
for i in range(pb.nb_jobs):
    j = pb.liste_jobs(i)
    j.afficher()
N = pb.nombre_jobs()    #nombre de jobs
F = N                   #nombre de fourmis
print (N,F)

visiterIterAvant = [[0 for j in range(N)] for i in range(F)]
print (visiterIterAvant)

visiterIterNow = [[0 for j in range(N)] for i in range(F)]
print (visiterIterNow)

avisiter #liste des jobs restants à être visités pour chaque fourmi

visibilite = np.zeros((N,N))
# remplir la matrice visibilite avec l'inverse des durées pour chaque job et chaque operation

pheromones = np.zeros((N,N)) #initialement il n'y a pas de pheromones déjà déposées entre les jobs

pherotrajet = np.zeros((N,N))  #initialement il n'y a pas de pheromones à déposer entre les jobs

probadevisite = [1 for i in range(N)]  #initialement chaque job a une proba de 1 de visite pour chaque fourmi