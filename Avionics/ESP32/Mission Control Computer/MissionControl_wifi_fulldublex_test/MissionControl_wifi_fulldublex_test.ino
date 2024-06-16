#include "aku_fullduplex_wifi_mcu.h"


uint8_t reciever_address[1];// = {0x70,0xB8,0xF6,0x3E,0x3A,0x68 }; //0x34,0x94,0x54,0xD5,0x7F,0x9C
uint8_t tData[100];
uint8_t rData[100];
int index_1 = 0;
int data_1;
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
  Serial.begin(115200); 
  Serial.println("CODE STARTED!!!");
  wifi_init(reciever_address);

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
