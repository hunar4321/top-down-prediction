![GitHub repo size](https://img.shields.io/github/repo-size/hunar4321/Guess_Pattern)
![GitHub](https://img.shields.io/github/license/hunar4321/Guess_Pattern)

# Predict Pattern 

Suppose you are in an exam and you have to answer a set of True or False questions. Also, suppose you do not know the correct answers to any of the questions. In this situation, all you can do is random guessing and normally your chance score will be around 50%. Let’s say the teacher who marks your work gives you many more trials to answer the same set of the questions and you can peek at your total score at the end of each trial. What is the optimal way to maximize the information gain from your past trials to reach the perfect score with a minimal number of trials?
The obvious answer is to mutate the choices one by one and peak at your total score after each trial until your reach the perfect score. In this case, if you have 100 true and false questions. First, set all your choices to false and by chance you may get 50 correct answers. Then, change each of your false choices to true and peek at the the total score again to see if your change increased the total score. This way you might need up to 100 trials to reach perfect score! However, if you mutate more than one question at the same time before peeking at your total score, it's possible to gain more information and reach the perfect score with less trials but it gets trickier as you mutate more questions at the same time.

For more inforation about this game and the optimal strategy to win please read this blog: 

https://www.brainxyz.com/blog/predict/


To play the game on your browser:

https://hunar4321.github.io/predict-pattern/

To run the simulations:

predict_pattern_algorithms.py


![](screen_shot.PNG)
</br>
