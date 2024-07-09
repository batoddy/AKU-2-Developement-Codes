/*
 * aku_infra_data.c
 *
 *  Created on: Apr 27, 2024
 *      Author: Batuhan
 */

#include "aku_infra_data.h"
#include "aku_structure.h"
#include "string.h"




IMU *imu_data_ptr;
Altitude *altitude_data_ptr;
ServoAngle *srv_angle_data_ptr;

void get_data(IMU * imu_ptr, Altitude* altitude_ptr,ServoAngle *srv_angle_ptr){
	imu_data_ptr = imu_ptr;
	altitude_data_ptr = altitude_ptr;
	srv_angle_data_ptr = srv_angle_ptr;
	return;
}

#if USE_USB == 1
 // USB Code
	#include "usbd_cdc_if.h"
	char usb_data[100] = "EMPTY DATA";

	void transmit_usb_data_eulerNservo(){

		sprintf(usb_data,"Yaw:%.2f, Pitch:%.2f, Roll:%.2f T:%lu || S1:%.2f, S2:%.2f, T:%lu",imu_data_ptr->euler.yaw,imu_data_ptr->euler.pitch,imu_data_ptr->euler.roll,imu_data_ptr->dataflow_rate,srv_angle_data_ptr->srv1,srv_angle_data_ptr->srv2,imu_data_ptr->servo_delta);
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

	char fccSD_str [200] = "DATA ERR!!!";
	FRESULT fresult ;
	uint8_t sd_init_txt[200]; /* File write buffer */
	UINT br, bw;

	void init_SD(){

		fresult  = f_mount(&SDFatFS, (TCHAR const *)SDPath, 1);
		if (fresult  != FR_OK){
			/* Mount err*/
		}
		fresult = f_open(&SDFile, "FCC.csv", FA_CREATE_NEW | FA_WRITE);
		if (fresult != FR_OK){
			/* File create err*/
		}
		sprintf(sd_init_txt,"IMU_timestamp,AccelX,AccelY,AccelZ,AccelRes,GyroX,GyroY,GyroZ,Yaw,Pitch,Roll,imuDataflow,Srv1Angle,Srv2Angle,SrvControlRate\n");

		fresult = f_write(&SDFile, sd_init_txt, strlen((char *)sd_init_txt), (void *)&bw);

		fresult = f_close(&SDFile);

	}

	void write_SD(){
		sprintf(fccSD_str,"%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%lu,%f,%f,%lu\n",imu_data_ptr->prev_tick,imu_data_ptr->accel.x,imu_data_ptr->accel.y,imu_data_ptr->accel.z,imu_data_ptr->accel.resultant,imu_data_ptr->gyro.x,imu_data_ptr->gyro.y,imu_data_ptr->gyro.z,imu_data_ptr->euler.yaw,imu_data_ptr->euler.pitch,imu_data_ptr->euler.roll,imu_data_ptr->dataflow_rate,srv_angle_data_ptr->srv1,srv_angle_data_ptr->srv2,srv_angle_data_ptr->control_rate);

		fresult = f_open(&SDFile, "FCC.csv", FA_OPEN_EXISTING | FA_WRITE);
		fresult = f_lseek(&SDFile, f_size(&SDFile));
		fresult = f_write(&SDFile, fccSD_str, strlen((char *)fccSD_str),  (void *)&bw);

		f_close(&SDFile);
	}

#endif

#if USE_FLASH == 1
 // Flash Code
#endif


