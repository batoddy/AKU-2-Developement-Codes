/*
 * aku_infrastructure.c
 *
 *  Created on: Feb 1, 2024
 *      Author: Batuhan
 */
#include "aku_config.h"
#include "aku_infrastructure.h"
#include "main.h"
#include "cmsis_os.h"



void aku_delay(uint32_t delay){
	/*__HAL_TIM_SET_COUNTER(DELAY_TIMER,0);
	while(__HAL_TIM_GET_COUNTER(DELAY_TIMER) < (delay*10)){
		0 == 0;
	}*/
	if(USE_FREERTOS)
		osDelay(delay);
	else
		HAL_Delay(delay);
}

uint16_t aku_chronometer(uint32_t *tick){ // gets tick as a parameter and returns Delta
	uint16_t timer = HAL_GetTick() - *tick;
	*tick = HAL_GetTick();
	return timer;
}

void led_blink_OK(){
	HAL_GPIO_WritePin(LED1_PORT, LED1_PIN, GPIO_PIN_SET);
	aku_delay(1000);
	HAL_GPIO_WritePin(LED1_PORT, LED1_PIN, GPIO_PIN_RESET);
	aku_delay(1000);
}

void led_blink_halted(){
	HAL_GPIO_WritePin(LED2_PORT, LED2_PIN, GPIO_PIN_SET);
	aku_delay(100);
	HAL_GPIO_WritePin(LED2_PORT, LED2_PIN, GPIO_PIN_RESET);
	aku_delay(100);
}

void buzzer_OK(){
	HAL_GPIO_WritePin(BUZZER_PORT, BUZZER_PIN, GPIO_PIN_SET);
	aku_delay(300);
	HAL_GPIO_WritePin(BUZZER_PORT, BUZZER_PIN, GPIO_PIN_RESET);
	aku_delay(700);
}
