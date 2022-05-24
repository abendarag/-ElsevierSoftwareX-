from ctypes import alignment
from random import randint
from tkinter import *
from tkinter import ttk
from turtle import color, width
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib import pyplot
from OPASolver import OPASolver
class VerticalScrolledFrame(Frame):
    def __init__(self, parent, bgcolor, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            
        vscrollbar = Scrollbar(self, orient=VERTICAL)     
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set,bg=bgcolor,width=800)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, bg=bgcolor)
        interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)

        # track changes to the canvas and frame width and sync them, # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
                # update the canvas's width to fit the inner frame
            canvas.config(width=800, height=180)
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=interior.winfo_reqwidth() )
        canvas.bind('<Configure>', _configure_canvas)




class OPAWindow:
    opa=OPASolver()
    experts=[]             
    criterias=[]           
    alternatives=[]         
    expertsCriterias=[]     
    expertsCriteriasAlternatives=[]
    preferenceDegreeExpert=1
    preferenceDegreeCriteria=1
    preferenceDegreeAlternative=1
    ec=[]
    eca=[]
    colors=["darkgray","gainsboro","darkgray","#D3D3D3"]
    def __init__(self):
        self.fenetre = Tk()
        self.opa=OPASolver()
        self.fenetre.title("PyOPASolver")
        self.fenetre.geometry("1024x960")
        self.fenetre.grid_columnconfigure((0,10), weight=1)
        
        titre = Label(self.fenetre, text="PyOPASolver", font=('sans serif', 20, 'bold'), fg='#900')
        titre.grid(row=0, column=0)

        self.F1 = Frame(self.fenetre, bg=self.colors[0],width=600, borderwidth=2, relief=RIDGE)
        self.F1.grid(row=1, column=0)


        Button1 = Button(self.fenetre,command=self.enterExpertsAndRank)
        Button1.configure(pady="3",padx="5")
        Button1.configure(text="Save expert inputs",bg=self.colors[0])
        Button1.grid(row=1, column=1)


        self.F2 = VerticalScrolledFrame(self.fenetre,self.colors[1])
        self.F2.grid(row=2, column=0)


        Button2 = Button(self.fenetre,command=self.getExperts,bg=self.colors[1])
        Button2.configure(pady="3",padx="5")
        Button2.configure(text="Save inputs")
        Button2.grid(row=2, column=1)
        

        self.F3 = VerticalScrolledFrame(self.fenetre,self.colors[2])
        self.F3.grid(row=3, column=0)


        Button3 = Button(self.fenetre,command=self.getExpertCriterias,bg=self.colors[2])
        Button3.configure(pady="3",padx="5")
        Button3.configure(text="solve problem")
        Button3.grid(row=3, column=1)
   


        self.Fw = VerticalScrolledFrame(self.fenetre,self.colors[3])
        self.Fw.grid(row=4, column=0)

      
        self.globalInformations()

    def enterExpertCriterias(self):
        maxnb=max(self.NumberofExpert,self.NumberofCreteria,self.NumberofAlternative)
        for i in range(self.NumberofExpert):
            for j in range(self.NumberofCreteria):
                label = Label(self.F3.interior, text="rank of "+self.criterias[j]["name"]+" for "+ self.experts[i]["name"] +":",bg=self.colors[2])
                entrer = Entry(self.F3.interior,width=15) 
                entrer.insert(0,randint(1,self.NumberofCreteria)) 
                label.grid(row=(i*self.NumberofCreteria)+j+maxnb+9, column=0)
                entrer.grid(row=(i*self.NumberofCreteria)+j+maxnb+9, column=1)
                self.ec.append(entrer)
        self.enterExpertCriteriaAlternatives()

        #Button3 = Button(self.F3.interior,command=self.getExpertCriterias,bg=self.colors[2])
       # Button3.configure(pady="3",padx="5")
       # Button3.configure(text="solve")
       # Button3.grid(row=(self.NumberofExpert*self.NumberofCreteria)+j+maxnb+10, column=8)
        #ttk.Separator(self.F3.interior, orient=HORIZONTAL).grid(row=4,columnspan=300, padx=10, pady=10, sticky=EW)
   
    def enterExpertCriteriaAlternatives(self):
        maxnb=max(self.NumberofExpert,self.NumberofCreteria,self.NumberofAlternative)
        decalage=0
        for i in range(self.NumberofExpert):
            for j in range(self.NumberofCreteria):
                for k in range(self.NumberofAlternative):
                    label = Label(self.F3.interior, text="("+self.experts[i]["name"]+" , "+self.criterias[j]["name"]+" ) : rank ( "+ self.alternatives[k]["name"]+" ) :",bg=self.colors[2])
                    entrer = Entry(self.F3.interior,width=15) 
                    entrer.insert(0,randint(1,self.NumberofAlternative)) 
                    label.grid(row=(j*self.NumberofAlternative)+k+maxnb+9, column=2+decalage)
                    entrer.grid(row=(j*self.NumberofAlternative)+k+maxnb+9, column=3+decalage)
                    self.eca.append(entrer)
            decalage+=2

    def enterCriterias(self):
        self.NumberofCreteria= int(self.txtcnbCriterias.get())
        for i in range(self.NumberofCreteria):
            label = Label(self.F2.interior, text="Name of creterion "+str(i)+" :",bg=self.colors[1])
            entrer = Entry(self.F2.interior,width=15)
            entrer.insert(0,"C"+str(i+1)) 
            label.grid(row=i+7, column=4)
            entrer.grid(row=i+7, column=5)
            self.criterias.append({"name":entrer})
        self.enterAlternatives()
    def enterAlternatives(self):
        self.NumberofAlternative=int(self.txtnbAlternatives.get())
        for i in range(self.NumberofAlternative):                    
            label = Label(self.F2.interior, text="Name of alternative  "+str(i)+" :",bg=self.colors[1])
            entrer = Entry(self.F2.interior,width=15) 
            entrer.insert(0,"A"+str(i+1))
            label.grid(row=i+7, column=6)
            entrer.grid(row=i+7, column=7)        
            self.alternatives.append({"name":entrer})
    def getDegreePreferences(self):
        self.preferenceDegreeExpert=int(self.txtdegreeExperts.get())  
        self.preferenceDegreeCriteria=int(self.txtdegreeCriterias.get())  
        self.preferenceDegreeAlternative=int(self.txtdegreeAlternatives.get())  
    
    def getExperts(self):
        for i in range(len(self.experts)):
            self.experts[i]["name"]=self.experts[i]["name"].get()
            self.experts[i]["rank"]=int(self.experts[i]["rank"].get())
        self.getCriterias()
    def enterExpertsAndRank(self):
        self.getDegreePreferences()
        self.NumberofExpert=int(self.txtnbExperts.get())
        for i in range(self.NumberofExpert):
            label = Label(self.F2.interior, text="Name of expert "+str(i)+" :",bg=self.colors[1])
            entrerE= Entry(self.F2.interior,width=15) 
            entrerE.insert(0,"E"+str(i+1))
            label.grid(row=i+7, column=0)
            entrerE.grid(row=i+7, column=1)
            label = Label(self.F2.interior, text="Rank of expert "+str(i)+" :",bg=self.colors[1])
            entrerR= Entry(self.F2.interior,width=15) 
            entrerR.insert(0,str(i+1))
            self.experts.append({"name":entrerE,"rank":entrerR})
            label.grid(row=i+7, column=2)
            entrerR.grid(row=i+7, column=3) 
        self.enterCriterias()
       # Button2 = Button(self.F2.interior,command=self.getExperts,bg=self.colors[1])
        #Button2.configure(pady="3",padx="5")
        #Button2.configure(text="Save")
       # Button2.grid(row=self.NumberofExpert+5, column=8)
        #ttk.Separator(self.F3.interior, orient=HORIZONTAL).grid(row=4,columnspan=300, padx=10, pady=10, sticky=EW)
        
    def getCriterias(self):
        for i in range(len(self.criterias)):
            self.criterias[i]["name"]=self.criterias[i]["name"].get()
        self.getAlternatives()
    def getAlternatives(self):
        for i in range(len(self.alternatives)):
            self.alternatives[i]["name"]=self.alternatives[i]["name"].get()
        self.enterExpertCriterias()

    def getExpertCriterias(self):
        ij=0
        for i in range(self.NumberofExpert):
            self.expertsCriterias.append({"expert":self.experts[i]["name"],"criterias":[]})
            for j in range(self.NumberofCreteria):
                self.expertsCriterias[i]["criterias"].append({"name":self.criterias[j]["name"],"rank":int(self.ec[ij].get())})
                ij+=1
        self.getExpertCriteriaAlternatives()

    def getExpertCriteriaAlternatives(self):
        self.expertsCriteriasAlternatives=self.expertsCriterias.copy() 
        ijk=0
        for i in range(self.NumberofExpert):
            for j in range(self.NumberofCreteria):   
                self.expertsCriteriasAlternatives[i]["criterias"][j]["alternatives"]=[]          
                for k in range(self.NumberofAlternative):
                    self.expertsCriteriasAlternatives[i]["criterias"][j]["alternatives"].append({"name":self.alternatives[k]["name"],"rank":int(self.eca[ijk].get())})
                    ijk+=1
        self.displayWeights()
    def globalInformations(self):
        nbExperts = Label(self.F1, text="Number of experts : ", bg=self.colors[0])
        nbCriterias = Label(self.F1, text="Number of criterias : ", bg=self.colors[0])
        nbAlternatives = Label(self.F1, text="Number of alternatives : ", bg=self.colors[0])

        self.txtnbExperts = Entry(self.F1,width=10) 
        self.txtnbExperts.insert(0,"3")
        self.txtcnbCriterias = Entry(self.F1,width=10)
        self.txtcnbCriterias.insert(0,"2")
        self.txtnbAlternatives = Entry(self.F1,width=10)
        self.txtnbAlternatives.insert(0,"4")

        nbExperts.grid(row=2, column=1)
        self.txtnbExperts.grid(row=2, column=2)
        nbCriterias.grid(row=2, column=3)
        self.txtcnbCriterias.grid(row=2, column=4)
        nbAlternatives.grid(row=2, column=5)
        self.txtnbAlternatives.grid(row=2, column=6)

        degreeExperts = Label(self.F1, text="Degree of preference for experts : ", bg=self.colors[0])
        degreeCriterias = Label(self.F1, text="Degree of preference for  criteria : ", bg=self.colors[0])
        degreeAlternatives = Label(self.F1, text="Degree of preference for alternatives : ", bg=self.colors[0])

        self.txtdegreeExperts = Entry(self.F1,width=10) 
        self.txtdegreeExperts.insert(0,"1")
        self.txtdegreeCriterias = Entry(self.F1,width=10)
        self.txtdegreeCriterias.insert(0,"1")
        self.txtdegreeAlternatives = Entry(self.F1,width=10)
        self.txtdegreeAlternatives.insert(0,"1")

        degreeExperts.grid(row=3, column=1)
        self.txtdegreeExperts.grid(row=3, column=2)
        degreeCriterias.grid(row=3, column=3)
        self.txtdegreeCriterias.grid(row=3, column=4)
        degreeAlternatives.grid(row=3, column=5)
        self.txtdegreeAlternatives.grid(row=3, column=6)

        #Button1 = Button(self.F1,command=self.enterExpertsAndRank)
        #Button1.configure(pady="3",padx="5")
        #Button1.configure(text="Save expert inputs",bg="saddlebrown")
        #Button1.grid(row=4, column=4)
        #ttk.Separator(self.F1, orient=HORIZONTAL).grid(row=11,columnspan=300, padx=10, pady=10, sticky=EW)
    def callSolver(self):
        self.opa.experts=self.experts.copy()
        self.opa.criterias=self.criterias.copy()
        self.opa.alternatives=self.alternatives.copy()
        for e in self.expertsCriterias:
            for c in e["criterias"] :
                self.opa.rankingCriterias(e["expert"],c["name"],c["rank"])
        for e in self.expertsCriteriasAlternatives:
            for c in e["criterias"] :

                for a in c["alternatives"]:
                    self.opa.rankingAlternativesByCriterias(e["expert"],c["name"],a["name"],a["rank"])
    def displayWeights(self):
        self.callSolver()
        maListe=self.opa.solve()
        self.txtnbExperts
        i=1
        #-------------- detailled Weights --------------------------
        texte=""
        for var in maListe:
            texte+=f"{var.name}: {round(var.value(),6)}\n" 
            if i%self.NumberofExpert ==0 :               
                reslabel = Label(self.Fw.interior, text=texte,bg=self.colors[3])
                reslabel.grid(row=1, column=i//self.NumberofExpert -1)
                texte=""
            i+=1
        reslabel = Label(self.Fw.interior, font=('sans serif', 16, 'bold'), text=f"{var.name}: {round(var.value(),6)}\n",bg=self.colors[3],fg="#900" )        
        reslabel.grid(row=2, column=4)
        maxnb=max(self.NumberofExpert,self.NumberofCreteria,self.NumberofAlternative)
        #-------------- Experts  Weights --------------------------
        wEperts=self.opa.getExpertsWeights()
        label = Label(self.Fw.interior, font=15, text="Expert Weights : ",bg=self.colors[3])
        label.grid(row=3, column=0)
        ie=1
        for e in wEperts:   
            reslabel = Label(self.Fw.interior, font=14, text=e+" : "+str(round(wEperts[e],6)) ,bg=self.colors[3])
            reslabel.grid(row=3, column=ie)
            ie+=1
        ButtonGE = Button(self.Fw.interior,command=self.plotWeightExpertsGraphs,bg=self.colors[3])
        ButtonGE.configure(pady="3",padx="5")
        ButtonGE.configure(text="Plot expert weights graphs")
        ButtonGE.grid(row=3, column=maxnb+1)
        #-------------- Criterias  Weights --------------------------
        wCriterias=self.opa.getCriteriasWeights()
        label = Label(self.Fw.interior, font=15, text="Criteria Weights : ",bg=self.colors[3]) 
        label.grid(row=4, column=0)
        ic=1
        for c in wCriterias:   
            reslabel = Label(self.Fw.interior, font=14, text=c+" : "+str(round(wCriterias[c],6)) ,bg=self.colors[3])
            reslabel.grid(row=4, column=ic)
            ic+=1
        ButtonGC = Button(self.Fw.interior,command=self.plotWeightCriteriaGraphs,bg=self.colors[3])
        ButtonGC.configure(pady="3",padx="5")
        ButtonGC.configure(text="Plot criteria weights graphs")
        ButtonGC.grid(row=4, column=maxnb+1)
        #-------------- Alternatives  Weights --------------------------
        wAlternatives=self.opa.getAlternativesWeights()
        label = Label(self.Fw.interior, font=15, text="Alternative Weights : ",bg=self.colors[3]) 
        label.grid(row=5, column=0)
        ia=1
        for a in wAlternatives:   
            reslabel = Label(self.Fw.interior, font=14, text=a+" : "+str(round(wAlternatives[a],6)),bg=self.colors[3] )
            reslabel.grid(row=5, column=ia)
            ia+=1
        ButtonGA = Button(self.Fw.interior,command=self.plotWeightAlternativesGraphs,bg=self.colors[3])
        ButtonGA.configure(pady="3",padx="5")
        ButtonGA.configure(text="Plot alternative weights graphs")
        ButtonGA.grid(row=5, column=maxnb+1)
    def plotWeightExpertsGraphs(self):  
        newWindow = Tk() 
        newWindow.title("Expert weights") 
        newWindow.geometry("400x400")  
        data = self.opa.getExpertsWeights()
        expertsNames = list(data.keys())
        expertsWheights = list(data.values())
        fig1 = plt.figure(figsize = (5, 5)) 
        # creating the bar plot
        plt.bar(expertsNames, expertsWheights, color ='maroon',width = 0.4)
        plt.xlabel("Experts names")
        plt.ylabel("Wheights")
        plt.title("Experts Wheights")
        canvas = FigureCanvasTkAgg(fig1,master = newWindow)  
        canvas.draw() 
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,newWindow)
        toolbar.update()
        canvas.get_tk_widget().pack()
    def plotWeightCriteriaGraphs(self):  
        newWindow = Tk() 
        newWindow.title("Criteria weights") 
        newWindow.geometry("400x400")  
        data = self.opa.getCriteriasWeights()
        criteriaNames = list(data.keys())
        criteriaWheights = list(data.values())
        fig1 = plt.figure(figsize = (5, 5)) 
        # creating the bar plot
        plt.bar(criteriaNames, criteriaWheights, color ='orange',width = 0.4)
        plt.xlabel("Criteria names")
        plt.ylabel("Wheights")
        plt.title("Criteria Wheights")
        canvas = FigureCanvasTkAgg(fig1,master = newWindow)  
        canvas.draw() 
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,newWindow)
        toolbar.update()
    def plotWeightAlternativesGraphs(self):  
        newWindow = Tk() 
        newWindow.title("Alternatives weights") 
        newWindow.geometry("400x400")  
        data = self.opa.getAlternativesWeights()
        alternativeNames = list(data.keys())
        alternativeWheights = list(data.values())
        fig1 = plt.figure(figsize = (5, 5)) 
        # creating the bar plot
        plt.bar(alternativeNames, alternativeWheights, color ='yellow',width = 0.4)
        plt.xlabel("Alternatives names")
        plt.ylabel("Wheights")
        plt.title("Alternatives Wheights")
        canvas = FigureCanvasTkAgg(fig1,master = newWindow)  
        canvas.draw() 
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,newWindow)
        toolbar.update()
app=OPAWindow()
app.fenetre.mainloop()
