#include <stdio.h>

#include <wiringPi.h>
#include <gertboard.h>

int main ()
{
  int x1, x2 ;
  double v1, v2 ;

  printf ("\n") ;
  printf ("Gertboard demo: Simple Thermemeter\n") ;
  printf ("==================================\n") ;

// Always initialise wiringPi. Use wiringPiSys() if you don't need
//	(or want) to run as root

  wiringPiSetupSys () ;

// Initialise the Gertboard analog hardware at pin 100

  gertboardAnalogSetup (100) ;

  printf ("\n") ;
  printf ("| Channel 0 | Channel 1 | Temperature 1 | Temperature 2 |\n") ;

  for (;;)
  {

// Read the 2 channels:

    x1 = analogRead (100) ;
    x2 = analogRead (101) ;

// Convert to a voltage:

    v1 = (double)x1 / 1023.0 * 3.3 ;
    v2 = (double)x2 / 1023.0 * 3.3 ;

// Print

    printf ("|    %6.3f |    %6.3f |", v1, v2) ;

// Print Temperature of both channels by converting the LM35 reading
//	to a temperature. Fortunately these are easy: 0.01 volts per C.

    printf ("          %4.1f |          %4.1f |\r", v1 * 100.0, v2 * 100.0) ;
    fflush (stdout) ;
  }

  return 0 ;
}

