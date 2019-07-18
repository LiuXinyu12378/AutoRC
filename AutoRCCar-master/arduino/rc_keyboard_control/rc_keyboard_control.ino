// assign pin num
int right_pin = 6;
int left_pin = 7;
int forward_pin = 10;
int reverse_pin = 9;

// duration for output
int time = 20;
int time2 = 20;
// initial command
int command = 0;

void setup() {
  pinMode(right_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  //receive command
  if (Serial.available() > 0){
    command = Serial.read();
  }
  else{
    reset();
  }
   send_command(command,time);
}

void right(int time){
  digitalWrite(13, HIGH);
  digitalWrite(right_pin, HIGH);
  delay(time);
}

void left(int time){
  digitalWrite(13, HIGH);
  digitalWrite(left_pin, HIGH);
  delay(time);
}

void forward(int time){
  digitalWrite(13, HIGH);
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, HIGH);
  delay(time);
  digitalWrite(forward_pin, LOW);
  delay(time2);
}

void reverse(int time){
  digitalWrite(13, HIGH);
  digitalWrite(reverse_pin, HIGH);
  delay(time);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void forward_right(int time){
  digitalWrite(13, HIGH);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(right_pin, HIGH);
  delay(time);
  digitalWrite(forward_pin, LOW);
  delay(time2);
}

void reverse_right(int time){
  digitalWrite(13, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(right_pin, HIGH);
  delay(time);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void forward_left(int time){
  digitalWrite(13, HIGH);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  delay(time);
  digitalWrite(forward_pin, LOW);
  delay(time2);
}

void reverse_left(int time){
  digitalWrite(13, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  delay(time);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void reset(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, LOW);
  digitalWrite(13, LOW);
}

void send_command(int command, int time){
  switch (command){

     //reset command
     case 48: reset(); break;

     // single command
     case 49: forward(time); break;
     case 50: reverse(time); break;
     case 51: right(time); break;
     case 52: left(time); break;

     //combination command
     case 54: forward_right(time); break;
     case 55: forward_left(time); break;
     case 56: reverse_right(time); break;
     case 57: reverse_left(time); break;

//     default: Serial.print("Inalid Command\n");
    }
}
