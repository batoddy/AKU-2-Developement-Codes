#include <WiFi.h>
#include <esp_now.h>

#define CHANNEL 1

esp_now_peer_info_t device;
esp_now_peer_info_t peerInfo;

//uint8_t* reciever_Addr;
uint8_t reciever_Addr[] = {0x70,0xB8,0xF6,0x3E,0x3A,0x68 }; //0x34,0x94,0x54,0xD5,0x7F,0x9C
int latency = millis();

uint8_t recieved_data[100];

void data_recieve_callback(const uint8_t *mac_addr, const uint8_t *incomingData, int len);

void data_send_callback(const uint8_t *mac_addr, esp_now_send_status_t status){
  Serial.print("Packet Send Status: "); Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
  
}
/*void data_recieve_callback(const uint8_t *mac_addr, const uint8_t *incomingData, int len){
  /*for (int i = 0;i<=len,i++){
     revieved_data[i] = incomingData[i];
  }*//*
  Serial.print("Recieved data: ");
  Serial.println((char*) incomingData);
  Serial.println("\n Latency :");
  Serial.println(millis() - latency);
  latency = millis();
/*
}*/


void wifi_init(uint8_t* addr){
  WiFi.mode(WIFI_STA);

  WiFi.disconnect();
  
  if(esp_now_init()==ESP_OK)
    Serial.println("ESPNow Init Sucess!");
  else{
    Serial.println("ESPNow Init Fail!");
    ESP.restart();
  }
  Serial.println("SADGSDGFADSFADFASD");
  // addr = reciever_Addr;
  // Serial.println("SADGSDGFADSFADFASD");
  memcpy(peerInfo.peer_addr, reciever_Addr, 6);
  peerInfo.channel = CHANNEL;  
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
  Serial.println("before callback");
  esp_now_register_send_cb(data_send_callback);
  esp_now_register_recv_cb(data_recieve_callback);
  
}

void wifi_send_data(uint8_t* data, int len){
  esp_now_send(reciever_Addr,data,len);
}
