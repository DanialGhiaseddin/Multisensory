unsigned long optic_micros = -1;
unsigned long audio_micros = -1;
signed long _delay;
int audio_interrupt_pin = 2;
int optic_interrupt_pin = 3;
bool audio_captured = false;
bool optic_captured = false;
bool displayed_capture = false;

String a;
int incomingByte = 0;

#define MAX_VALID_TIME 4293918720
#define NOISE_REJECTION 3000000


void setup() {
  Serial.begin(115200);
  Serial.println("Device is ready ...");
  int mode_flag = -1;
  while(mode_flag == -1){
    if (Serial.available() > 0) {
      a = Serial.readString();
      int command = a.toInt();
      if(command == 0){
        mode_flag = 0;
        attachInterrupt(digitalPinToInterrupt(audio_interrupt_pin), audio_capture, FALLING);
        attachInterrupt(digitalPinToInterrupt(optic_interrupt_pin), optic_capture, RISING);
        Serial.println("Operational Mode");
      }
      else if(command == 1){
        mode_flag = 1;
        attachInterrupt(digitalPinToInterrupt(audio_interrupt_pin), audio_capture_debug, FALLING);
        attachInterrupt(digitalPinToInterrupt(optic_interrupt_pin), optic_capture_debug, RISING);
        Serial.println("Debug Mode");
      }
    }
  }
}

int state = 0;

void loop() {
  if(micros() > MAX_VALID_TIME){
    Serial.println("Please reset the device...");
    while(1){}
  }
  if (audio_captured && optic_captured){
    if(!displayed_capture){
      Serial.print("Measured delay: ");
      if(audio_micros > optic_micros){
        _delay = audio_micros - optic_micros;
      }
      else{
        _delay = (optic_micros - audio_micros) * -1;
      }
      Serial.println(_delay);
      displayed_capture = true;
    }
//    Serial.println("For a new test please reset device");
    if(micros() > NOISE_REJECTION + audio_micros){
       audio_captured = false;
       optic_captured = false;
       displayed_capture = false;
    }
  }
  
}

void audio_capture(){
  if (!audio_captured){
    audio_captured = true;
    audio_micros = micros(); 
  }
}

void optic_capture(){
  if (!optic_captured){
    optic_captured = true;
    optic_micros = micros();
  }  
}

void audio_capture_debug(){
  if (!audio_captured){
    audio_captured = false;
    audio_micros = micros();
    Serial.print("Audio Detected: ");
    Serial.println(audio_micros);  
  }
}

void optic_capture_debug(){
  if (!optic_captured){
    optic_captured = false;
    optic_micros = micros();
    Serial.print("optic Detected: ");
    Serial.println(optic_micros);
  }
}
