from flowshop import Flowshop
from fourmi import Fourmi
from job import Job
from ordonnancement import Ordonnancement
import NEH
import random
import numpy as np
import time

class Piste() :
    """ Classe modélisant une piste parcourue par des fourmis.
    
    Attributes:
        flowshop (Flowshop): Instance d'un problème de flowshop de permutation

        pheromone_sur_arc (numpy.array<float>): Stocke la quantité de phéromone présente
        sur chaque segment/arc de la piste.

        cbest (float): Plus courte distance totale parcourue par une des fourmis.

        nombre_fourmis (int): Nombre de fourmis parcourant la piste.

        liste_fourmis (list<Fourmi>): Liste contenant l'ensemble des Fourmi parcourant 
        la Piste.
            
    """

    ALPHA = 1
    BETA = 2
    Q = 100
    P = 0.5
    ELITISTE = True
    NOMBRE_ELITISTE = 20
    COEF_ELITISTE = 10
    MAX_TIME = 60
    C_INI_PHEROMONE = 0.1
    NOMBRE_FOURMIS = 10

    def __init__(self, flowshop : Flowshop, nombre_fourmis=NOMBRE_FOURMIS):
        """ Initialise un objet Piste.
        
        Parameters:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            nombre_fourmis (int): Nombre de fourmis parcourant la piste.
                        
        """

        self.flowshop = flowshop
        self.pheromone_sur_arc = self.C_INI_PHEROMONE * np.ones((flowshop.nb_jobs, flowshop.nb_jobs))
        self.cbest = -1
        self.solution_temp = []
        self.nombre_fourmis = nombre_fourmis

        self.liste_fourmis = [Fourmi(self.flowshop, self) for i in range(0, self.nombre_fourmis)]


    #------------------------------------------------------------
    # Methods                                                   ||
    #------------------------------------------------------------

    def maj_pheromone(self):
        """ Met a jour la quantite de pheromones en fonction du cmax 
        parcouru par les fourmis ainsi qu'en fonction du coefficient d'evaporation
        P des pheromones
        Plus l'ordre des jobs parcouru est faible, plus la quantite de pheromones deposee est importante
        """

        for i in range(0, self.flowshop.nb_jobs):
            for j in range(0,i):
                self.pheromone_sur_arc[i][j] = self.P * self.pheromone_sur_arc[i][j]
                for fourmi in self.liste_fourmis:
                    if fourmi.elitiste:
                        self.pheromone_sur_arc[i][j] \
                            += fourmi.passage_sur_arc[i][j] * self.COEF_ELITISTE * (self.Q/ fourmi.ordonnancement.duree)
                    else:
                        self.pheromone_sur_arc[i][j] \
                            += fourmi.passage_sur_arc[i][j] * (self.Q / fourmi.ordonnancement.duree)
               
                    self.pheromone_sur_arc[j][i] = self.pheromone_sur_arc[i][j]

    def maj_best_solution(self):
        best = self.liste_fourmis[0].ordonnancement.duree
        best_fourmi = self.liste_fourmis[0]
        for fourmi in self.liste_fourmis:
            if fourmi.ordonnancement.duree < best:
                best = fourmi.ordonnancement.duree
                best_fourmi = fourmi

        if self.cbest < 0:
            self.cbest = best
            self.solution_temp = best_fourmi.ordonnancement

        elif self.cbest > best:
            self.cbest = best
            self.solution_temp = best_fourmi.ordonnancement

    def reset_fourmis(self):
        """ Apres un tour complet la memoire de chaque fourmi est reinitialisee

        """

        self.liste_fourmis.clear()
        self.liste_fourmis = [Fourmi(self.flowshop, self) for i in range(0, self.nombre_fourmis)]

    def appliquer_NEH(self):
        for i in range(self.nombre_fourmis) :
            seuil = random.randint(0,100)
            if seuil < 10 :
                ordo_actuel = self.liste_fourmis[i].ordonnancement
                ordo_NEH = NEH.MethodeNEH(ordo_actuel)
                if ordo_NEH.duree < ordo_actuel.duree :
                    self.liste_fourmis[i].ordonnancement=ordo_NEH

    def set_elitiste(self, nombre : int):

        for i in range(nombre):
            best = self.liste_fourmis[0].ordonnancement.duree
            best_fourmi = self.liste_fourmis[0]

            for j in range(len(self.liste_fourmis)):
                if (self.liste_fourmis[j].ordonnancement.duree < best \
                    and not self.liste_fourmis[j].elitiste):
                    best = self.liste_fourmis[j].ordonnancement.duree
                    best_fourmi = self.liste_fourmis[j]
			
            best_fourmi.elitiste = True

            if i == 0:
                if self.cbest < 0:
                    self.cbest = best
                    self.solution_temp = best_fourmi.ordonnancement			
                elif self.cbest > best:
                    self.cbest = best
                    self.solution_temp = best_fourmi.ordonnancement	


if __name__ == "__main__":
    
    flowshop = Flowshop()
    flowshop.definir_par("jeu_donnees_2/tai52.txt")
    print("nb machine = ", flowshop.nb_machines)
    print("nb job = " , flowshop.nb_jobs)

    piste = Piste(flowshop)

    start_time = time.time()
    spent_time = 0
    index = 0
		
    while True: 

        #Initialise la première ville de chaque fourmi
        for k in range(len(piste.liste_fourmis)):
            piste.liste_fourmis[k].ajouter_job_visite(
                random.choice
                (piste.liste_fourmis[k].jobs_non_visites))

        for k in range(len(piste.liste_fourmis)):
            for i in range(len(piste.liste_fourmis[k].jobs_non_visites)):
                piste.liste_fourmis[k].set_job_suivant()	
        
        piste.appliquer_NEH()

        if piste.ELITISTE:
            piste.set_elitiste(piste.NOMBRE_ELITISTE)
        else:
            piste.maj_best_solution()

        piste.maj_pheromone()
        piste.reset_fourmis()

        spentTime = time.time() - start_time
        index += 1

        print("Itération : {} - {} ".format(index, piste.cbest))

        piste.solution_temp.afficher()
        print("Meilleur chemin : {}".format(piste.cbest))

        if spentTime > 60:
            print("Nombre d'itérations : {}".format(index))
            break 

