#include <Wire.h>

int data[] = {2, 13}; //Data pins for the two shift registers
int latch[] = {4, 12}; //Latch pins for the two shift registers
int clk[] = {3, 11}; //Clock pins for the two shift registers

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++) {
    pinMode(data[i], OUTPUT);
    pinMode(clk[i], OUTPUT);
    pinMode(latch[i], OUTPUT);
  }
}

void loop() {
  Wire.onReceive(handler);
}

void handler(int numBytes) {
  int vals[numBytes];
  for (int i = 0; i < numBytes; i++) {
    vals[i] = int(Wire.read());
  }
  
  /*char buffer [50];
  int i = sprintf(buffer, "Vals0: %d    Vals1: %d", vals[0], vals[1]);
  for (int l = 0; l <= i; l++) {
    Serial.print(buffer[l]);
  }*/
  
  displayValues(vals[0], vals[1]);
}

void displayValues(int val, int reg) {
  digitalWrite(latch[reg], LOW);
  shiftOut(data[reg], clk[reg], MSBFIRST, val);
  digitalWrite(latch[reg], HIGH);
}
