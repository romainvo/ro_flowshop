import job,flowshop,ordonnancement

def deux_opt(ordo):
    nb_machines = ordo.nb_machines
    nb_jobs = len(ordo.sequence)
    for i in range(nb_jobs):
        for j in range(i+1,nb_jobs):
            sequence = ordo.sequence
            new_sequence=changement_parcours(sequence,i,j)
            new_ordo = ordonnancement.Ordonnancement(nb_machines)
            new_ordo.ordonnancer_liste_job(new_sequence)
            if new_ordo.duree<ordo.duree:
                ordo=new_ordo
    return ordo

def changement_parcours(sequence,i,j):
    a=min(i,j)
    b=max(i,j)
    while (a<b):
        inter=sequence[a]
        sequence[a]=sequence[b]
        sequence[b]=inter
        a=a+1
        b=b-1
    return sequence
