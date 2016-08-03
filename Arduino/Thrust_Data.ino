/*   
  Force Sensor Reading
  
  modified 19 March 2016
  by Josh Cook
*/
 
int potPin = 0;    // Analog input pin attached to (A0)
int potValue = 0;  // value read from the force sensor
float mass = 0.0;
float thrust = 0.0;
float t = 0.0;
 
void setup() {
  Serial.begin(9600);     // initialize serial communications at 9600 bps (for serial monitor output)
  while(!Serial);
  Serial.println("time,thrust");
}
 
void loop() {
  potValue = analogRead(potPin); // read the potential value from the specified analog pin (returns value 0 to 1023)
  if(potValue > 0) {
    mass = (1.7 * potValue) + 16.6;
    thrust = (mass / 1000) * 9.8;
    t = t + 0.1;
  }
  else {
    thrust = 0.0;
  }
  
  Serial.print(t);
  Serial.print(",");
  Serial.println(thrust);      // print the potential value back to the serial monitor
  
  delay(100);                     // wait 10 milliseconds before the next loop
  
}
