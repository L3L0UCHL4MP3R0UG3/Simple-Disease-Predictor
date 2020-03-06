# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:54:43 2019

@author: liudmila
"""
import tkinter as T
import MySQLdb as m
text="YOU HAVE:\n"
dis=[]
db=m.connect("localhost","root","ye*********","med")
disease=[]
xo=[]

class App(T.Tk):
    def __init__(self,*args,**kwargs):
        T.Tk.__init__(self,*args,**kwargs)
        self.geometry('1017x700')
        container=T.Frame(self)
        container.place(x=0,y=0,width=1017,height=700)
       
        canvas = T.Canvas(container)
        canvas.pack()
        global disease
        global q
        global dis
        
        
        self.frames={}
        for f in(Welcome,Sorting):
            frame=f(container,self)
            self.frames[f]=frame
            frame.place(x=0,y=0,width=1017,height=700)
        self.show_frame(Welcome)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

class Welcome(T.Frame):
    def __init__(self,parent,controller):
        T.Frame.__init__(self,parent)
        canvas = T.Canvas(self, width = 1017, height = 700)
        canvas.pack()
        label=T.Label(self,text="WELCOME!!!",bg='MediumAquamarine',font=26,fg='white')
        label.place(x=0,y=0,width=1017,height=50)
        
        button=T.Button(self,text="Continue",command=lambda: controller.show_frame(Sorting),activebackground='Seagreen',fg='white',bg='MediumAquamarine')
        button.place(x=250,y=500,width=500, height=50)
        
        
        
class Sorting(T.Frame):
    def __init__(self,parent,controller):
        T.Frame.__init__(self,parent)
        canvas = T.Canvas(self, width = 1017, height = 700)
        canvas.pack()
        global db
        global selection
        global disease
        global q
        global v
        global lst
        global lst2
        global dis
        global t
        cursor=db.cursor()
        dis=[]
        q=[]
        def Nxt():   
            global db
            global disease
            global dis
            global q
            global text
            global xo
            global t
            global cnt
            for b in selection:
                if b not in(-1,0):
                        q.append(lst[b-1])
            '''DISEASES HAVING Q SYMPTOM '''
            for i in q:
                cursor1=db.cursor()
                cursor1.callproc('chck_dis',[i,])
                result1=cursor1.fetchall()
                dis.extend([x[0] for x in result1])
                cursor1.close()
            disease=list(set(dis))
            for i in disease:
                cursor2=db.cursor()
                cursor2.callproc('probchck',[i,])
                result2=cursor2.fetchall()
                xo.extend([x[0] for x in result2])
                cursor2.close()
            cnt=[dis.count(i) for i in disease]
            t=dict(zip(disease,cnt))
            a=0
            per=[]
            for i in t:
                per.append(float((t[i]/len(dis))*(t[i]/xo[a])*100))
                a=a+1
            a=0
            trying=max(per)
            trying2=per.index(trying)
            for i in disease:
                text=text+str(per[a])+" % chance of having "+i+"\n"
                a=a+1
            text=text+"\n\n====> "+disease[trying2]
            label=T.Label(self,text=text,fg='Green',justify='left')
            label.place(x=581,y=51,width=400,height=600)
            
            
        def sel():
            global selection
            global b
            global q
            selection=[]
            for i in v:
                selection.append(int(i.get()))
            
            
        '''ASK FOR SYMPTOM'''
        sql="select S.S_name from symptoms S"
        cursor.execute(sql)
        a=cursor.rowcount
        
        lst2=[i for i in range(1,a+1)]
        
        result=cursor.fetchall()
        lst=[str(j[0]) for j in result]
        
        LOL=dict(zip(lst,lst2))
        v=[T.IntVar() for i in range(len(LOL))]
        counter=0
        y=101
        for (text, value) in LOL.items(): 
            T.Checkbutton(self, text = text, variable = v[counter],  
                            onvalue = value, offvalue=-1,indicator=0,
                            background = "light blue", command=sel).place(x=41,y=y,width=450,height=27)
            y=y+30
            counter=counter+1
        label=T.Label(self,text="SELECT THE VISIBLE SYMPTOMS",bg='MediumAquamarine',font=26,fg='white')
        label.place(x=170,y=0,width=677,height=39)
        back=T.Button(self,text="<< Go back", command=lambda: controller.show_frame(Welcome),fg='white',bg='MediumAquamarine')
        back.place(x=0,y=0,width=170,height=39)
        nxt=T.Button(self,text="Next >>", command=Nxt,fg='white',bg='MediumAquamarine')
        nxt.place(x=847,y=0,width=170,height=39)


main=App()
main.mainloop()



 















        
    
