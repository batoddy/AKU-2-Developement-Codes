/*
 * aku_infra_data.c
 *
 *  Created on: Apr 27, 2024
 *      Author: Batuhan
 */

#include "aku_infra_data.h"
#include "aku_structure.h"
#include "string.h"


char fccData_str[100];

IMU *imu_data;
Altitude *altitude_data;
ServoAngle *srv_angle_data;

void get_data(IMU * imu_ptr, Altitude* altitude_ptr,ServoAngle *srv_angle_ptr){
	imu_data = imu_ptr;
	altitude_data = altitude_data;
	srv_angle_data = srv_angle_ptr;
	return;
}

#if USE_USB == 1
 // USB Code
	#include "usbd_cdc_if.h"
	char usb_data[100] = "EMPTY DATA";

	void transmit_usb_data_eulerNservo(){

		sprintf(usb_data,"Yaw:%.2f, Pitch:%.2f, Roll:%.2f T:%lu || S1:%.2f, S2:%.2f, T:%lu",imu_data->euler.yaw,imu_data->euler.pitch,imu_data->euler.roll,imu_data->dataflow_rate,srv_angle_data->srv1,srv_angle_data->srv2,imu_data->servo_delta);
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
	#include "fatfs.h"
	FATFS *FatFs;


	char path[20] = "fcc.txt";
	FRESULT fresult ;
	UINT br, bw;

	void init_SD(){
		FIL fil;
		fresult  = f_mount(FatFs, (TCHAR const *)SDPath, 1);
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
		FIL fil;
		fresult = f_open(&fil, path, FA_WRITE | FA_OPEN_ALWAYS);

		fresult = f_write(&fil, fccData_str, strlen(fccData_str), &bw);

		f_close(&fil);
	}

#endif

#if USE_FLASH == 1
 // Flash Code
#endif


