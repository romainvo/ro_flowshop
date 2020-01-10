import flowshop,job,ordonnancement,fourmi

class Piste() :

    ALPHA = 1
    BETA = 2
    Q = 100
    P = 0.2
    ELITISTE = True
    NOMBRE_ELITISTE = 20
    COEF_ELITISTE = 10
    MAX_TIME = 60
    c_ini_pheromone = 0.1
    NOMBRE_FOURMI = 101

    def __init__(self,flowshop):

        self.fs = flowshop;
        self.pheromoneSurArc = [[]]
        self.bestLongueur = -1
        self.solutionTemp = []
        self.listeFourmis = []
        for i in range(0,self.fs.nombre_jobs()):
            for j in range(0,i):
              self.pheromoneSurArc[i][j]=self.c_ini_pheromone
              self.pheromoneSurArc[j][i]=self.pheromoneSurArc[i][j]

        self.nombreFourmi = self.NOMBRE_FOURMI
        for i in range(0,self.nombreFourmi):
            self.listeFourmis.append(fourmi.Fourmi(self.fs,self))

    #------------------------------------------------------------
    # Methods                                                   ||
    #------------------------------------------------------------

    def getFlowshop(self):
        return self.fs

    def getFourmi(self,index):
        return self.getFourmi()[index]

    def getFourmis(self):
        return self.getFourmi()

    def getPheromonesSurArc(self):
        return self.pheromoneSurArc

    def getBestLongueur(self):
        return self.bestLongueur

    def getSolutionTemp(self):
        return self.solutionTemp

    def majPheromone(self):
        for i in range(0,self.fs.nombre_jobs()):
            for j in range(0,i):
                self.getPheromoneSurArc()[i][j]=self.P * self.getPheromoneSurArc()[i][j];
                for four in self.getFourmis():
                    if not four.getElitiste():
                        self.getPheromoneSurArc()[i][j] += four.getPassage()[i][j]*(self.Q / four.getCmax())
                else:
                    self.getPheromoneSurArc()[i][j]+= four.getPassage()[i][j] * self.COEF_ELITISTE * (self.Q / four.getCmax())
                self.getPheromoneSurArc()[j][i] = self.getPheromoneSurArc()[i][j];

    def majBestSolution(self):
        best = self.getFourmi(0).getCmax();
        bestF = self.getFourmi(0);
        for four in self.getFourmis():
            if four.getCmax() < best:
                best = four.getCmax();
                bestF = four;
        if self.getBestCmax() < 0:
            self.bestCmax=best;
            self.solutionTemp=bestF.getJobsVisitees();
        elif self.getBestCmax() > best:
            self.bestLongueur=best;
            self.solutionTemp=bestF.getJobsVisitees();

    def resetFourmis(self):
        self.listeFourmis.clear();
        self.listeFourmis = [];
        for i in range(0,self.getFlowshop().nombre_jobs()):
            self.listeFourmis.add(fourmi.Fourmi(self.getFlowshop(), self));
