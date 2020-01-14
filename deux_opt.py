import job,flowshop,ordonnancement


def deux_opt(ordo):
    nb_machines = ordo.nb_machines
    nb_jobs = len(ordo.seq)
    print("NOMBRE DE JOBS : " + str(nb_jobs))
    for i in range(nb_jobs):
        for j in range(i+1,nb_jobs):
            sequence = ordo.seq
            new_sequence=changement_parcours(sequence,i,j)
            new_ordo = ordonnancement.Ordonnancement(nb_machines)
            new_ordo.ordonnancer_liste_job(new_sequence)
            if new_ordo.dur<ordo.dur:
                ordo=new_ordo
    return ordo

def changement_parcours(sequence,i,j):
    new_sequence = sequence.copy()
    if i<j :
        a=i
        b=j
    else : 
        a=j
        b=i
    while (a<b):
        new_sequence[a]=sequence[b]
        new_sequence[b]=sequence[a]
        a=a+1
        b=b-1
    return new_sequence
