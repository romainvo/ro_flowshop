#!/usr/bin/env python
# coding: utf-8

""" Classe Job """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

class Job():
    """ Classe modélisant un job dans un problème de flowshop de permutation. 
    
    Attributes:
        numero (int): Numéro du Job.

        nb_op (int): Nombre d'opérations à effectuer pour ce Job.

        duree_op (list<float>): Liste des durées corespondant à chaque opération.

        date_deb (list<float>): List des dates de début des opérations lorsque le
        Job est ordonnancé.

        duree_job (float): Somme des durées de chaque opération.
    
    """

    def __init__(self, numero : int, tab_durees=[]):
        """ Initialise un Job.

        Parameters:
            numero (int): Numéro du Job.

        Keyword arguments:
            tab_durees (list<float>): Vide par défaut, contient les durées
            correspondant à chaque opération.
            
        """

        # numéro du job
        self.numero = numero
        # nombre d'opérations
        self.nb_op = len(tab_durees)
        # durées des opérations
        self.duree_op = [i for i in tab_durees]
        # date de début des opérations quand le job est ordonnancé
        self.date_debut = [None for i in tab_durees]
        # durée totale du job
        self.duree_job = self.calculer_duree_job()

    def duree_operation(self, operation):
        """ Retourne la durée de l'opération demandée.

        Parameters:
            operation (int): Numéro de l'opération.
            
        """
        return self.duree_op[operation]

    def afficher(self):
        print("Job", self.numero,"de durée totale", self.duree_job, ":")
        for num in range(len(self.duree_op)):
            duree = self.duree_op[num]
            debut = self.date_debut[num]
            print("  opération", num, ": durée =", duree, "début =", debut)       

    def calculer_duree_job(self):
        return sum(self.duree_op)    

# "main" pour tester la classe
if __name__ == "__main__":
    a = Job(1,[1,3,5,18,23])
    a.afficher()