#include <Arduino.h>
#include <CircularBuffer.h>

CircularBuffer<int, 30> tempWindow;
const int tempPin = A0;
float voltage = 0;
float tempeInC = 0;
const float resistor = 263.355;
float a;
float b;
const int temp_1 = 0;
const int temp_2 = 1300;
int i = 0;
const int inputPin = 0;
const int outputPin = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(inputPin, INPUT);
  pinMode(outputPin, OUTPUT);
  analogReadResolution(14);
  float raw1 = 16383 * (0.004 * resistor) / 5;
  float raw2 = 16383 * (0.02 * resistor) / 5;
  a = (temp_2 - temp_1) / (raw2- raw1);
  b = temp_2 - a * raw2;
}

void loop() {
  int rawValue = analogRead(tempPin);
  float temperature = rawValue * a + b;
  tempWindow.push(temperature);
  if (!tempWindow.isFull()) {
    Serial.println("Window not full.");
  } else {
    float sum = 0;
    for (int i = 0; i < tempWindow.size(); i++) {
      sum += tempWindow[i];
    }
    float average = sum / tempWindow.size();
    Serial.println(average);
    tempWindow.shift();
  }
  delay(400);
}
