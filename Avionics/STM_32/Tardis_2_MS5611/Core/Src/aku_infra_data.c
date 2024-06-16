/*
 * aku_infra_data.c
 *
 *  Created on: Apr 27, 2024
 *      Author: Batuhan
 */

// #include "usbd_cdc_if.h"
#include "string.h"

void get_data(){
	return;
}

#if USE_USB == 1
 // USB Code
	void transmit_usb_data(){
		char* usb_data = "EMPTY DATA";
		CDC_Transmit_FS(usb_data, strlen(usb_data));
	}
#endif

#if USE_UART == 1
 // UART Code
	void transmit_usb_data(){
			char* usb_data = "EMPTY DATA";
			CDC_Transmit_FS(usb_data, strlen(usb_data));
		}
#endif

#if USE_CAN == 1
 // CAN Code
	void init_CAN(){
		return;
	}

	void activate_CAN(){
		return;
	}
#endif

#if USE_SD == 1
 //SD Code
#endif

#if USE_FLASH == 1
 // Flash Code
#endif


