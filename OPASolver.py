from matplotlib import pyplot
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable,GLPK

class OPASolver:
    experts=[]              # experts=[{"name"="Alami","rank"=1,weight=0.235},{"name":"Salami","rank":2,weight:0.134},...]
    criterias=[]            # criterias=[{"name"="price","rank"=1,weight=0.4},{"name":"power","rank":2,weight:0.121},...]
    alternatives=[]         # alternatives=[{"name"="Renault","rank"=1,weight=0.564},{"name":"Fiat","rank":2,weight:0.215},...]
    expertsCriterias=[]     # expertsCriterias=[{"expert":"Alami","criterias":[{"name":"power","rank":1},{"name":"price","rank":2}]},{"expert":"Salami","criterias":[{"name"="power","rank"=1},{"name"="price","rank"=2}]},...]
    preferenceDegreeExpert=1
    preferenceDegreeCriteria=1
    preferenceDegreeAlternative=1
    model=LpProblem(name="OPA", sense=LpMaximize)
    expertsCriteriasAlternatives=[]
    def __init__(self,e=[],c=[],a=[],ec=[],eca=[]):
        self.experts=e
        self.criterias=c
        self.alternatives=a
        self.expertsCriterias=ec
        self.expertsCriteriasAlternatives=eca
        self.model = LpProblem(name="OPA", sense=LpMaximize)
    #__________________________ Degree of preference __________________
    def setPreferenceDegreeExpert(self,d=1):
        self.preferenceDegreeExpert=d;
    def setPreferenceDegreeCriteria(self,d=1):
        self.preferenceDegreeCriteria=d;
    def setPreferenceDegreeAlternative(self,d=1):
        self.preferenceDegreeAlternative=d;
    
    def getPreferenceDegreeExpert(self,d=1):
        return self.preferenceDegreeExpert;
    def getPreferenceDegreeCriteria(self,d=1):
        return self.preferenceDegreeCriteria;
    def getPreferenceDegreeAlternative(self,d=1):
        return self.preferenceDegreeAlternative;
    #_______________________________Builders_____________________
    def addExpert(self,name,rank):
        for expert in self.experts:
            if(expert["name"]==name):
                print("This expert already exists !!")
                return 
        self.experts.append({"name":name,"rank":rank})
    def addCriteria(self,name,rank=0):
        for criteria in self.criterias:
            if(criteria["name"]==name):
                print("This criteria already exists !!")
                return 
        self.criterias.append({"name":name,"rank":rank})
    def addAlernative(self,name):
        for alternative in self.alternatives:
            if(alternative["name"]==name):
                print("This alternative already exists !!")
                return 
        self.alternatives.append({"name":name})
    #________________________________________________________________
    def setCriteriaRanks(self):
        for i in range (len(self.criterias)):
            rank=len(self.criterias)
            for j in range(len(self.criterias)):
                if(self.criterias[j]["weight"]<self.criterias[i]["weight"]):
                    rank -=1
            self.criterias[i]["rank"]=rank
    
    def setAlternativeRanks(self):
        for i in range (len(self.alternatives)):
            rank=len(self.alternatives)
            for j in range(len(self.alternatives)):
                if(self.alternatives[j]["weight"]<self.alternatives[i]["weight"]):
                    rank -=1
            self.alternatives[i]["rank"]=rank
    #______________________________________________________________
    def indiceExpert(self,nom):
        for i in range(len(self.experts)):
            if(self.experts[i]["name"]==nom):
                return i
        return -1
    
    def indiceCriteria(self,nom):
        for i in range(len(self.criterias)):
            if(self.criterias[i]["name"]==nom):
                return i
        return -1
    
    def indiceAlternative(self,nom):
        for i in range(len(self.alternatives)):
            if(self.alternatives[i]["name"]==nom):
                return i
        return -1
    #__________________________________________________________________
    def indexExpert(self,nom):
        for i in range(len(self.expertsCriterias)):
            if(self.expertsCriterias[i]["expert"]==nom):
                return i
        return -1
    def expertRank(self,name):
        for expert in self.experts:
            if(expert["name"]==name): return expert["rank"]
        return -1
    def rankingCriterias(self,expertName,criteria,rank):
        j=self.indexExpert(expertName)
        if(j > -1):
            lenght=len(self.expertsCriterias[j]["criterias"])
            if(lenght==0) : 
                self.expertsCriterias[j]["criterias"]=[{"criteria":criteria,"rank":rank}]
            else :                
                c=0
                while(c<lenght and self.expertsCriterias[j]["criterias"][c]["rank"]<rank): c+=1   
                self.expertsCriterias[j]["criterias"].insert(c,{"criteria":criteria,"rank":rank})
        else:
            lenghtexp=len(self.expertsCriterias)
            if(lenghtexp==0) : 
                self.expertsCriterias=[{"expert":expertName,"rank":self.expertRank(expertName),"criterias":[{"criteria":criteria,"rank":rank}]}]
            else :                
                e=0
                while(e<lenghtexp and self.expertRank(self.expertsCriterias[e]["expert"])<self.expertRank(expertName)): e+=1
                self.expertsCriterias.insert(e,{"expert":expertName,"rank":self.expertRank(expertName),"criterias":[{"criteria":criteria,"rank":rank}]})
    #__________________________________________________Alternatives / criterias / experts_______________________________________________________________
    def indexExpert1(self,nom):
        for i in range(len(self.expertsCriteriasAlternatives)):
            if(self.expertsCriteriasAlternatives[i]["expert"]==nom):
                return i
        return -1    
    def indexCriteria(self,j,nameC):
        for c in range(len(self.expertsCriteriasAlternatives[j]["criterias"])):
            if(self.expertsCriteriasAlternatives[j]["criterias"][c]["criteria"]==nameC):
                return c
        return -1
    def rankingAlternativesByCriterias(self,expertName,criteria,alternative,rankA):
        self.expertsCriteriasAlternatives=self.expertsCriterias.copy()
        j=self.indexExpert1(expertName)
        c=self.indexCriteria(j,criteria)
        if("alternatives" not in self.expertsCriteriasAlternatives[j]["criterias"][c]):
            self.expertsCriteriasAlternatives[j]["criterias"][c]["alternatives"]=[{"alternative":alternative,"rank":rankA}]
        else :
            if((j > -1 ) and (c>-1)):            
                lenght=len(self.expertsCriteriasAlternatives[j]["criterias"][c]["alternatives"])          
                a=0
                while(a<lenght and self.expertsCriteriasAlternatives[j]["criterias"][c]["alternatives"][a]["rank"]<rankA): a+=1   
                self.expertsCriteriasAlternatives[j]["criterias"][c]["alternatives"].insert(a,{"alternative":alternative,"rank":rankA})
            else:
                print(" erreur de saisie des critères par experts ", expertName, criteria,alternative)

    def createCoefficients(self):
        coefs=[]
        for expert in self.expertsCriteriasAlternatives:
            i=expert["rank"]
            for criteria in expert["criterias"]:
                j=criteria['rank']
                for alternative in criteria["alternatives"]:
                    k=alternative['rank']
                    coefs.append((i**self.preferenceDegreeExpert)*(j**self.preferenceDegreeCriteria)*(k**self.preferenceDegreeAlternative))
        return coefs
#---------------------------------------------------------------------------------------
    def solve(self):
        nbExperts=len(self.experts)
        nbCriterias=len(self.criterias)
        nbAlternatives=len(self.alternatives)
        coefficients=self.createCoefficients();
        dim=len(coefficients)
        weights=[]
        for i in range(dim):
                e= i // (nbAlternatives*nbCriterias) +1
                c= (i // nbAlternatives)%nbCriterias +1
                a= i % nbAlternatives +1
                weights.append(LpVariable(name="W"+str(e)+str(c)+str(a), lowBound=0))
        z=LpVariable(name="z", lowBound=0)
        # Add the constraints to the model
       
        for i in range(dim):
            if( (i+1) % nbAlternatives == 0):
                self.model +=  coefficients[i]*weights[i] >=z
            else:  
                self.model  += coefficients[i]*(weights[i]-weights[i+1])>=z
        self.model += sum([weights[i] for i in range(dim)])==1
      
        
        # Add the objective function to the model
        self.model  += lpSum([z, z])
        status = self.model.solve()
        liste= self.model.variables()
        w=0;
        for i in range(len(self.experts)):
            self.experts[i]["weight"]=0
        for i in range(len(self.criterias)):
            self.criterias[i]["weight"]=0
        for i in range(len(self.alternatives)):
            self.alternatives[i]["weight"]=0

        for i in range(len(self.expertsCriteriasAlternatives)):
            c=len(self.expertsCriteriasAlternatives[i]["criterias"])
            self.expertsCriteriasAlternatives[i]["weight"]=0
            expertName=self.expertsCriteriasAlternatives[i]["expert"]
            index=self.indiceExpert(expertName)
            self.experts[index]["weight"]=0
            for j in range(c):
                a=len(self.expertsCriteriasAlternatives[i]["criterias"][j]["alternatives"]);
                criteriaIndex=self.indiceCriteria(self.expertsCriteriasAlternatives[i]["criterias"][j]["criteria"])
                for k in range(a):
                    self.expertsCriteriasAlternatives[i]["criterias"][j]["alternatives"][k]["weight"]=liste[w].value()
                    print(liste[w].name," = ",liste[w].value())
                    alternativeIndex=self.indiceAlternative(self.expertsCriteriasAlternatives[i]["criterias"][j]["alternatives"][k]["alternative"])
                    self.expertsCriteriasAlternatives[i]["weight"]+=liste[w].value()
                    self.experts[index]["weight"]+=liste[w].value()
                    self.criterias[criteriaIndex]["weight"]+=liste[w].value()
                    self.alternatives[alternativeIndex]["weight"]+=liste[w].value()
                    w=w+1;
        self.setCriteriaRanks()
        self.setAlternativeRanks()
        return liste                
#---------------------------------------------------------------------------------------
   #______________________ getters and setters ______________________    
    def getExperts(self):
        return self.experts
    def getCriterias(self):
        return self.criterias
    def getAlternatives(self):
        return self.alternatives
    #________________________ OPA output weights  _____________________
    def getExpertsWeights(self):
        dics={}
        for expert in self.experts:
            if ("weight" not in expert):
                print("the experts weights are not yet calculated !!")
                return {}
            else : dics[expert["name"]]=expert["weight"]
        return dics
    def getCriteriasWeights(self):
        dics={}
        for criteria in self.criterias:
            if (criteria['weight']==0):
                print("the criterias weights are not yet calculated !!")
                return {}
            else : dics[criteria["name"]]=criteria["weight"]
        return dics
    def getAlternativesWeights(self):
        dics={}
        for alternative in self.alternatives:
            if (alternative['weight']==0):
                print("the alternatives weights are not yet calculated !!")
                return {}
            else : dics[alternative["name"]]=alternative["weight"]
        return dics
    #_________________ graphic drawing _________
    def drawExpertWeights(self):
        dics=self.getExpertsWeights()
        self.drawWeights(dics,"#5C9AD6","Experts")
    def drawCriteriasWeights(self):
        dics=self.getCriteriasWeights()
        pyplot.bar(list(dics.keys()),dics.values())
        self.drawWeights(dics,"#FCC000","Criterias")
    def drawAlternativesWeights(self):
        dics=self.getAlternativesWeights()
        self.drawWeights(dics,"#ED7D31","Alternatives")
        
    def drawWeights(self,dics,color,param=""):
        pyplot.bar(list(dics.keys()),dics.values(),color =color,
        width = 0.8)
        pyplot.grid(color='#95a5a6', linestyle=':', linewidth=0.5, axis='y')
        pyplot.xlabel(param)
        pyplot.ylabel('Weights')
        pyplot.title('weights of '+param)





