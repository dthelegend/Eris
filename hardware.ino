#include <Adafruit_NeoPixel.h>
#include <Servo.h>  // Include the Servo library

#define PIN        6  // Pin where the first LED strip is connected
#define PIN2       8  // Pin where the second LED strip is connected
#define BUZZER_PIN 7  // Pin where the buzzer is connected
#define SERVO_PIN  9  // Pin where the servo is connected
#define NUM_LEDS  45  // Total number of LEDs in the first strip
#define NUM_LEDS2  9   // Total number of LEDs in the second strip 

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2(NUM_LEDS2, PIN2, NEO_GRB + NEO_KHZ800);
Servo myServo;       // Create a Servo object

void setup() {
  strip.begin();
  strip2.begin();
  strip.show(); // Initialize all pixels to 'off'
  strip2.show();
  pinMode(BUZZER_PIN, OUTPUT); // Set buzzer pin as output

  // Turn on all LEDs in strip2 to white
  for (int i = 0; i < NUM_LEDS2; i++) {
    strip2.setPixelColor(i, strip2.Color(255, 255, 255)); // White color
  }
  strip2.show(); // Update strip2 to show white light

  // Initialize random seed
  randomSeed(analogRead(0));

  // Attach the servo to the specified pin
  myServo.attach(SERVO_PIN);
  myServo.write(0); // Set initial position (0 degrees)

  Serial.begin(9600);
  while (!Serial) {
    ;
  }
}

bool lightsOut() {
    // Light up the last 5 LEDs in red, one at a time
  for (int i = NUM_LEDS - 5; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0)); // Red color
    strip.show();
    
    // Sound the buzzer for a short beep
    tone(BUZZER_PIN, 1200); // 1200 Hz frequency
    delay(200);             // Buzzer sound duration
    noTone(BUZZER_PIN);     // Stop the sound

    delay(800);             // Wait for the rest of the interval
  }

  // Random delay between 200 ms and 2000 ms
  int delayTime = random(200, 2001); // 2001 to include 2000
  delay(delayTime);

  // Turn off all LEDs
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0)); // Turn off the LED
  }
  strip.show();

  // Sound the buzzer when all LEDs are turned off
  tone(BUZZER_PIN, 1500); // 1500 Hz frequency
  delay(400);             // Buzzer sound duration  
  Serial.println("GO");
  delay(1600);
  noTone(BUZZER_PIN);     // Stop the sound
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
  
    if (command == "LIGHTS") {
      lightsOut();
    }
    if (command == "WAVE"){
      waveFlag();
    }
  }
}

void waveFlag() {
  for (int i = 0; i < 20; i++) {
    myServo.write(130);  // Move the servo down to 90 degrees
    delay(300);        // Wait for the servo to reach the position
    myServo.write(45);   // Move the servo back to 0 degrees
    delay(300);
  }
}

