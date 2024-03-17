#include <Arduino.h>
#include <LedControl.h>
#include "../array.cpp"

LedControl control = LedControl(12, 11, 10, 4);

void setup() {
  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1A |= B00000101;
  TIMSK1 |= B00000010;
  OCR1A = 5207;
  sei();

  control.shutdown(0,false);
  /* Set the brightness to a medium values */
  control.setIntensity(0,8);
  /* and clear the display */
  control.clearDisplay(0);

}

void loop() {}

ISR(TIMER2_COMPB_vect) { 
  
}