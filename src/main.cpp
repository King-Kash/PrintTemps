// #include <Arduino.h>
// #include <CircularBuffer.h>

// CircularBuffer<float, 20> tempWindow;

// const int tempPin = A0;
// const float resistor = 263.6;
// float a;
// float b;

// const int temp_1 = 0;
// const int temp_2 = 1300;

// const int outputPin = 3;
// const int inputPin = 4;

// // bool stop_tracking = false;
// const float min_temp = 26;
// const float max_temp = 30;

// int currentLayer = 0;

// void setup() {
//   Serial.begin(9600);
//   pinMode(outputPin, OUTPUT);
//   digitalWrite(outputPin, LOW);
//   pinMode(inputPin, INPUT);
//   analogReadResolution(14);

//   float raw1 = 16383 * (0.004 * resistor) / 5;
//   float raw2 = 16383 * (0.02 * resistor) / 5;
//   a = (temp_2 - temp_1) / (raw2 - raw1);
//   b = temp_2 - a * raw2;
// }

// void loop() {
//   // Serial.print("Pin 3: ");
//   // Serial.print(digitalRead(outputPin));
//   // Serial.print(" | Pin 4: ");
//   // Serial.println(digitalRead(inputPin));

//   if (digitalRead(inputPin) == HIGH) {
//     int rawValue = analogRead(tempPin);
//     float temperature = rawValue * a + b;

//     tempWindow.push(temperature);
//       //performs running average with n samples (max 20 samples)
//       float sum = 0;
//       for (int i = 0; i < tempWindow.size(); i++) {
//         sum += tempWindow[i];
//       }
//       float average = sum / tempWindow.size();
//       if (tempWindow.size() >= 20){
//         Serial.print("log,");
//         Serial.println(average);
//         //flag to return control to Duet Board
//         if (average <= max_temp && average >= min_temp) {
//           Serial.println("done");
//           // stop_tracking = true;
//           tempWindow.clear();
//           digitalWrite(outputPin, HIGH);
//           delay(100);
//           digitalWrite(outputPin, LOW);
//           currentLayer += 1;
//         } else if (average < min_temp) {
//           Serial.println("abort");
//           tempWindow.clear();
//         }
//         if (tempWindow.size() >= 20){
//           tempWindow.shift();
//         }
//       }
//       delay(200);
//   }
// }


//VERSION FOR NEW CAMERA SENSOR

#include <Arduino.h>
#include <CircularBuffer.h>

CircularBuffer<float, 20> tempWindow;

const int tempPin = A0;
// const float resistor = 263.6;
float a;
float b;

const int temp_1 = 50;
const int temp_2 = 400;

const int outputPin = 3;
const int inputPin = 4;

// bool stop_tracking = false;
const float min_temp = 150;
const float max_temp = 175;

int currentLayer = 0;

void setup() {
  Serial.begin(9600);
  pinMode(outputPin, OUTPUT);
  digitalWrite(outputPin, LOW);
  pinMode(inputPin, INPUT);
  analogReadResolution(14);

  float raw1 = 0;
  float raw2 = 16383;
  a = (temp_2 - temp_1) / (raw2 - raw1);
  b = temp_2 - a * raw2;
}

void loop() {
  // Serial.print("Pin 3: ");
  // Serial.print(digitalRead(outputPin));
  // Serial.print(" | Pin 4: ");
  // Serial.println(digitalRead(inputPin));

  if (digitalRead(inputPin) == HIGH) {
    int rawValue = analogRead(tempPin);
    float temperature = rawValue * a + b;

    tempWindow.push(temperature);
      //performs running average with n samples (max 20 samples)
      float sum = 0;
      for (int i = 0; i < tempWindow.size(); i++) {
        sum += tempWindow[i];
      }
      float average = sum / tempWindow.size();
      if (tempWindow.size() >= 20){
        Serial.print("log,");
        Serial.println(average);
        //flag to return control to Duet Board
        if (average <= max_temp && average >= min_temp) {
          Serial.println("done");
          // stop_tracking = true;
          tempWindow.clear();
          digitalWrite(outputPin, HIGH);
          delay(100);
          digitalWrite(outputPin, LOW);
          currentLayer += 1;
        } else if (average < min_temp) {
          Serial.println("abort");
          tempWindow.clear();
        }
        if (tempWindow.size() >= 20){
          tempWindow.shift();
        }
      }
      delay(130);
  }
}
