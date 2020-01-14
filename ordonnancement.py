#!/usr/bin/env python
# coding: utf-8

""" Classe Ordonnancement """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job

class Ordonnancement():
    """ Classe modélisant l'ordonancement d'un problème de flowshop de permutation.

    Attributes:
        seq (list<Job>): Liste ordonnée de Job correspondant à leur séquencement.

        nb_machines (int): Nombre de machine dans le problème.

        duree (float): Durée totale de l'ordonnancement - Cmax.

        date_dispo(list<float>): Date à partir de laquelle chaque machine est libre.

    """

    # constructeur pour un ordonnancement vide
    def __init__(self, nb_machines : int):
        """ Initialise une instance d'Ordonnancement.

        Attributes:
            nb_machines (int): Nombre de machine dans le problème.

        """

        # séquence des jobs
        self.sequence = []
        # nombre de machiners
        self.nb_machines = nb_machines
        # durée totale de l'ordonnancement
        self.duree = 0
        # date à partir de laquelle chaque machine est libre
        self.date_dispo = [0 for i in range(self.nb_machines)]
    
    def date_disponibilite(self, num_machine):
        """ Retourne la date de disponibilité de la machine 'num_machine'.

        Attributes:
            num_machine (int): Numéro de la machine.

        """

        return self.date_dispo[num_machine]

    def date_debut_operation(self, job, operation):
        """ Retourne la date de début de début d'une opération d'un job.

        Attributes:
            job (Job): 

            operation (int): Numéro de l'opération

        """

        return job.date_debut[operation]

    def fixer_date_debut_operation(self, job, operation, date):
        job.date_debut[operation] = date

    def afficher(self):
        print("Ordre des jobs :", end='')
        for job in self.sequence:
            print(" ",job.numero," ", end='')
        print()
        for job in self.sequence:
            print("Job", job.numero, ":", end='')
            for mach in range(self.nb_machines):
                print(" op", mach, "à t =", self.date_debut_operation(job, mach),"|", end='')
            print()
        print("Cmax =", self.duree)

    # ajoute un job dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_job(self, job):
        self.sequence += [job]
        for mach in range(self.nb_machines):
            if mach == 0:   # première machine
                self.fixer_date_debut_operation(job, 0, self.date_dispo[0])
            else:   # machines suivantes
                date = max(self.date_dispo[mach-1], self.date_dispo[mach])
                self.fixer_date_debut_operation(job, mach, date)
            self.date_dispo[mach] = self.date_debut_operation(job, mach) + \
            job.duree_operation(mach)
        self.duree = max(self.duree, self.date_dispo[self.nb_machines-1])

    # ajoute les jobs d'une liste dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_liste_job(self, liste_jobs):
        for job in liste_jobs:
            self.ordonnancer_job(job)

# "main" pour tester la classe   
if __name__ == "__main__":
    a = job.Job(1,[1,1,1,1,10])
    b = job.Job(2,[1,1,1,4,8])
    a.afficher()
    b.afficher()
    l = [a,b]
    ordo = Ordonnancement(5)
    ordo.ordonnancer_job(a)
    ordo.ordonnancer_job(b)
    ordo.sequence
    ordo.afficher()
    a.afficher()
    b.afficher()
