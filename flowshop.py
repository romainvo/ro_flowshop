#!/usr/bin/env python
# coding: utf-8

"""Résolution du flowshop de permutation : 
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement
import NEH, deux_opt
import time

class Flowshop():
    """ Classe modélisant un problème de flowshop de permutation. 
    
    Attributes:
        nb_jobs (int): Nombre de jobs dans le problème.

        nb_machines (int): Nombre de machine dans le problème.

        l_job (list<Job>): Liste contenant les objets Job.

    """

    def __init__(self, nb_jobs=0, nb_machines=0, l_job=None):
        """ Initialise une instance de Flowshop.
        
        Keyword arguments:
            nb_jobs (int): Nombre de jobs dans le problème.

            nb_machines (int): Nombre de machine dans le problème.

            l_job (list<Job>): Liste contenant les objets Job.
                        
        """
        self.nb_jobs = nb_jobs
        self.nb_machines = nb_machines
        self.l_job = l_job

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline() 
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])

        self.l_job = []
        for i in range(self.nb_jobs):
            ligne = fdonnees.readline() 
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()

if __name__ == "__main__":

    prob = Flowshop()
    prob.definir_par("tai52.txt")
    print("nb machine = ",prob.nb_machines)
    print("nb job = " ,prob.nb_jobs)
    start_time = time.time()
    ordo_NEH = NEH.MethodeNEH(prob)
    print("Temps d'éxécution NEH : " + str((time.time()-start_time)))

   # prob.definir_par("jeu_donnees_1/tai51.txt")
   # print("nb machine = ",prob.nb_machines)
   # print("nb job = " ,prob.nb_jobs)
    #NEH.MethodeNEH(prob)

    # Test 2-opt
    start_time = time.time()
    new_ordo = deux_opt.deux_opt(ordo_NEH)
    print("\n Test de 2-opt :")
    new_ordo.afficher()
    print("Temps d'éxécution 2opt : " + str((time.time()-start_time)))
