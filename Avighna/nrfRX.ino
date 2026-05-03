#include <SPI.h>
#include <RF24.h>
#include <printf.h>

RF24 radio(48,53);

void setup()
{
Serial.begin(9600);

printf_begin();

if(!radio.begin())
{
Serial.println("Radio failed");
while(1);
}

Serial.println("Radio detected");

radio.printDetails();
}

void loop(){}