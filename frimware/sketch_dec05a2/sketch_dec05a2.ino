unsigned long optic_micros = -1;
unsigned long audio_micros = -1;
signed long _delay;
int audio_interrupt_pin = 2;
int optic_interrupt_pin = 3;
bool audio_captured = false;
bool optic_captured = false;

#define MAX_VALID_TIME 400000000

void setup() {
  attachInterrupt(digitalPinToInterrupt(audio_interrupt_pin), audio_capture, FALLING);
  attachInterrupt(digitalPinToInterrupt(optic_interrupt_pin), optic_capture, RISING);
  Serial.begin(115200);
  Serial.println("Device is ready ...");
}

int state = 0;

void loop() {
  if(micros() > MAX_VALID_TIME){
    Serial.println("Please reset the device...");
    while(1){}
  }
  if (audio_captured && optic_captured){
    Serial.print("Measured delay: ");
    if(audio_micros > optic_micros){
      _delay = audio_micros - optic_micros;
    }
    else{
      _delay = (optic_micros - audio_micros) * -1;
    }
    Serial.println(_delay);
    Serial.println("For a new test please reset device");
    while(1){}
  }
  
}

void audio_capture(){
  if (!audio_captured){
    audio_captured = false;
    audio_micros = micros();
    Serial.print("Audio Detected: ");
    Serial.println(audio_micros);  
  }
//  elapsed = millis() - previous;
//  Serial.println("Audio Detected...");
////  Serial.println(elapsed);
//  previous = millis();
}

void optic_capture(){
  if (!optic_captured){
    optic_captured = false;
    optic_micros = micros();
    Serial.print("optic Detected: ");
    Serial.println(optic_micros);
  }
  
}
