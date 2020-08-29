//layer=[];


mem=[];
cell=[];
pat=[];
mypat=[];
score=[];
shift=40;
hide=true;
trials=8;
state=0;
level=1;

answer_shift=50;
pat_shift=110;
x_shift=100;
y_shift=100;

restartX=30;
restartY=10;

mainX = 290
mainY = 10

var quiz_num=8;
ball_size=40;
txtSize = 16
gameStarted=false;

imessage = ""
state=10;


var w = window.innerWidth;
var h = window.innerHeight;

/// generates the true and false set (randomly)
function genPat(){
    for(var i=0; i<quiz_num; i++){
        mypat[i]=round(random(0,1));
    }
    return mypat;
}

// display the answer circles (hidden)
function displayPat(){
    for(var i=0; i<quiz_num; i++){
        pat[i]=new unit();
        pat[i].answer=mypat[i];
        pat[i].x=pat_shift+x_shift;
        pat[i].y=y_shift;
        pat[i].y+=i*ball_size;
        pat[i].display();
    }   
}

// hiddes the answer circles (draws over them)
function displayHiddenPat(){
    for(var i=0; i<quiz_num; i++){
        pat[i]=new unit();
        pat[i].answer=3;
        pat[i].x=pat_shift+x_shift;
        pat[i].y=y_shift;
        pat[i].y+=i*ball_size;
        pat[i].display();
    }   
}

// display all the guessing circles
function displayCells(){    
    for(var i=0; i< quiz_num; i++){
        cell[i].answer=mem[i];
        cell[i].x=answer_shift+x_shift;
        cell[i].y=y_shift;
        cell[i].y+=i*ball_size;
        cell[i].display();
    }
}

function gameStates(){
    fill(200,200,0)
    textSize(txtSize+2);
    if(state == 10){
        text("Guess Better", 130, 25)
        fill(220);
        textSize(txtSize);
        text("Please Select Your Level:", 100, 50)
        text("How to Play:", 140, 300)        
        mm = "Guess a hidden array of True or False \nchoices. You can peek your score for \na limited number of trials. To win: \n   - Use more Brain, less Luck! \n   - Learn from your past trials.\n   - Find an optimal strategy. \n\nAn article about optimal strategy at:"
        ww = "www.brainxyz.com/blog/guessbetter"
        text(mm, 50, 410)
        fill(200,200,0)
        text(ww, 50, 510)
    }
    else if(state==0){
        text("Guess T or F", 140, 20)
    }else if(state==1){
        text("You Win", 140, 20);
    }else{
        text("You Lose", 140, 20);
    }
}

// re-sets the game set
function gameRestart(cstate){
    state=cstate
    gameStates();
    trials=8;
    hide=true;
    for(var i=0; i<quiz_num; i++){
        mem[i]=0;
        cell[i]=new unit();
    }
    genPat();
    restart=new unitRestart();
    restart.x=restartX;
    restart.y=restartY;
    //restart.display();

    main=new unitRestart();
    main.x=mainX;
    main.y=mainY;

    hideScore=new unitRect();
    hideScore.x=20;
    hideScore.y=200;
    hideScore.xWidth=90;
}

// calculate the score
function scoreShow(){
    if(checkBounderyRect(hideScore)){
        hide=false;
        trials=trials-1;
        if(trials==0 && checkAnswer() < quiz_num){
            state=2;
            imessage = ""
        }else if(checkAnswer() == quiz_num){
            state=1;
            imessage = ""
        }else{
            state=0;
            mytrials=trials + " trials\nremains!";
            imessage = checkAnswer() + " of "+ quiz_num+ "\nare correct!\n" + "Not perfect!\nGuess Better!"
        }
    }else{
        hide=true;
        imessage = ""
    }
}

// display score
function myscore(myfinal){
    background(0);
    //sc="score " + myfinal +"/" + quiz_num;
    sc=""
    fill(200);
    textSize(txtSize);
    text(sc,30,225);
    text(imessage, 30, 310)
}

// display some text
function recDisplay(){
    fill(150)
    sguess= "   your\nguesses"
    sanswer=" hidden\nanswers"
    text(sguess, 138,80)
    text(sanswer, 210,80)
}

function add(a,b){ return a+b; }

// checks the current total score for the answers
function checkAnswer(){

    // prefinal=score.reduce(add,0);
    // for(var i=0; i<quiz_num; i++){
    //     if(mypat[i]==mem[i]){ score[i]=1;
    //     }else{ score[i]=0; }
    // }
    
    // final=score.reduce(add,0);
    // return final;

    total = 0;
    for(var i=0; i<quiz_num; i++){
        if(mypat[i]==mem[i]){ 
            total +=1;
        }
    }

    return total

}

// for displaying the guesses and the hidden answers (circles)
function unit(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;

    this.display=function(){

        if(this.answer==0){
            fill(255, 26, 26);
            ans = "F"
        }else if (this.answer==1){
            fill(0, 230, 153);
            ans = "T"
        }else{
            fill(100, 100, 100);
            ans = "H"
        }
        ellipseMode(CORNER)
        ellipse(this.x,this.y, ball_size, ball_size);
        fill(0)
        text(ans, this.x+15, this.y+25)
    };
}

// for displaying the restart button
function unitRestart(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;
    this.display=function(){
        fill(102, 153, 255); 
        ellipseMode(CORNER)
        ellipse(this.x,this.y,ball_size,ball_size);        
    };
}


// for displaying the show score button
function unitRect(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;
    this.xWidth=40;
    this.yWidth=40;

    this.display=function(){

        fill(200, 200, 0);
        rectMode(CORNER)
        rect(this.x,this.y,this.xWidth,this.yWidth);
        fill(0);
        text(" Peek Score",this.x, this.y+25);  
    };
}

// for displaying Level buttons at the start
function unitLevel(){

    this.levelName="";
    this.qnum=7;
    this.x=230+shift;
    this.y=100;
    this.xWidth=80;
    this.yWidth=40;

    this.display=function(){

        fill(200, 200, 0);
        rectMode(CORNER)
        rect(this.x,this.y,this.xWidth,this.yWidth);
        fill(0);
        text(this.levelName,this.x, this.y+25);  
    };
}

function toggle(answer){
    if(answer==0){ answer=1; }else{ answer=0; }
    return answer;
}

// checking the bounderies for the mouse click (circular objects)
function checkBoundery(unit){

    if(mouseX>unit.x && mouseX<unit.x+ball_size
    && mouseY>unit.y && mouseY<unit.y+ball_size){ 
        return true;
    }else{
        return false;
    }
   
}

// checking the bounderies for the mouse click (rectangular objects)
function checkBounderyRect(unit){

    if(mouseX>unit.x && mouseX<unit.x+unit.xWidth
    && mouseY>unit.y && mouseY<unit.y+unit.yWidth){
        return true;
    }else{
        return false;
    }
   
}

function setup(){

    //createCanvas(360,640);
    createCanvas(w, h)
    //frameRate(32);
    background(0);    
    gameRestart(state);

    L1 = new unitLevel()
    L2 = new unitLevel()
    L3 = new unitLevel()

    L1.levelName = "  Baby"
    L1.qnum = 8;
    L1.x = 140
    L1.y = 80
    L2.levelName = "  Amateur"
    L2.qnum = 10; 
    L2.x = 140
    L2.y = 140   
    L3.levelName = "  Master"
    L3.qnum = 12; 
    L3.x = 140
    L3.y = 200        
}

function draw(){

    background(0)
    if(state == 10){
        L1.display()
        L2.display()       
        L3.display()

     }else{
        myscore(checkAnswer());
        displayCells();
        displayPat();
        if(state==0){
            displayHiddenPat()
            recDisplay()
        }
        mytrials="remaining \ntrials: "+" " + trials;
        fill(220);
        text(mytrials, 30,160);

       hideScore.display()
       restart.display();
       main.display();
       fill(220);
       text("restart", restartX,restartY+60);
       text("main", mainX, mainY+60);
    }
    gameStates();

}

// touch events
function touchStarted(){
    if(mouseIsPressed){
        if(state==0){
            myscore(checkAnswer());
            for(var i=0; i<quiz_num; i++){
                if(checkBoundery(cell[i])){
                    cell[i].answer=toggle(cell[i].answer);
                    mem[i]=toggle(mem[i]);
                }   
            }
            displayCells();
            displayPat();
            checkAnswer();
            if(state==0){
                displayHiddenPat()
                recDisplay()
            }
           scoreShow();
        }

       if(checkBoundery(restart)){
            // restarts with state = 0
            gameRestart(0);
       }

        if(checkBoundery(main)){
            // back to main menu with state = 10
            gameRestart(10);
       } 

       if(state==10){

            if(checkBounderyRect(L1)){
                quiz_num = L1.qnum
                state = 0
                gameRestart(state)
            }
            if(checkBounderyRect(L2)){
                quiz_num = L2.qnum
                state = 0
                gameRestart(state)

            }
            if(checkBounderyRect(L3)){
                quiz_num = L3.qnum
                state = 0
                gameRestart(state)

            }

       }

    }
}


// window.onresize = function() {
//   // assigns new values for width and height variables
//   w = window.innerWidth;
//   h = window.innerHeight;  
//   canvas.size(w,h);
// }