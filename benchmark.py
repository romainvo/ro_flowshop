# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:00:35 2020

@author: romain
"""

from flowshop import Flowshop
from piste import Piste
from job import Job
from ordonnancement import Ordonnancement
import NEH, deux_opt
import random
import numpy as np
import time

flowshop = Flowshop()
flowshop.definir_par("jeu_donnees_2/tai02.txt")
print("nb machine = ", flowshop.nb_machines)
print("nb job = " , flowshop.nb_jobs)

piste = Piste(flowshop)

start_time = time.time()
spent_time = 0
index = 0
		
while True: 

    for k in range(len(piste.liste_fourmis)):
        for i in range(len(piste.liste_fourmis[k].jobs_non_visites)):
            piste.liste_fourmis[k].set_job_suivant()	
    
    piste.appliquer_2_opt()
    #piste.appliquer_NEH()

    if piste.ELITISTE:
        piste.set_elitiste(piste.TAUX_ELITISTE)
    else:
        piste.maj_best_solution()

    piste.maj_pheromone()
    piste.reset_fourmis()

    spentTime = time.time() - start_time
    index += 1

    print("Itération : {} - {} ".format(index, piste.cbest))
    print(piste.pheromone_sur_arc)
    piste.solution_temp.afficher()
    print("Meilleur chemin : {}".format(piste.cbest))

    if spentTime > 600:
        print("Nombre d'itérations : {}".format(index))
        break 