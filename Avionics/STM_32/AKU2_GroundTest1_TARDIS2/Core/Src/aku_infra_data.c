/*
 * aku_infra_data.c
 *
 *  Created on: Apr 27, 2024
 *      Author: Batuhan
 */

#include "aku_infra_data.h"
#include "aku_structure.h"
#include "string.h"


char *fccData_str = "Hello\n";

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
	// FATFS SDFatFs_;
	//FIL SDFile;

	char path[20] = "fcc.txt";
	FRESULT fresult ;
	uint8_t wtext[] = "STM32 FATFS works great!"; /* File write buffer */
	UINT br, bw;

	void init_SD(){

		fresult  = f_mount(&SDFatFS, (TCHAR const *)SDPath, 1);
		if (fresult  != FR_OK){
			/* Mount err*/
		}
		fresult = f_open(&SDFile, "FCC.txt", FA_CREATE_ALWAYS | FA_WRITE);
		if (fresult != FR_OK){
			/* File create err*/
		}
		sprintf(fccData_str,"135");
		fresult = 10;
		fresult = f_write(&SDFile, fccData_str, strlen((char *)fccData_str), (void *)&bw);
		fresult = 10;
		fresult = f_close(&SDFile);

	}

	void write_SD(){
		fresult = f_open(&SDFile, "FCC.txt", FA_WRITE | FA_OPEN_ALWAYS);
		fresult = f_lseek(&SDFile, f_size(&SDFile));
		fresult = f_write(&SDFile, fccData_str, strlen((char *)fccData_str),  (void *)&bw);

		f_close(&SDFile);
	}

#endif

#if USE_FLASH == 1
 // Flash Code
#endif


