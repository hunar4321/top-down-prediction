# -*- coding: utf-8 -*-
"""
Predict Hidden Patterns - Exploring Algorthims
@author: Hunar @ brainxyz.com

For more info please check out the associated video: https://youtube.com/@brainxyz/   ?comming soon
Also, there is a blog post: https://www.brainxyz.com/blog/predict/
        
"""

## To run the code, numpy and scipy need to be installed
import numpy as np
from scipy.optimize import lsq_linear
from tkinter import *


## For a more commented version of this algorithm please look at predict_pattern_algorithms.py
class PredictPattern():
    """
    Gui interface with predictions for each guess & trial
    """
    def __init__(self):    
        self.root = Tk()
        self.root.title("Brainxyz - Predict Pattern")         
        self.btnWdith = 10
        self.btnHeight = 5
        self.fontSize = 13
        self.Nrows = 4
        self.Ncols = 4
        self.N = self.Nrows * self.Ncols
        self.trials = 0
        self.pat = np.ones(self.N)
        self.guess = np.zeros(self.N)
        self.score = 0
        self.total_ones = 0
        self.total_zeros = self.N
        self.xs = []
        self.ys = []
        self.wT = np.ones(self.N)*0.5
        self.wF = np.ones(self.N)*0.5          
        self.text = [None]*self.N 
        self.buttons = [None for x in range(self.N)] 
        self.labelText = StringVar()
        self.labelText.set("Score: ?")
        self.label1 = Label(self.root, font=('Arial', 15), textvariable=self.labelText, height=5)
        self.label1.grid(row = 0, column = 1)
        self.labelTrials = StringVar()
        self.labelTrials.set("Trials: 0")
        self.label2 = Label(self.root, font=('Arial', 15), textvariable=self.labelTrials, height=5)
        self.label2.grid(row = 0, column = 2)
        self.button1 = Button(self.root, bg="coral", font=('Arial', self.fontSize), height=3, text=" Restart ", command=lambda: self.restart())
        self.button1.grid(row=0, column = 3)
        self.button2 = Button(self.root, bg="light blue", font=('Arial', self.fontSize), height=3, text=" Rescore ", command=lambda: self.rescore())
        self.button2.grid(row=0, column = 0)
    
    def restart(self):        
        self.trials = 0
        self.pat = np.random.choice([1.0,0.0], self.N)
        self.guess = np.zeros(self.N)
        self.score = self.check_score(self.pat, self.guess)
        self.trials += 1
        self.total_zeros = self.score   
        self.total_ones = self.N-self.total_zeros     
        self.xs = []
        self.ys = []
        self.xs.append(1-self.guess.copy())    
        self.ys.append(self.total_ones)    
        self.wT = np.ones(self.N) * (self.total_ones/self.N)
        self.wF = np.ones(self.N) * (self.total_zeros/self.N)
        self.labelTrials.set("Trials: "+ str(self.trials))
        self.labelText.set("Score: "+ str(self.score))
        j=-1
        k=0         
        for i in range(self.N):
            self.text[i] = StringVar()
            self.text[i].set('T .%d' % (self.wT[i]*100))        
            self.buttons[i] = Button(self.root, command = lambda i=i, : self.toggle_guess(i))
            self.buttons[i].config(bg="light pink", textvariable = self.text[i], font=('Arial', self.fontSize), width = self.btnWdith, height = self.btnHeight)
            if(i%self.Nrows == 0):
                j += 1
                k = 0
            self.buttons[i].grid(row = j+2, column = k)
            k += 1   
        self.log()
            
    def log(self):
        print("----------------")
        print('trials:', self.trials, 'score:', self.score)          
        print('truth:', self.pat)
        print('guess:', self.guess)
        print("T:", np.round(self.wT, 2))
        print("F:", np.round(self.wF, 2))
        print("True grid:") 
        print(np.reshape(self.pat, (self.Nrows,self.Ncols)))
        
    def toggle_guess(self, i):
        if(self.guess[i]== 0):
            self.guess[i] = 1
            self.buttons[i].config(bg = "green yellow")
        else:
            self.guess[i] = 0
            self.buttons[i].config(bg = "light pink")
            
    def check_score(self, pattern, guess):
        score = np.sum(pattern == guess)
        return score
     
    def rescore(self):
        self.score = self.check_score(self.pat, self.guess)    
        self.labelText.set("Score: " + str(self.score))
        self.labelTrials.set("Trials: " + str(self.trials))
        self.trials += 1        
        self.solve()
        self.log()
    
    def solve(self): 
        x1 = self.guess
        x2 = 1-self.guess
        y1 = (np.sum(self.guess) - (self.total_zeros - self.score))/2
        y2 = self.total_ones - y1
        
        ## sanity checks ####
        # print("check1:", y1, x1)
        # print("check2:", y2, x2)
        # print("check3:", float(self.total_ones), self.pat)
        # r1 = x1 @ self.pat
        # r2 = x2 @ self.pat
        # print("r1:", r1, "y1:", y1, "r2:", r2, "y2:", y2)
        # assert(r1==y1)
        # assert(r2==y2)   
            
        self.xs.append(x1.copy())
        self.xs.append(x2.copy())         
        self.ys.append(y1)
        self.ys.append(y2)    
        res = lsq_linear(self.xs, self.ys, bounds=(0, 1))
        self.wT = np.round(res.x, 2)*100
        self.wF = 100-self.wT
        for i in range(self.N):
            self.text[i] = StringVar()
            self.text[i].set('T .%d' % (self.wT[i]))        
            self.buttons[i].config(textvariable = self.text[i])
            
            
            
           
print("*******************")
print("Running The Gui Interface")
gui = PredictPattern()
gui.restart()
gui.root.mainloop()
            
            
            
            
            
            
            
            
            
            
            
            
            
            

