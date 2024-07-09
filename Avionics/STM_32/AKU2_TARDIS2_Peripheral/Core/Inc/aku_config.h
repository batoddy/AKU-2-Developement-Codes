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

#define USE_USB 1
#define USE_UART 0
#define USE_CAN 1
#define USE_SD 1
#define USE_FLASH 0

//------ PINS --------------------

#define BUZZER_PORT GPIOB
#define BUZZER_PIN GPIO_PIN_4

#define LED1_PORT GPIOC
#define LED1_PIN GPIO_PIN_2

#define LED2_PORT GPIOC
#define LED2_PIN GPIO_PIN_3

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

//------ Motor Defines ------

#define DC_MOTOR_MAX_THRUST 1000 // Control the value from ioc file (ARR Register value+1)
#define DC_MOTOR_MIN_THRUST 400
#define SERVO_CCW_MAX 150
#define SERVO_CW_MAX 1060

#define SERVO1_TIM htim2
#define SERVO2_TIM htim2
#define SERVO3_TIM htim2
#define SERVO4_TIM htim2

#define SERVO1_CHA TIM_CHANNEL_1
#define SERVO2_CHA TIM_CHANNEL_2
#define SERVO3_CHA TIM_CHANNEL_3
#define SERVO4_CHA TIM_CHANNEL_4

#define DC1_TIM htim12
#define DC1_CHA TIM_CHANNEL_1

#endif /* INC_AKU_CONFIG_H_ */
