from flowshop import Flowshop
from job import Job
from ordonnancement import Ordonnancement

import random
import numpy as np
from copy import deepcopy

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

    """

    def __init__(self, flowshop : Flowshop, piste):
        """ Initialise un objet Fourmi.
        
        Parameters:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            piste (Piste): Instance d'une piste, aggrège les principales caractéristiques
            de la piste parcourue par les fourmis.
                        
        """
        
        self.piste = piste
        self.flowshop = flowshop
        self.ordonnancement = Ordonnancement(flowshop.nb_machines)

        self.elitiste = False

        self.jobs_non_visites = flowshop.l_job.copy()
        
        self.bool_jobs_non_visites = np.ones(flowshop.nb_jobs, dtype=bool)

        self.passage_sur_arc = np.zeros((flowshop.nb_jobs, flowshop.nb_jobs), dtype=bool)
        
        #On intialise la ville de départ de la fourmi (job)
        self.ajouter_job_visite(random.choice
                (self.jobs_non_visites))

    def ajouter_job_visite(self, job : Job):
        """ Ajoute à l'ordonnancement le job visité et supprime ce dernier de la liste
        des jobs non visites.

        Attributes:
            job (Job): Job visité par la fourmi durant l'itération.

        """
                
        if self.get_dernier_job_visite() != -1:
            self.passage_sur_arc[self.get_dernier_job_visite()][job.numero] = True

        self.ordonnancement.ordonnancer_job(job)

        self.bool_jobs_non_visites[job.numero] = False

        indice = self.jobs_non_visites.index(job)
        del self.jobs_non_visites[indice]

    def get_dernier_job_visite(self):
        """ Retourne le numéro du dernier job visité. """

        if len(self.ordonnancement.sequence) == 0:
            return -1
        else:
            return self.ordonnancement.sequence[-1].numero

    def set_job_suivant(self):
        """ Calcule le prochain Job à visiter pour la fourmi et ajoute ce job
        à l'instance d'Ordonnancement.
        
        Note:
            Appelle la fonction ajouter_job_visite.
            
        """

        proba_jobs_non_visites = []

        i = self.get_dernier_job_visite()

        for job in self.jobs_non_visites:
            self.piste.pheromone_closeness_products[i, job.numero] \
            = self.__get_pheromone_closeness_product(i, job.numero)
        
        for job in self.jobs_non_visites:
            proba_jobs_non_visites.append(
                self.get_proba(self.get_dernier_job_visite()
                , job.numero))

        job_suivant = np.random.choice(self.jobs_non_visites, p=proba_jobs_non_visites)
        self.ajouter_job_visite(job_suivant)
        
    def __get_pheromone_closeness_product(self, i : int, j : int):
        
        ordonnancement_temp = deepcopy(self.ordonnancement)
        ordonnancement_temp.ordonnancer_job(self.flowshop.l_job[j])
        
        delta_ij = ordonnancement_temp.duree - self.ordonnancement.duree 
        
        pcp = pow(self.piste.pheromone_sur_arc[i][j], Piste.ALPHA) \
            * pow(1.0 / delta_ij, Piste.BETA)
            
        return pcp
    
    def get_proba(self, i : int, j : int):
        """ Calcule la probabilité pour une fourmi d'aller d'un Job i à un Job J.

        Attributes:
            i (int): Numéro du Job de départ

            j (int): Numéro du Job d'arrivée
        """
                
        num = self.piste.pheromone_closeness_products[i,j]
        den = np.sum(self.piste.pheromone_closeness_products[i, self.bool_jobs_non_visites])
        
        return num/den
    
        """
        
        ordonnancement_temp = deepcopy(self.ordonnancement)
        ordonnancement_temp.ordonnancer_job(self.flowshop.l_job[j])
        
        delta_ij = ordonnancement_temp.duree - self.ordonnancement.duree
        
        num = pow(self.piste.pheromone_sur_arc[i][j], Piste.ALPHA) \
            * pow(1.0 / delta_ij, Piste.BETA)
        den = 0
        
        for job in self.jobs_non_visites:
            
            ordonnancement_temp = deepcopy(self.ordonnancement)
            ordonnancement_temp.ordonnancer_job(self.flowshop.l_job[j])
            
            delta_ij = ordonnancement_temp.duree - self.ordonnancement.duree
            
            den += pow(self.piste.pheromone_sur_arc[i][job.numero], Piste.ALPHA) \
                * pow(1.0 / delta_ij, Piste.BETA)

        return num / den           
        """
        
from piste import Piste