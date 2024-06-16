#include "aku_fullduplex_wifi_telemetry.h"


uint8_t reciever_address[1];// = {0xA8,0x42,0xE3,0x90,0x81,0xE4}; //0x70,0xB8,0xF6,0x3E,0x3A,0x68 
// 0xA8,0x42,0xE3,0x90,0x81,0xE4
uint8_t tData[100];
uint8_t rData[100];
int index_1 = 0;

void data_recieve_callback(const uint8_t *mac_addr, const uint8_t *incomingData, int len){
  /*for (int i = 0;i<=len,i++){
     revieved_data[i] = incomingData[i];
  }*/
  memcpy(rData,incomingData,len);
  Serial.print("Recieved data: ");
  Serial.println(*rData);
  Serial.println("\n Latency :");
  Serial.println(millis() - latency);
  latency = millis();
}  
void setup() {
  Serial.begin(115200); ç
  Serial.println("CODE STARTED!!!");
  wifi_init(reciever_address); 0möjçk.l 

}

void loop() {
  index_1++;
  memcpy(tData,&index_1,sizeof(index_1)+1);
  //Serial.println("CODE LOOPIN!!!");
  wifi_send_data(tData,200);
  Serial.print("Index:");
  Serial.println(*rData);
  Serial.println();
  delay(5);
}
