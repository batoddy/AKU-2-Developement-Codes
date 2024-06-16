#include <CAN.h>

#define CAN_BITRATE 100E3
#define CAN_RX 0
#define CAN_TX 4

typedef struct CAN_Header{
  long id;
  int DLC;
  bool RTR;
}CAN_Header;

CAN_Header txHeader;
CAN_Header rxHeader;

uint8_t txData[8] = "Hi AKU";
uint8_t rxData[8];

void setup() {
  Serial.begin(115200);
  CAN.begin(CAN_BITRATE);  
  CAN.setPins(CAN_RX,CAN_TX);
  
  //CAN.loopback();
  
  CAN.end();

  txHeader.id = 0x446;
  txHeader.DLC = 8;
  txHeader.RTR = false;
  CAN.onReceive(onReceive);
}

void loop() {
  
  CAN.beginPacket(txHeader.id, txHeader.DLC, txHeader.RTR);
  CAN.write(txData, 8);
  CAN.endPacket();
  delay(1000);
}

void onReceive(int packetSize){
  rxHeader.id = CAN.packetId();
  rxHeader.DLC = CAN.packetDlc();
  rxHeader.RTR = CAN.packetRtr();

  Serial.println(rxHeader.id,HEX);
  Serial.println(rxHeader.DLC);
  Serial.println(rxHeader.RTR);
  
  while(CAN.available() != -1){
    rxData[CAN.available()] = CAN.read();
    Serial.println((char*)rxData[CAN.available()]);
  }
}
