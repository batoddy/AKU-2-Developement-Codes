/*
 * aku_infra_SD.c
 *
 *  Created on: Feb 8, 2024
 *      Author: Batuhan
 */
/*
#include "aku_infra_SD.h"
#include "fatfs.h"
#include "string.h"
#include "stdio.h"
#include "ff.h"*/
// |||||||||||||||||| NOT TESTED ||||||||||||||||||
// |||||||||||||||||| NOT TESTED ||||||||||||||||||
// |||||||||||||||||| NOT TESTED ||||||||||||||||||
// |||||||||||||||||| UNDER DEVELOPEMENT ||||||||||||||||||

//FRESULT res; /* FatFs function common result code */
//uint32_t byteswritten, bytesread; /* File write/read counts */
//uint8_t wtext[] = "STM32 FATFS works great!"; /* File write buffer */
//uint8_t rtext[_MAX_SS];/* File read buffer */
/*
FILINFO fno;
char path[100] = "/TARDIS_2/data.txt";

void init_SD(){
	if(f_mount(&SDFatFS, (TCHAR const*)SDPath, 0) != FR_OK)
	{
		Error_Handler();
	}
	else{
		if(f_mount(&SDFatFS, "/", 0) != FR_OK){
			f_mkdir("/TARDIS_2");
			}

		uint16_t i;
		while(f_open(&SDFile,path,FA_CREATE_NEW | FA_WRITE) == FR_EXIST){
			i++;
			sprintf(path,"/TARDIS_2/data%d.txt",i);
		}
		res = f_write(&SDFile, wtext, strlen((char *)wtext), (void *)&byteswritten);
						if((byteswritten == 0) || (res != FR_OK))
						{
							Error_Handler();
						}
						else
						{
							f_close(&SDFile);
						}
	}
}
void write_to_SD(char *data){
	res = f_open(&SDFile,path,FA_OPEN_APPEND | FA_WRITE);
	res = f_write(&SDFile,data,strlen(data),(void *)&byteswritten);
}

void read_from_SD(char *data){
	res = f_open(&SDFile,path,FA_READ);
	res = f_read(&SDFile,data,f_size(&SDFile),(void *)&byteswritten);
	res = f_close(&SDFile);
}*/
