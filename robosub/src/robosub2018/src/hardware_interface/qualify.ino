#include <Servo.h>

Servo servo[8];
int neutral = 1500;
int down = 1600;
int power = 1750;
int scale = 300;

int pins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
int depthPin = 0; 

//float surfacePSI = 10.44; // Check ad hoc
float surfacePSI = -1;
float psi;
float depth = 0.0;

float error = 0.0;
float dererror = 0.0;
float interror = 0.0;
float dt = 0.0;
float time;

//PID Gains
float kp = 0.5; // TODO: Tune
float ki = 0.5;;
float kd = 0.5;


float targetDepth = 1.5


void setSurfacePSI() {
	if(surfacePSI == -1) {
		sensePSI();
		surfacePSI = psi;
	}
}


void sensePSI() {
	psi = (analogRead(depthPin) * 0.0048828125 - 1) * 12.5;
}


void calcDepthUpdate() {
	sensePSI();
	time =  abs(millis() - time);
	depth = ((analogRead(depthPin) * 0.0048828125 - 1) * 12.5 - surfacePSI) * 0.13197839577;
	// compute dt
	float preverror = error;
	error = depth - target_depth;
	interror += error * dt;
	dererror = (error - temp) * dt;
}


float depthPID() {
	command = (error * kp) + (interror * dt * ki) + (dererror * kd)
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
	servo.attach(pins);
	setSurfacePSI();
	calcDepthUpdate();

	int i;
	for(i = 0; i < 8; i++) {
		servo.attach(pins[i]);
		servo[i].writeMicroseconds(neutral);
	}

	delay(1000);
	servo[4].writeMicroseconds(down);
	servo[5].writeMicroseconds(down);
	servo[6].writeMicroseconds(down);
	servo[7].writeMicroseconds(down);
	time = millis();
}

void loop() {
	calcDepthUpdate();
	command = depthPID();
	down = command * scale + neutral;

	servo[0].writeMicroseconds(power);
	servo[1].writeMicroseconds(power);
	servo[4].writeMicroseconds(down);
	servo[5].writeMicroseconds(down);
	servo[6].writeMicroseconds(down);
	servo[7].writeMicroseconds(down);
}
