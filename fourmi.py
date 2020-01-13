from flowshop import Flowshop
from piste import Piste
from job import Job
from ordonnancement import Ordonnancement

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
    """ Classe modélisant une fourmi.
    
    Attributes:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            piste (Piste): Instance d'une piste, aggrège les principales caractéristiques
            de la piste parcourue par les fourmis.

            ordonnancement (Ordonnancement): Chemin pris par la fourmi.

            jobs_non_visites (list<Job>): Liste des jobs encore non ordonnancés.

            passage_sur_arc (numpy.array<bool>): Une case vaut True si la fourmi a emprunté
            l'arc correspondant.

            cmax (float): Distance totale parcourue par la fourmi, 
            ou durée totale de l'ordonnancement.

    """

    def __init__(self, flowshop : Flowshop, piste : Piste):
        """ Initialise un objet Fourmi.
        
        Note: 
            bla bla bla
        
        Parameters:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            piste (Piste): Instance d'une piste, aggrège les principales caractéristiques
            de la piste parcourue par les fourmis.
        
        Keyword arguments:
            bla bla bla
                        
        """
        self.piste = piste
        self.flowshop = flowshop
        self.ordonnancement = Ordonnancement(flowshop.nb_machines)

        self.jobs_non_visites = flowshop.l_job.copy()

        self.passage_sur_arc = np.zeros((flowshop.nb_jobs, flowshop.nb_jobs), dtype=bool)

    def ajouter_job_visite(self, job : Job):
        """ Ajoute à l'ordonnancement le job visité et supprime ce dernier de la liste
        des jobs non visites.

        Attributes:
            job (Job): Job visité par la fourmi durant l'itération.

        """
        if self.get_dernier_job_visite() != -1:
            self.passage_sur_arc[self.get_dernier_job_visite()][job.num] = True

        self.ordonnancement.ordonnancer_job(job)

        indice = self.jobs_non_visites.index(job)
        del self.jobs_non_visites[indice]

    def get_dernier_job_visite(self):
        """ Retourne le numéro du dernier job visité. """

        if len(self.ordonnancement.seq) == 0:
            return -1
        else:
            return self.ordonnancement.seq[-1].num

    def set_job_suivant(self):
        """ Calcule le prochain Job à visiter pour la fourmi. """

        proba_jobs_non_visites = []

        for job in self.jobs_non_visites:
            proba_jobs_non_visites.append(
                self.get_proba(self.get_dernier_job_visite()
                , job))

        job_suivant = np.random.choice(self.jobs_non_visites, p=proba_jobs_non_visites)
        self.ajouter_job_visite(job_suivant)
    
    def get_proba(self, i : int, j : int):
        """ Calcule la probabilité pour une fourmi d'aller d'un Job i à un Job J.

        Attributes:
            i (int): Numéro du Job de départ

            j (int): Numéro du Job d'arrivée
        """
        num = pow(self.piste.pheromone_sur_arc[i][j], Piste.ALPHA) * pow(1.0, Piste.BETA)
        den = 0
        for num_job in self.jobs_non_visites():
            den = den + pow(self.piste.pheromone_sur_arc[i][num_job], Piste.ALPHA) \
                * pow(1.0, Piste.BETA)

        return num / den            

    def set_cmax(self):
        self.cmax = self.ordonnancement.dur