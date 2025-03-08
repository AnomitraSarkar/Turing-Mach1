#include <Serial.h>

void setup(){
    Serial.begin(9600);
  }
  
void loop(){
  if(Serial.isAvailable()){
    Serial.println("Serial init");
  }
    Serial.println("hello");
}