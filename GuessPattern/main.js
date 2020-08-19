//layer=[];


mem=[];
cell=[];
pat=[];
mypat=[];
score=[];
//trial=0;
shift=40;
//rec=false;
hide=true;
trials=8;
state=0;
level=1;

answer_shift=50;
pat_shift=110;
x_shift=100;
y_shift=100;

restartX=300;
restartY=20;

quiz_num=10;
ball_size=40;

gameStarted=false;

function setup(){

    createCanvas(360,640);
    background(0);
    
    // fill(0);
    // rect(0,0, 360, 640);
    // level1=new unitStart();
    // level2=new unitStart();
    // level3=new unitStart();

    // level1.display();
    // level2.display();
    // level3.display();



    gameRestart();

}

function levels(){
    if(level==1){
        quiz_num=4;
    }else if(level==2){
        quiz_num=8;
    }else{
        quiz_num=10;
    }
}

function gameStates(){
    fill(220);
    if(state==0){
        text("Guess Pattern", 140, 20)
    }else if(state==1){
        text("You Win",140,20);
    }else{
        text("You Lose", 140,20);
    }

}

function gameRestart(){
    state=0;
    gameStates();
    trials=8;
    hide=true;
    for(var i=0; i<quiz_num; i++){
        mem[i]=0;
       // score[i]=0;
        cell[i]=new unit();
    }
    genPat();
    restart=new unitRestart();
    restart.x=restartX;
    restart.y=restartY;
    restart.display();

    hideScore=new unitRect();
    hideScore.x=20;
    hideScore.y=10;
    hideScore.xWidth=90;
    hideScore.display();
    scoreShow();

}

function draw(){
    // if(gameStarted==true){
        myscore(checkAnswer());
        displayCells();
        displayPat();
        if(state==0){
            recDisplay();  
        }
        mytrials="remaining trials: "+"\n" +trials;
        fill(220);
        text(mytrials, 20,70);

        if(hide==true){
            hideScore.display();
        }
       restart.display();
       fill(220);
       text("restart", restartX,restartY+60);
       gameStates();
 // }

}


function genPat(){
    for(var i=0; i<quiz_num; i++){
        mypat[i]=round(random(0,1));
    }
    return mypat;
}


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

function displayCells(){
    
    for(var i=0; i<quiz_num; i++){
        cell[i].answer=mem[i];
        cell[i].x=answer_shift+x_shift;
        cell[i].y=y_shift;
        cell[i].y+=i*ball_size;
        cell[i].display();
    }
}

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
       recDisplay(); 
    }
   scoreShow();
}
   if(checkBoundery(restart)){
    gameRestart();
   }
    }
}


function scoreShow(){
    if(checkBounderyRect(hideScore)){
        hide=false;
        trials=trials-1;
        if(trials==0 && checkAnswer()<quiz_num){
            state=2;
        }else if(checkAnswer()==quiz_num){
            state=1;
        }else{
            state=0;
        }
    }else{
        hide=true;
    }
}

function myscore(myfinal){
    background(0);
    sc="score " + myfinal +"/" + quiz_num;
    fill(200);
    textSize(16);
    text(sc,20,30);
}

function recDisplay(){
    fill(100)
    rect(210,100,ball_size+20,ball_size*quiz_num);
    text(" hidden", 210,95)
    text(" guess", 140,95)
  
}


function checkAnswer(){

   prefinal=score.reduce(add,0);
    for(var i=0; i<quiz_num; i++){
        if(mypat[i]==mem[i]){
            score[i]=1;
        }else{
            score[i]=0;
        }
    }
    
    final=score.reduce(add,0);
    return final;
//    console.log(final);
}
function add(a,b){
    return a+b;
}

function unit(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;

    this.display=function(){

        if(this.answer==0){
            fill(100);
        }else if (this.answer==1){
            fill(200, 200,0);
        }
        ellipseMode(CORNER)
        ellipse(this.x,this.y,ball_size,ball_size);
        
    };

}

function unitRestart(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;

    this.display=function(){

        fill(200,0,0);
        ellipseMode(CORNER)
        ellipse(this.x,this.y,ball_size,ball_size);
        
    };

}

function unitRect(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;
    this.xWidth=40;
    this.yWidth=30;

    this.display=function(){

        fill(200, 200, 0);
        rectMode(CORNER)
        rect(this.x,this.y,this.xWidth,this.yWidth);
        fill(0);
        text(" show score",this.x, this.y+20);
        
    };

}


function unitStart(){

    this.answer=0;
    this.x=230+shift;
    this.y=100;
    this.xWidth=30;
    this.yWidth=30;
    this.mytext="Level /"+ level;
    this.display=function(){

        fill(200);
        rectMode(CORNER)
        rect(this.x,this.y,this.xWidth,this.yWidth);
        fill(0);
        text("Level",this.x, this.y+20);
        
    };

}


function toggle(answer){
    if(answer==0){
        answer=1;
    }else{
        answer=0;
    }

    return answer;
}

function checkBoundery(unit){

    if(mouseX>unit.x && mouseX<unit.x+ball_size
    && mouseY>unit.y && mouseY<unit.y+ball_size){
        return true;
    }else{
        return false;
    }
   
}

function checkBounderyRect(unit){

    if(mouseX>unit.x && mouseX<unit.x+unit.xWidth
    && mouseY>unit.y && mouseY<unit.y+unit.yWidth){
        return true;
    }else{
        return false;
    }
   
}