/*
 * aku_infra_data.c
 *
 *  Created on: Apr 27, 2024
 *      Author: Batuhan
 */

#include "aku_infra_data.h"
#include "string.h"

char fccData_str[100];

void get_data(){
	return;
}

#if USE_USB == 1
 // USB Code
	#include "usbd_cdc_if.h"

	void transmit_usb_data(){
		char* usb_data = "EMPTY DATA";
		CDC_Transmit_FS(usb_data, strlen(usb_data));
	}
#endif

#if USE_UART == 1
 // UART Code

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
	#include "ff.h"

	FATFS FatFs;

	FIL fil;
	char path[100] = "FCC.txt";
	FRESULT fresult ;
	UINT br, bw;

	void init_SD(){

		fresult  = f_mount(&FatFs, "", 1);
		if (fresult  != FR_OK){
			/* Mount err*/
		}
		fresult = f_open(&fil, path, FA_WRITE | FA_OPEN_ALWAYS);
		if (fresult != FR_OK){
			/* File create err*/
		}
		f_close(&fil);
	}

	void write_SD(){
		fresult = f_open(&fil, path, FA_WRITE | FA_OPEN_ALWAYS);

		fresult = f_write(&fil, fccData_str, strlen(fccData_str), &bw);

		f_close(&fil);
	}

#endif

#if USE_FLASH == 1
 // Flash Code
#endif


