from OPASolver import OPASolver
if __name__ == '__main__':
    opa = OPASolver()
    opa.addExpert("E1",1)
    opa.addExpert("E2",3)
    opa.addExpert("E3",2)
    
    opa.addCriteria("c1")
    opa.addCriteria("c2")
    opa.addCriteria("c3")

    opa.addAlernative("A")
    opa.addAlernative("B")

    opa.rankingCriterias("E1","c1",1)
    opa.rankingCriterias("E1","c2",3)
    opa.rankingCriterias("E1","c3",2)
    opa.rankingCriterias("E2","c1",2)
    opa.rankingCriterias("E2","c2",3)
    opa.rankingCriterias("E2","c3",1)
    opa.rankingCriterias("E3","c1",1)
    opa.rankingCriterias("E3","c2",2)
    opa.rankingCriterias("E3","c3",3)
    #print(opa.expertsCriterias)
    
    opa.rankingAlternativesByCriterias("E2","c1","A",1)
    opa.rankingAlternativesByCriterias("E2","c1","B",2)

    opa.rankingAlternativesByCriterias("E2","c2","A",2)
    opa.rankingAlternativesByCriterias("E2","c2","B",1)

    opa.rankingAlternativesByCriterias("E2","c3","A",2)
    opa.rankingAlternativesByCriterias("E2","c3","B",1)

    opa.rankingAlternativesByCriterias("E1","c1","A",1)
    opa.rankingAlternativesByCriterias("E1","c1","B",2)

    opa.rankingAlternativesByCriterias("E1","c2","A",1)
    opa.rankingAlternativesByCriterias("E1","c2","B",2)

    opa.rankingAlternativesByCriterias("E1","c3","A",1)
    opa.rankingAlternativesByCriterias("E1","c3","B",2)

    opa.rankingAlternativesByCriterias("E3","c1","A",2)
    opa.rankingAlternativesByCriterias("E3","c1","B",1)

    opa.rankingAlternativesByCriterias("E3","c2","A",1)
    opa.rankingAlternativesByCriterias("E3","c2","B",2)

    opa.rankingAlternativesByCriterias("E3","c3","A",1)
    opa.rankingAlternativesByCriterias("E3","c3","B",2)
    opa.solve()
    print(opa.expertsCriteriasAlternatives)
    opa.drawExpertWeights()
    opa.drawCriteriasWeights()
    opa.drawAlternativesWeights()
