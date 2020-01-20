from flowshop import Flowshop
from fourmi import Fourmi
from job import Job
from ordonnancement import Ordonnancement
import NEH, deux_opt
import random
import numpy as np
import time

class Piste() :
    """ Classe modélisant une piste parcourue par des fourmis.
    
    Attributes:
        flowshop (Flowshop): Instance d'un problème de flowshop de permutation

        pheromone_sur_arc (numpy.array<float>): Stocke la quantité de phéromone présente
        sur chaque segment/arc de la piste.
        
        pheromone_closeness_products (numpy.array<float>): Stocke le produit de
        la quantité de phéromone présente sur chaque segment et de l'inverse de 
        la longueur de ce segment

        cbest (float): Plus courte distance totale parcourue par une des fourmis.

        nombre_fourmis (int): Nombre de fourmis parcourant la piste.

        liste_fourmis (list<Fourmi>): Liste contenant l'ensemble des Fourmi parcourant 
        la Piste.
            
    """

    ALPHA = 1
    BETA = 2
    Q = 1
    P = 0.5

    ELITISTE = False
    TAUX_ELITISTE = 0.10
    COEF_ELITISTE = 10
    MAX_TIME = 60
    C_INI_PHEROMONE = 1e-8
    NOMBRE_FOURMIS = 40

    def __init__(self, flowshop : Flowshop, nombre_fourmis=NOMBRE_FOURMIS):
        """ Initialise un objet Piste.
        
        Parameters:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            nombre_fourmis (int): Nombre de fourmis parcourant la piste.
                        
        """

        self.flowshop = flowshop
        self.pheromone_sur_arc = self.C_INI_PHEROMONE * np.ones((flowshop.nb_jobs, flowshop.nb_jobs))
        self.pheromone_closeness_products = np.zeros((flowshop.nb_jobs, flowshop.nb_jobs))
        self.cbest = -1
        self.solution_temp = []
        self.nombre_fourmis = nombre_fourmis

        self.liste_fourmis = [Fourmi(self.flowshop, self) for i in range(0, self.nombre_fourmis)]

    #------------------------------------------------------------
    # Methods                                                   ||
    #------------------------------------------------------------
               
    def maj_best_solution(self):
        
        best_fourmi = min(self.liste_fourmis,
                          key=lambda fourmi: fourmi.ordonnancement.duree)
        
        cbest = best_fourmi.ordonnancement.duree

        if self.cbest < 0:
            self.cbest = cbest
            self.solution_temp = best_fourmi.ordonnancement

        elif self.cbest > cbest:
            self.cbest = cbest
            self.solution_temp = best_fourmi.ordonnancement

    def set_elitiste(self, taux : float):
        
        self.liste_fourmis = sorted(self.liste_fourmis,
                                    key=lambda fourmi: fourmi.ordonnancement.duree,
                                    reverse=False)
        
        if self.cbest < 0:
            self.cbest = self.liste_fourmis[0].ordonnancement.duree
            self.solution_temp = self.liste_fourmis[0].ordonnancement
            
        elif self.cbest > self.liste_fourmis[0].ordonnancement.duree:
            self.cbest = self.liste_fourmis[0].ordonnancement.duree
            self.solution_temp = self.liste_fourmis[0].ordonnancement           
        
        for i in range(int(self.nombre_fourmis * taux)):
            self.liste_fourmis[i].elitiste = True

    def maj_pheromone(self):
        """ Met a jour la quantite de pheromones en fonction du cmax 
        parcouru par les fourmis ainsi qu'en fonction du coefficient d'evaporation
        P des pheromones
        Plus l'ordre des jobs parcouru est faible, plus la quantite de pheromones deposee est importante
        """

        self.pheromone_sur_arc = self.P * self.pheromone_sur_arc
        for fourmi in self.liste_fourmis:
            if fourmi.elitiste:
                self.pheromone_sur_arc \
                    += fourmi.passage_sur_arc * self.COEF_ELITISTE * (self.Q / fourmi.ordonnancement.duree)
            else:
                self.pheromone_sur_arc \
                    += fourmi.passage_sur_arc * (self.Q / fourmi.ordonnancement.duree)

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

    def appliquer_2_opt(self):
        for i in range(self.nombre_fourmis) :
            seuil = random.randint(0,100)
            if seuil < 10 :
                ordo_actuel = self.liste_fourmis[i].ordonnancement
                ordo_2_opt = deux_opt.deux_opt(ordo_actuel)
                if ordo_2_opt.duree < ordo_actuel.duree :
                    self.liste_fourmis[i].ordonnancement = ordo_2_opt  

if __name__ == "__main__":
    
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
    
        if spentTime > 30:
            print("Nombre d'itérations : {}".format(index))
            break 

