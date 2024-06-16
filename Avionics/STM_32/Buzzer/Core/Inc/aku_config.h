/*
 * aku_config.h
 *
 *  Created on: Jan 30, 2024
 *      Author: Batuhan
 */

#ifndef INC_AKU_CONFIG_H_
#define INC_AKU_CONFIG_H_


#include "i2c.h"

#define SYSTEM_TIMER &htim1


#define USE_FREERTOS 1

#define USE_USB 0
#define USE_UART 0
#define USE_CAN 0
#define USE_SD 1
#define USE_FLASH 0


//------ IMU Device Defines ------

#define IMU_I2C &hi2c3
#define IMU_ADDR 0x28
#define IMU_CHIP_ID 0xA0
#define IMU_CHIP_ID_ADDR 0x00
#define IMU_OFFSET_VAL 250
#define IMU_EMPTY_REG_VAL 250
#define SET_OFFSET 0 // 1 for offsetting, 0 for not-offsetting
#define SYS_STATUS_REG 0x39
#define SYS_ERR_REG 0x3A

//------ BAROMETER Device Defines ------

#define BARO_I2C &hi2c1
#define BARO_ADDR 0x77
#define BARO_OSR 2
#define BARO_OFFSET_VAL 250
#define BARO_EMPTY_REG_VAL 50

#endif /* INC_AKU_CONFIG_H_ */
