import matplotlib.pyplot as plt
import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import tkinter
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo


#setting the window
root = Tk()
root.title("ANALYSIS OF VARIANCE")
root.configure(width=1000, height=900)
fontStyle = tkFont.Font(family="Lucida Grande", size=13)


#list o send the excel file for pd to read
excelfile = list()

#first window            
class mainwindow:
    def __init__(self, master):
        self.master = master
        fontStyle = tkFont.Font(family="Lucida Grande", size=25)

        self.btn1 = tk.Button(self.master, text ="ONE-WAY ANOVA", font = fontStyle, command = self.clearpage1)
        self.btn1.place(relx = 0.5, rely = 0.40, anchor = CENTER)

        self.btn2 = tk.Button(self.master, text ="TWO-WAY ANOVA", font = fontStyle, command = self.clearpage2)
        self.btn2.place(relx = 0.5, rely = 0.60, anchor = CENTER)


    #functionro clear the page to view the next page elements
    def clearpage1(self):
        self.btn1.destroy()
        self.btn2.destroy()
        
        self.another = Oneway(self.master)
    def clearpage2(self):
        self.btn1.destroy()
        self.btn2.destroy()
        
        self.another = Twoway(self.master)

#One way anova component
class Oneway:
    def __init__(self, master):
           

        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)

        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        
        
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        
        
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        
        self.label3= Label(self.master, text="Independent Variable: ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)


        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)


        #function for all the one way anova analysis   
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var = (self.entry_2.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    model = ols('%s ~ %s ' %(dependent_var, independent_var), data = data).fit()
                    aov = sm.stats.anova_lm(model, type=2)
                    
                    
                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - ONE WAY ANOVA")
                    newwindow.geometry("700x500")

                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace.set(aov)
                    self.label4= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label4.place(relx = 0.5, rely = 0.10, anchor = CENTER)

                    #Run new window
                    newwindow.mainloop()
        def boxplot():
            dependent_var = (self.entry_1.get())
            independent_var = (self.entry_2.get())
            for file in excelfile:
                data = pd.read_excel(file)
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var) )
                plt.show()
                
        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail

            selectedfilespace.set(mainfilename)


        #Buttons
        self.label5= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label5.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        self.btn5.place(relx = 0.5, rely = 0.33  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.40, anchor = CENTER)
            
        
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label5.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()
                
        self.another = mainwindow(self.master)


#Two way anova component
class Twoway:
    def __init__(self, master):
           

        # keep `root` in `self.master`
        self.master = master
        fontStyle1 = tkFont.Font(family="Lucida Grande", size=13)


        #back button to view previous page, that is the main page
        self.btn4 = tk.Button(self.master, text ="BACK", font = fontStyle1, command = self.load_back)
        self.btn4.place(relx = 0.90, rely = 0.84, anchor = CENTER)
        
        
        self.label1 = Label(self.master, text="File Selected:", font = fontStyle)
        self.label1.place(relx = 0.3, rely = 0.15, anchor = CENTER)
        
        
        self.label2 = Label(self.master, text="Dependent Variable: ", font = fontStyle)
        self.label2.place(relx = 0.3, rely = 0.20, anchor = CENTER)
        self.label3= Label(self.master, text="Independent Variable one : ", font = fontStyle)
        self.label3.place(relx = 0.3, rely = 0.25, anchor = CENTER)
        self.label4= Label(self.master, text="Independent Variable two : ", font = fontStyle)
        self.label4.place(relx = 0.3, rely = 0.30, anchor = CENTER)

        #entry box for dependent and independent variavles
        self.entry_1 = Entry(self.master)
        self.entry_2 = Entry(self.master)
        self.entry_3 = Entry(self.master)
        self.entry_1.place(relx = 0.5, rely = 0.20, anchor = CENTER)
        self.entry_2.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.entry_3.place(relx = 0.5, rely = 0.30, anchor = CENTER)

        

        #function for all the two way anova analysis
        def analyse():
            #Check if a file selected whenever the user clicks "Analyse" button and showinformation if there is no file selected
            if len(excelfile) == 0:
                messagebox.showinfo("showinfo", "Please, select a file")
            #Continue with the analysis if a file is selected
            else:
                dependent_var = (self.entry_1.get())
                independent_var1 = (self.entry_2.get())
                independent_var2 = (self.entry_3.get())
                for file in excelfile:
                    data = pd.read_excel(file)
                    model = ols('%s ~ %s+%s ' %(dependent_var, independent_var1, independent_var2), data = data).fit()
                    aov = sm.stats.anova_lm(model, type=2)

                    
                        
                    #setting up newwindow to embed the result on
                    newwindow = Toplevel()      #TOPLEVEL() USED
                    newwindow.title("RESULT WINDOW - ONE WAY ANOVA")
                    newwindow.geometry("700x500")

                    
                    #setting space to view result on inside of the new window
                    aovspace = tk.StringVar()
                    aovspace.set(aov)
                    self.label5= Label(newwindow, text="", textvariable=aovspace, font = fontStyle)
                    self.label5.place(relx = 0.5, rely = 0.10, anchor = CENTER)
                    #Run new window
                    newwindow.mainloop()

        def boxplot():
            dependent_var = (self.entry_1.get())
            independent_var1 = (self.entry_2.get())
            independent_var2 = (self.entry_3.get())
            for file in excelfile:
                data = pd.read_excel(file)
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var1) )
                data.boxplot('%s' %(dependent_var), by='%s' %(independent_var2) )
                plt.show()

        #settinf up space to view the name of selected file
        selectedfilespace = tk.StringVar()
        
        #function for selecting excel file to be used in the analysis
        def select_file():
            filetypes = (('text files', '*.xlsx'),('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
            
            #send the selected excel file to the excelfile list
            excelfile.append(filename)

            #split and remove the path of the selected file and be left with that main filename
            head, tail = os.path.split(filename)
            mainfilename = tail
            
            selectedfilespace.set(mainfilename)

        #Buttons
        self.label6= Label(self.master, text="File Selected: ", textvariable=selectedfilespace, font = fontStyle)
        self.label6.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #creating a checkbox to allow view boxplot
        self.btn5 = tk.Checkbutton(self.master, text="show boxplot", command=boxplot, font=fontStyle)
        self.btn5.place(relx = 0.5, rely = 0.36  , anchor = CENTER)
        self.btn6 = tk.Button(self.master,text='Open a File',font= fontStyle1, command=select_file)
        self.btn6.place(relx = 0.5, rely = 0.07, anchor = CENTER)
        self.btn7 = tk.Button(self.master,text='Analyse',font= fontStyle1, command=analyse)
        self.btn7.place(relx = 0.5, rely = 0.43, anchor = CENTER)
            
        
                        
    #function to clear the current page to view the previous page elements
    def load_back(self):
        self.entry_1.destroy()
        self.entry_2.destroy()
        self.entry_3.destroy()
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.btn4.destroy()
        self.btn5.destroy()
        self.btn6.destroy()
        self.btn7.destroy()
        excelfile.clear()
   
        self.another = mainwindow(self.master)

   


#set default window as mainwindow and run
mainwindow(root)
root.mainloop()
