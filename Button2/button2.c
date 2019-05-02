#include <stdio.h>
#include <wiringPi.h>

// Array to keep track of our LEDs

int leds [] = { 0, 0, 0 } ;

// scanButton:
//	See if a button is pushed, if so, then flip that LED and
//	wait for the button to be let-go

void scanButton (int button)
{
    printf("Waiting for release");
    if (digitalRead (button) == HIGH)	// Low is pushed
        return ;

  leds [button] ^= 1 ; // Invert state
  digitalWrite (4 + button, leds [button]) ;

  while (digitalRead (button) == LOW)	// Wait for release
  {
    printf("Waiting for release");
    delay (10) ;
  }
}

int main (void)
{
  int i ;

  printf ("Raspberry Pi Gertboard Button Test\n") ;

  wiringPiSetup () ;

// Setup the outputs:
//	Pins 3, 4, 5, 6 and 7 output:
//	We're not using 3 or 4, but make sure they're off anyway
//	(Using same hardware config as blink12.c)

  for (i = 3 ; i < 8 ; ++i)
  {
    pinMode      (i, OUTPUT) ;
    digitalWrite (i, 0) ;
  }

// Setup the inputs

  for (i = 0 ; i < 3 ; ++i)
  {
    pinMode         (i, INPUT) ;
    pullUpDnControl (i, PUD_UP) ;
    leds [i] = 0 ;
  }

  for (;;)
  {
    for (i = 0 ; i < 3 ; ++i)
      scanButton (i) ;
    delay (1) ;
  }
}
