/*
 * aku_infrastructure.h
 *
 *  Created on: Feb 1, 2024
 *      Author: Batuhan
 */

#ifndef INC_AKU_INFRASTRUCTURE_H_
#define INC_AKU_INFRASTRUCTURE_H_

#include "stdio.h"

void timer_init();
void aku_delay(uint32_t delay);
uint16_t aku_chronometer(uint32_t *tick);

void led_blink_OK();
void buzzer_OK();
void led_blink_halted();

#endif /* INC_AKU_INFRASTRUCTURE_H_ */
