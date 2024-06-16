/*
 * aku_infra_flash_mem.c
 *
 *  Created on: 10 Feb 2024
 *      Author: Batuhan
 */

#include "aku_infra_flash_mem.h"
#include "spi.h"
#include "aku_config.h"
#include "aku_infrastructure.h"

// |||||||||||||||||| NOT READY TO USE ||||||||||||||||||
// |||||||||||||||||| NOT READY TO USE ||||||||||||||||||
// |||||||||||||||||| NOT READY TO USE ||||||||||||||||||
// |||||||||||||||||| NOT READY TO USE ||||||||||||||||||

#define SPI2_CS_Pin GPIO_PIN_12
#define SPI2_CS_GPIO_Port GPIOB

#define csLOW() HAL_GPIO_WritePin(SPI2_CS_GPIO_Port, SPI2_CS_Pin, GPIO_PIN_RESET);
#define csHIGH() HAL_GPIO_WritePin(SPI2_CS_GPIO_Port, SPI2_CS_Pin, GPIO_PIN_SET);

#define W25Q_SPI hspi2

void spi_write(uint8_t* data, uint8_t len){
	HAL_SPI_Transmit(&W25Q_SPI,data,len,2000);
}

void spi_read(uint8_t* data, uint8_t len){
	HAL_SPI_Receive(&W25Q_SPI,data,len,5000);
}

void W25Q_Reset ()
{
	uint8_t	t_data[2];
	t_data[0] = 0x66;
	t_data[1] = 0x99;

	csLOW();
	spi_write(t_data,2);
	csHIGH();
	aku_delay(50);
}

uint32_t read_W25Q_ID(){
	uint8_t t_data = 0x9f;
	uint8_t r_data[3];
	uint32_t id;

	csLOW();
	spi_write(&t_data,1);
	spi_read(r_data,3);
	csHIGH();

	id = (r_data[0] << 16) | (r_data[1] << 8)| (r_data[2]);
	return id;
}


