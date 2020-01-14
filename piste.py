from flowshop import Flowshop
from fourmi import Fourmi
from job import Job
from ordonnancement import Ordonnancement

import random
import numpy as np

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
    P = 0.2
    ELITISTE = True
    NOMBRE_ELITISTE = 20
    COEF_ELITISTE = 10
    MAX_TIME = 60
    C_INI_PHEROMONE = 0.1
    NOMBRE_FOURMIS = 101

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

        for i in range(0,self.flowshop.nombre_jobs()):
            for j in range(0,i):
                self.pheromone_sur_arc[i][j]=self.P * self.pheromone_sur_arc[i][j]
                for fourmi in self.liste_fourmis:
                    self.pheromone_sur_arc[i][j] \
                    += fourmi.passage_sur_arc[i][j] * (self.Q / fourmi.cmax)
               
                    self.pheromone_sur_arc[j][i] = self.pheromone_sur_arc[i][j]

    def majBestSolution(self):
        """ Met a jour le meilleur ordre des jobs et son cmax

        """

        best = self.liste_fourmis[0].cmax
        best_fourmi = self.liste_fourmis[0]
        for fourmi in self.liste_fourmis:
            if fourmi.cmax < best:
                best = fourmi.cmax
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