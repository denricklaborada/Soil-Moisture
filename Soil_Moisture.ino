#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <Thread.h>

byte mac[] = { 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0x30 };
IPAddress ip(10, 200, 180, 30);
IPAddress server(10, 200, 180, 3);

int moistureSensor = A0;
int pumpMotor = 9;
int min = 430;
int max = 720;
int sensorVal;
float percentage;
Thread publishThread = Thread();
Thread sensorThread = Thread();

EthernetClient ethClient;
PubSubClient client(ethClient);

void checkMoisture() {
  sensorVal = analogRead(A0);
  percentage = map(sensorVal, max, 0, 0, min);
  
  if (percentage < 0.0) {
    percentage = 0.0;
  }
  if (percentage > 100.0) {
    percentage = 100.0;
  }
  
  Serial.print("Moisture: ");
  Serial.print(percentage);
  Serial.println("%");
  
  if (percentage < 20.0) {
    digitalWrite(pumpMotor, HIGH);
  } else {
    digitalWrite(pumpMotor, LOW);
  }
}

void publishMsg() {
  if (client.connect("arduinoClient")) {
    char buf[8];
    dtostrf(percentage, 1, 1, buf);
    client.publish("Node/2", buf);
  }
  delay(5000);
}

void setup() {
  pinMode(moistureSensor, INPUT);
  pinMode(pumpMotor, OUTPUT);
  Serial.begin(9600);
  client.setClient(ethClient);
  client.setServer(server, 1883);
  Ethernet.begin(mac, ip);
}

void loop() {
  checkMoisture();
  publishMsg();
}
