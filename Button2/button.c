
#include <stdio.h>
#include <wiringPi.h>

#define button 17

//Needed if there is a output pin
void cleanUp(void) {
    //digitalWrite(led, 0);
}

int main(void) {

    wiringPiGpioSetup();

    //pinMode(led, OUTPUT);
    pinMode(button, INPUT);

    for(;;){

        delay(1000);
        if(digitalRead(button) == 1){

            printf("Button HIGH\n\r");
        }
        else {
            printf("Button LOW\n\r");
        }
    }
}