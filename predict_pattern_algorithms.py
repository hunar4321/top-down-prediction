# -*- coding: utf-8 -*-
"""
Predict Hidden Patterns - Exploring Algorthims
@author: Hunar @ brainxyz.com

For more info please check out the associated video: https://youtube.com/@brainxyz/   ?comming soon...
Also, there is a blog post: https://www.brainxyz.com/blog/predict/

The following Algortihms are tried to solve this game: https://hunar4321.github.io/predict-pattern/
0- Brute Force approach, on average, requires 65000 trials to predict a grid of 16 hidden 1s (T) & 0s (F)
1- Linear Algera with 16 different equations can predict unambiguously a grid of 16 hidden 1s (T) & 0s (F) 
2- Single Toggle (Point Mutations) requires 15.5 trials on average for the above
3- Double Toggle can save %25 of the required trials on average compared to above
4- Top Down Prediction can save %50 on average - more or less depending on how much reguilarity exists in the hidden pattern
5- Binary Top Down Prediction can save more than %25 especially if the hidden pattern contains localized regularities
        
"""

## To run the code, numpy and scipy need to be installed
import numpy as np
from scipy.optimize import lsq_linear
import matplotlib.pylab as plt

## simulation results in the video are reported for the random seed=1, N=100, numpy version: 1.21.5
seed = 1 
rng = np.random.RandomState(seed)    
print("numpy version:", np.version.version)

# number of simulations
N = 100

# pattern length (better to be in power of 2 [8, 16, 32, 64, 128,...] to avoid some unchecked problems!)
M = 16

# generate N randomly vectors of M elements: 0 represents F & 1 represents T.
patterns = rng.randint(0, 2, (N, M))

#################### Helper Functions ####################


def check_score(pattern, guess):
    score = np.sum(pattern == guess)
    return score

def print_stat(trials):
    print("Average Number of Trials = ", np.round(np.mean(trials), 2), "| SD =", np.round(np.std(trials), 2))
    
def generate_guess_vectors(M):
    """
    guess_vectors are an arrays of vectors for the initial guesses. It tries to capture regular patterns
    The vectors are square waves starting with low to high frequences. 
    """
    guess_vectors = np.zeros((int(np.log2(M)), M))
    ln = np.linspace(0, 2*np.pi, M)
    for i in range(1, guess_vectors.shape[0]+1):
        t = np.cos(ln*i)
        t[t >= 0] = 1
        t[t < 0 ] = 0
        guess_vectors[i-1] = t.copy()
    # plt.imshow(guess_vectors) #visualize
    return guess_vectors

def simulate(algorithm, patterns, N):
    """
    running N simulaiton for each algorithm to estimate 
    the average trials required to predict the pattern
    """
    trials = np.zeros(N)
    for k in range(N):
        trial = algorithm(patterns[k])
        trials[k] = trial
    print_stat(trials)
    return trials

#################### Algorithm Definitions ################

def algorithm0(pat):
    """
     Brute Force Prediction
    """
    score = 0
    trial = 0
    while(score < M):
        # randomly guess until you find the match!
        guess = rng.randint(0, 2, M)
        score = check_score(pat, guess)
        trial +=1
    return trial
        
def algorithm1(pat):
    """
    Linear Algebra: solves xs @ ws = ys; where xs are our guess matrix, ys are the global scores
    """
    xs = 1-np.eye(M) # generate 16 different equations (16 trials)
    ys = np.zeros((M))
    for i in range(len(ys)):
        ys[i] = check_score(pat, xs[i])
    # linear solution with lower bounds=0 (F) and upper bounds=1 (T)    
    res = lsq_linear(xs, ys, bounds=(0, 1))
    ws = np.round(res.x)
    score = check_score(pat, ws)
    assert(score == M)
    trial = len(xs)
    return trial


def algorithm2(pat):
    """
    Single Toggle Prediction (point mutations)
    """
    guess = [0]*M # set all guesses to 0 initially
    score = check_score(pat, guess)
    trial = 1
    i = 0
    while (score < M):
        pscore = score
        # toggle each guess to 1 one at a time
        guess[i] = 1
        score = check_score(pat, guess)
        # if the new score is lower than previous toggle back to 0
        if(score <= pscore):
            guess[i] = 0
        i += 1
        trial += 1
    return trial

def algorithm3(pat):
    """
    Double Toggle Prediction
    same as single toggle but toggles 2 guesses at once
    """
    guess = np.zeros(M)
    score = check_score(pat, guess)
    trial = 1
    i = 0
    while(score < M):
        guess[i]= 1
        guess[i+1]= 1
        new_score = check_score(pat, guess)
        trial += 1
        delta = new_score - score
        # if the difference +2 or -2 it means we figured out the answer of both toggles
        if(delta == 2):
            score += 2        
        elif(delta == -2):
            guess[i] = 0
            guess[i+1] = 0
        else:
            # else if difference = 0 it means one toggle was correct but the other toggle was not
            # another single toggle + check_score is need to resolve which toggle was correct
            guess[i] = 0
            new_score = check_score(pat, guess)
            trial += 1
            delta = new_score-score
            if(delta == 1):
                score += 1 
            else:
                guess[i]= 1
                guess[i+1]= 0
                score += 1
        i += 2
    return trial
    
def algorithm4(pat):
    """
    Top Down Prediction
    """
    xs = []
    ys = []
    current_belief = np.zeros(M) 
    #initial check score to estimate the total 0s (F) vs total 1s (T)
    score = check_score(pat, current_belief)
    trial = 1
    total_zeros = score
    total_ones = M-total_zeros
    xs.append(current_belief.copy())
    xs.append(1-current_belief.copy())    
    ys.append(total_zeros)
    ys.append(total_ones)
    past_beliefs = []
    
    while(True):
        
        # max upper limit is 1 which represents T and max lower limit is 0 which represents F
        res = lsq_linear(xs, ys, bounds=(0, 1))
        evidence = res.x #evidence are the weight vector (ws) that solve xs @ ws = ys
        
        if( trial < (len(guess_vectors) + 1) ):
            ## this part makes some initial guesses based on a pre-defined guess_vectors (passed as a global variable)
            if(guess_vectors.size != 0):
                current_belief = guess_vectors[trial-1]
            else:
                # inital random guesses still works but pre-defined broadly varied initial guesses are better
                current_belief = rng.randint(0, 2, M)
        else:
            ## record all the guesses
            past_beliefs.append(current_belief.copy())
            
            ## update the current_belief according to the evidence(ws) which ranges from 0.0 to 1.0
            ## sort the evidence and set the higher values to 1 and the lower values to 0                         
            inds = sorted(range(len(evidence)), key=lambda k: evidence[k])        
            current_belief = np.ones(M)
            for t in range(total_zeros):
                current_belief[inds[t]] = 0     
                
            ## compare the current_belief with the past ones    
            for p in range(len(past_beliefs)-1, -1, -1):
                ## if the updated belief == a previous belief and the score still less than M, we are stuck on a local maximum                                    
                if(np.all(past_beliefs[p] == current_belief)): 
                    ## mutate the current belief (Make a large perturbance)                                     
                    mutate = rng.randint(0, 2, M) 
                    for i in range(M):
                        # current_belief[i] = mutate[i]
                        confidence = 0.99
                        if( evidence[i] >= (1-confidence) and evidence[i] < confidence):
                            current_belief[i] = mutate[i]
                    break

        score = check_score(pat, current_belief)
        if(score >= M): 
            break 
        
        ## this part calculates the sum of 1s (Trues) in each part (x1 @ pat = y1) and (x2 @ pat = y2)
        x1 = current_belief
        x2 = 1-current_belief
        y1 = (np.sum(current_belief) - (total_zeros - score))/2
        y2 = total_ones - y1  
        xs.append(x1.copy())
        xs.append(x2.copy())         
        ys.append(y1)
        ys.append(y2)

        ### sanity checks ####
        # r1 = x1 @ pat
        # r2 = x2 @ pat
        # assert(r1==y1)
        # assert(r2==y2)
        
        trial += 1              
        #safety break
        if(trial > (M*2)):
            break
        
    return trial        
 
class Node:
    """
     This approach is recommended by ChatGPT. A Fun Conversation here: https://twitter.com/hunar012/status/1598327049516630019
     I also detailed it in this blog: https://www.brainxyz.com/blog/predict/
     This approach is same as the Top Down approach, less flexable but faster and may work better for localized patterns
    
    """
    def __init__(self, M):
        self.id = -1
        self.pos = 0
        self.left = None
        self.right = None
        self.parent = None
        self.state = 0
        self.total = 1
        self.score = 0
        self.guess = [0]*M
        self.prob = 0.5
        
class Tree():
    def __init__(self, M):
        self.node = Node(M)
        self.id = -1
        self.M = M
        self.trial = 0
        self.confidence = 0.99
        self.depth = int(np.log2(M)) 
        self.create_tree(self.node, self.depth)
        self.patList = []
        self.get_pattern(self.node, self.patList)
        
    def fill_list(self, lst, start, stop, val):
        for i in range(start, stop):
            lst[i] = val 
            
    def create_tree(self, node, depth):
        self.id +=1
        node.id = self.id
        if(depth > 0):
            left = Node(self.M)
            right = Node(self.M)
            left.parent = node
            right.parent = node
            left.pos = node.pos
            shift = 2**(depth-1)
            right.pos = node.pos + shift
            self.fill_list(left.guess, left.pos, right.pos, 1)
            self.fill_list(right.guess, right.pos, right.pos + shift, 1)
            node.left = left
            node.right = right
            node.total = 2**depth
            node.score = 0
            depth = depth-1
            self.create_tree(node.left, depth)
            self.create_tree(node.right, depth)
            
    def print_tree(self, node):
        print("guess:", node.guess, "total:", node.total, "score:", node.score)
        if(node.left != None):
            self.print_tree(node.left)
            self.print_tree(node.right) 
            
    def get_pattern(self, node, patList):
        patList.append(node.guess)
        if(node.left != None):
            self.get_pattern(node.left, patList)
            self.get_pattern(node.right, patList)              
            
    def _predict_pattern(self, nodeLeft, nodeRight, pat, total_zeros):
        guess_score = check_score(nodeLeft.guess, pat)
        self.trial +=1
        delta = total_zeros - guess_score
        left_0 = (delta + nodeLeft.total)/2
        right_0 = nodeLeft.parent.score - left_0
        nodeLeft.score = left_0
        nodeRight.score = right_0
        nodeLeft.prob = left_0/nodeLeft.total
        nodeRight.prob = right_0/nodeLeft.total
        if(nodeLeft.left != None):
            if(nodeLeft.prob > (1-self.confidence) and nodeLeft.prob < self.confidence):
                self._predict_pattern(nodeLeft.left, nodeLeft.right, pat, total_zeros)
            if(nodeRight.prob > (1-self.confidence) and nodeRight.prob < self.confidence):                
                self._predict_pattern(nodeRight.left, nodeRight.right, pat, total_zeros) 
                
    def predict_pattern(self, pat):
        self.trial = 0
        self.node.score = check_score(self.node.guess, pat)
        self.trial +=1
        total_zeros = self.node.score
        self._predict_pattern(self.node.left, self.node.right, pat, total_zeros)
        return self.trial


############################# Simulations ##################################

print("------------------")
print("Running the Simulations...")
print("Pattern Length:", M, "| Iterations:", N)

# print("**************")
# print("[Naive Brute Force]")
# trials = simulate(algorithm0, patterns, 10)
    
print("***************")
print("[Linear Algebra Prediction]")
trials = simulate(algorithm1, patterns, N)

print("**************")
print("[Single Toggle Prediction]")
trials = simulate(algorithm2, patterns, N)

print("**************")
print("[Double Toggle Prediction]")
if( M%2 == 0 ):
    trials = simulate(algorithm3, patterns, N)
else:
    print("Incorrect Results! M should be an even number for double toggle approach")

print("********************")
print("[Binary Top Down Predcition]")
isLog2 = ((M & (M-1) == 0) and M != 0)
if(isLog2):
    btree = Tree(M) 
    # btree.print_tree(btree.node)  
    trials = simulate(btree.predict_pattern, patterns, N)          
else:
    print("Incorrect Results! M should be power of 2 for binary try approach")
    
print("********************")
print("[Top Down Prediction]")
guess_vectors = generate_guess_vectors(M) 
#guess_vectors passed as a global variable to algorithm4
trials = simulate(algorithm4, patterns, N)
print("-------------------")
print("Trials:")
print(trials)

print("*****************************************************")

################################## Testing with Regular Patterns ########################################

print("Running the Simulations for more regular patterns...")

## 1D vectors representing letters # A C H O T I L S (because of the small grid only these few letters could be represented)
patterns = np.asarray([
    [1., 1. ,1. ,1., 1., 0., 0., 1., 1., 1., 1., 1., 1., 0., 0., 1.], #A
    [1., 1., 1., 1., 1., 0., 0., 0., 1., 0., 0., 0. ,1., 1., 1. ,1.], #C
    [1,  0,  0  ,1,  1  ,1  ,1,  1  ,1,  0  ,0  ,1  ,1  ,0  ,0,  1 ], #H
    [1., 1., 1., 1., 1., 0. ,0. ,1., 1. ,0. ,0. ,1., 1., 1., 1., 1.], #O
    [1. ,1., 1., 1., 0., 1., 1., 0., 0. ,1. ,1. ,0., 0., 1. ,1., 0.], #T
    [1. ,1. ,1., 1., 0. ,1., 1., 0., 0. ,1. ,1. ,0., 1. ,1., 1., 1.], #I
    [1. ,0., 0., 0., 1. ,0., 0., 0. ,1., 0. ,0., 0. ,1., 1., 1. ,1.], #L
    [1. ,1. ,1. ,1. ,1., 0. ,0. ,0. ,1. ,1., 1., 1. ,1., 1., 1. ,1.], #S
    ])

## visualize pattern
# ind = 2
# pat2d = np.reshape(patterns[ind], (4 , 4))
# plt.imshow(pat2d)

N = patterns.shape[0]
M = patterns.shape[1]

print("Pattern Length:", M, "| Iterations:", N)

    
print("***************")
print("[Linear Algebra Prediction]")
trials = simulate(algorithm1, patterns, N)

print("**************")
print("[Single Toggle Prediction]")
trials = simulate(algorithm2, patterns, N)

print("**************")
print("[Double Toggle Prediction]")
if( M%2 == 0 ):
    trials = simulate(algorithm3, patterns, N)
else:
    print("Incorrect Results! M should be an even number for double toggle approach")

print("********************")
print("[Binary Top Down Predcition]")
isLog2 = ((M & (M-1) == 0) and M != 0)
if(isLog2):
    btree = Tree(M) 
    # btree.print_tree(btree.node)  
    trials = simulate(btree.predict_pattern, patterns, N)          
else:
    print("Incorrect Results! M should be power of 2 for binary try approach")
    
print("********************")
print("[Top Down Prediction]")
guess_vectors = generate_guess_vectors(M) 
#guess_vectors passed as a global variable to algorithm4
trials = simulate(algorithm4, patterns, N)
print("-------------------")
print("Trials:")
print(trials)
