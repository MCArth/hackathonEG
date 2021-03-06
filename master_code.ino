#include <Wire.h>

int data[] = {2, 13}; //Data pins for the two shift registers
int latch[] = {4, 12}; //Latch pins for the two shift registers
int clk[] = {3, 11}; //Clock pins for the two shift registers

int binVal[] = {1, 2, 4, 8, 16, 32, 64, 128, 256}; //Binary values to 2^8

int playerLoc[] = {0, 5}; //Contains players current location of the top of their paddle
int playerPotVal[] = {2, 2}; //Contains player pot mapped values (0 is paddle moving down fast, 5 is moving up fast, 2, 3 are not moving)
int playerWaits[] = {10, 10}; //Contains the remaining wait of the player
int playerScores[] = {0, 0}; //Contains the score of each player
int ballLocation[] = {5, 3}; //Contains the balls location WHERE 1, 1 is bottom left of the grid row, column
//(I'm not sure how we're using the LED matrixes so you'll almost definitely have to change these values to fit how we actually need it)

int ballAngle = 135; //Angle of ball (45 is going towards top right of grid
int potPin[] = {A0, A1}; //Need to add resistor on pin A1
unsigned long previous = 0;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++) {
    pinMode(data[i], OUTPUT);
    pinMode(clk[i], OUTPUT);
    pinMode(latch[i], OUTPUT);
  }
}

void loop() {

  //Make ball move at certain speed
  if (millis() - previous >= 1000) {
    moveBall();

    previous = millis();
  }
  readPotVals(1);
  readPotVals(2);
  checkWait(1);
  checkWait(2);

  unsigned long start = millis();
  while (millis() < start + 100) {
    //Display player 1 paddle
    outPut(binVal[0], 1);
    outPut(rowsValGen(1), 0);
    clearMatrix();
    //Display player 2 paddle
    outPut(binVal[7], 1);
    outPut(rowsValGen(2), 0);
    clearMatrix();
    //Display ball
    outPut(binVal[ballLocation[0]], 1);
    outPut(255 - binVal[ballLocation[1]], 0);
    clearMatrix();
  }
}

//reg 0 = rows, 1 = columns
void outPut(int val, int reg) {
  Wire.beginTransmission(1);
  Wire.write(byte(val));
  Wire.write(byte(reg));
  Wire.endTransmission();
  
}

void readPotVals(int player) {
  int i = player - 1;

  int potVal = analogRead(potPin[i]);
  int mappedVal = map(potVal, 0, 1023, 0, 5); //Maps potentiometer value to 0 to 5, where 0 is paddle moving down
  playerPotVal[i] = mappedVal;
  if (mappedVal == 2 || mappedVal == 3) { //If in middle, player paddle permanently does not move as wait stays on 10
    playerPotVal[i] = mappedVal;
    playerWaits[i] = 10;
  }

  //Changes wait value based on speed player wishes
  else if (playerWaits[i] > 0) {

    if (mappedVal == 0 || mappedVal == 5) {
      playerWaits[i] -= 2;
    }

    else { //For values mappedVal == 1 or == 4
      playerWaits[i]--;
    }
  }

  //Resets wait if bat has just been moved
  else {
    playerWaits[i] = 4;
  }
}

//Generates value to write to row shift reg
int rowsValGen(int player) {
  int rows = 0;
  for (int i = 0; i < 3; i++) {
    rows += binVal[playerLoc[player - 1] + i];
  }
  return 255 - rows;
}

//Outputs a blank matrix with delays for use between displaying
//values on the board
void clearMatrix() {
  delay(1);
  outPut(0, 1);
  outPut(255, 0);
  delay(1);
}

void checkWait(int player) {
  int i = player - 1;
  if (playerWaits[i] < 1) { //If wait is over
    if (playerPotVal[i] < 2) { //If player moving down
      if (playerLoc[i] < 5) {
        playerLoc[i]++;
      }
    }
    else { //If player moving up
      if (playerLoc[i] > 0) {
        playerLoc[i]--;
      }
    }
  }
}

//TODO: endGame - flash LEDs continuously (we could play a tune but I don't think necessary)
//I would say just have players press reset button if they want to play again instead of implementing function for playing again
void endGame() {
  if (playerScores[0] == 10) {
    for (int i = 0; i < 5; i++) {
        outPut(124, 1);
        outPut(255 - binVal[0], 0);
        clearMatrix();
        for (int row = 1; row <= 4; row++) {
          outPut(16, 1);
          outPut(255 - binVal[row], 0);
          clearMatrix();
        }
        outPut(20, 1);
        outPut(255 - binVal[5], 0);
        clearMatrix();
        outPut(24, 1);
        outPut(255 - binVal[6], 0);
        clearMatrix();
        outPut(16, 1);
        outPut(255 - binVal[7], 0);
        clearMatrix();
        delay(150);
    }
  } else {
    for (int i = 0; i < 5; i++) {
        outPut(63, 1);
        outPut(255 - binVal[0], 0);
        clearMatrix();
        outPut(51, 1);
        outPut(255 - binVal[1], 0);
        clearMatrix();
        outPut(6, 1);
        outPut(255 - binVal[2], 0);
        clearMatrix();
        outPut(28, 1);
        outPut(255 - binVal[3], 0);
        clearMatrix();
        outPut(48, 1);
        outPut(255 - binVal[4], 0);
        clearMatrix();
        outPut(51, 1);
        outPut(255 - binVal[5], 0);
        clearMatrix();
        outPut(30, 1);
        outPut(255 - binVal[6], 0);
        clearMatrix();
        delay(150);
    }
  }
}

/*
   Function to increment score of player, flash ball, check win condition and resest game
   Parameters: int player: the player which scored
*/
void scorePoint(int player) {
  //get zero indexed player value
  int i = player - 1;
  playerScores[i]++;
  //Flashes ball 5 times
  for (int i =  0; i < 5; i++) {
    clearMatrix();
    outPut(binVal[ballLocation[0]], 1);
    outPut(255 - binVal[ballLocation[1]], 0);
    delay(250);
    clearMatrix();
    delay(250);
  }
  //Check win condition
  if (playerScores[i] == 10) {
    endGame();
  }
  //Reset game
  ballLocation[0] = 3;
  ballLocation[1] = 5;
  ballAngle = 45;
}

void moveBall() {
  boolean pointOver = false;

  //Moving ball in direction it wants to be moved
  if (!(pointOver)) {
    if (ballAngle == 0) {
      ballLocation[0] -= 1;
    } else if (ballAngle == 45) {
      ballLocation[0] -= 1;
      ballLocation[1] -= 1;
    } else if (ballAngle == 135) {
      ballLocation[0] -= 1;
      ballLocation[1] += 1;
    } else if (ballAngle == 180) {
      ballLocation[1] += 1;
    } else if (ballAngle == 225) {
      ballLocation[0] += 1;
      ballLocation[1] += 1;
    } else if (ballAngle == 315) {
      ballLocation[0] += 1;
      ballLocation[1] -= 1;
    }
  }

  if (ballLocation[0] == 7) {
    scorePoint(1);
    pointOver = true;
  }
  else if (ballLocation[0] == 0) {
    scorePoint(2);
    pointOver = true;
  }

  if (ballLocation[0] == 6 && playerLoc[1] - ballLocation[1] >= -3 && playerLoc[1] - ballLocation[1] <= 1) {
    if (playerLoc[1] - ballLocation[1] == -3) {
      if (ballAngle == 315) {
        ballAngle += 180;
      }
    }
    else if (playerLoc[1] - ballLocation[1] == 1) {
      if (ballAngle == 225) {
        ballAngle += 180;
      }
    }
    else {
      if (ballAngle == 225) {
        ballAngle = 135;
      }
      else if (ballAngle == 315) {
        ballAngle = 45;
      }
    }
  }

  if ((ballLocation[0] == 1) && (playerLoc[0] - ballLocation[1] >= -3) && (playerLoc[0] - ballLocation[1] <= 1)) {
    if (playerLoc[0] - ballLocation[1] == -3) {
      if (ballAngle == 45) {
        ballAngle += 180;
      }
    }
    else if (playerLoc[0] - ballLocation[1] == 1) {
      if (ballAngle == 135) {
        ballAngle += 180;
      }
    }
    else {
      if (ballAngle == 45) {
        ballAngle = 315;
      }
      else if (ballAngle == 135) {
        ballAngle = 225;
      }
    }
  }
  //Bouncing off top and bottom wall (where the bats aren't)
  if (ballLocation[1] == 7) {
    if (ballAngle == 225) {
      ballAngle = 315;
    } else if (ballAngle == 135) {
      ballAngle = 45;
    }
  }
  else if (ballLocation[1] == 0) {
    if (ballAngle == 45) {
      ballAngle = 135;
    } else if (ballAngle == 315) {
      ballAngle = 225;
    }
  }

  /*char buffer [50];
  int i = sprintf(buffer, "Location[0]: %d   Location[1]: %d    Angle: %d", ballLocation[0], ballLocation[1], ballAngle);
  for (int l = 0; l <= i; l++) {
    Serial.print(buffer[l]);
  }
  i = sprintf(buffer, "    Bat1: %d    Bat2: %d", playerLoc[0], playerLoc[1]);
  for (int l = 0; l <= i; l++) {
    Serial.print(buffer[l]);
  }
  Serial.println();*/

  //Ensure ballAngle 0 <= ballAngle < 360
  ballAngle = ballAngle % 360;
  if (ballAngle < 0) {
    ballAngle *= -1;
  }

}
