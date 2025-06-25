#include <Arduino.h>
#include <CircularBuffer.h>

CircularBuffer<float, 20> tempWindow;

const int tempPin = A0;
const float resistor = 263.355;
float a;
float b;

const int temp_1 = 0;
const int temp_2 = 1300;

const int outputPin = 3;
const int inputPin = 4;

bool stop_tracking = false;
const float target_temp = 29;

void setup() {
  Serial.begin(9600);
  pinMode(outputPin, OUTPUT);
  digitalWrite(outputPin, LOW);
  pinMode(inputPin, INPUT);
  analogReadResolution(14);

  float raw1 = 16383 * (0.004 * resistor) / 5;
  float raw2 = 16383 * (0.02 * resistor) / 5;
  a = (temp_2 - temp_1) / (raw2 - raw1);
  b = temp_2 - a * raw2;
}

void loop() {
  Serial.print("Pin 3: ");
  Serial.print(digitalRead(outputPin));
  Serial.print(" | Pin 4: ");
  Serial.println(digitalRead(inputPin));

  if (digitalRead(inputPin) == HIGH) {
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
        Serial.print("Average: ");
        Serial.println(average);

        if (average > target_temp) {
          Serial.println("Target temperature hit, resuming print");
          stop_tracking = true;
          digitalWrite(outputPin, HIGH);
        }

        tempWindow.shift();
      }

      delay(1000);
  }
}
