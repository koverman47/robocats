#include <Servo.h>

/*
 * 2 - +
 * 3 - -
 * 4 - -
 * 5 - -
 * 6 - -
 * 7 - +
 * 8 - +
 * 9 - -
 * 
 */


Servo servo[8];
int neutral = 1500;

int down = 250;
int power = 250;
int scale = 350;

int pins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
int depthPin = 0; 

//float surfacePSI = 10.44; // Check ad hoc
/*float surfacePSI = -1;
float psi;
float depth = 0.0;*/

float error = 0.0;
float dererror = 0.0;
float interror = 0.0;
float dt = 0.0;
float tim;

//PID Gains
float kp = 0.16; // TODO: Tune
float ki = 0.0;
float kd = 0.1;


//float targetDepth = -0.75;
float target = 105;
float command = 0.0;
float measurement;


/*void setSurfacePSI() {
	if(surfacePSI == -1) {
		sensePSI();
		surfacePSI = psi;
	}
}


void sensePSI() {
	psi = (analogRead(depthPin) * 0.0048828125 - 1) * 12.5;
}*/


/*void calcDepthUpdate() {
	sensePSI();
	time =  abs(millis() - time);
	depth = ((analogRead(depthPin) * 0.0048828125 - 1) * 12.5 - surfacePSI) * 0.13197839577;
	// compute dt
	float preverror = error;
	error = depth - targetDepth;
	interror += error * dt;
	dererror = (error - preverror) * dt;
}*/

void calcUpdate() {
    measurement = analogRead(depthPin);
    int temp = millis();
    dt = abs(temp - tim) / 1000;
    tim = temp;
    float preverror = error;
    error = measurement - target;
    interror += error * dt;
    dererror = (error - preverror) * dt;
}


float depthPID() {
	float p = (error * kp);
	float i = (interror * dt * ki);
  float d = (dererror * kd);
  //Serial.println(p);
  //Serial.println(i);
  //Serial.println(d);
	command = p + i + d;
	if(command > 1) {
		command = 1;
	}
	else if(command < -1) {
		command = -1;
	}
	return command;
}


void setup() {
	Serial.begin(9600);
	//setSurfacePSI();
	//calcDepthUpdate();
  calcUpdate();

	int i;
	for(i = 0; i < 8; i++) {
		servo[i].attach(pins[i]);
		servo[i].writeMicroseconds(neutral);
	}

	delay(5000);
	servo[4].writeMicroseconds(neutral - down);
	servo[5].writeMicroseconds(neutral + down);
	servo[6].writeMicroseconds(neutral + down);
	servo[7].writeMicroseconds(neutral - down);
	tim = millis();
}

void loop() {
	calcUpdate();
	command = depthPID();
	down = command * scale + neutral;

  /*Serial.print("Down: ");
  Serial.println(down);
  Serial.print("Command: ");
  Serial.println(command);
  Serial.print("Analog: ");
  Serial.println(analogRead(depthPin));*/

	//servo[0].writeMicroseconds(neutral + power);
	//servo[1].writeMicroseconds(neutral - power);
	servo[4].writeMicroseconds(neutral - down);
	servo[5].writeMicroseconds(neutral + down);
	servo[6].writeMicroseconds(neutral + down);
	servo[7].writeMicroseconds(neutral - down);
}
