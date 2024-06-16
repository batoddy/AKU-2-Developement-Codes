/*
 * aku_infra_motor.c
 *
 *  Created on: Jun 10, 2024
 *      Author: Batuhan
 */

#include "aku_infra_motor.h"
#include "tim.h"
#include "aku_config.h"

#include "FreeRTOS.h"
#include "cmsis_os.h"

//#define DC_MOTOR_MAX_THRUST 1000 // Control the value from ioc file (ARR Register value+1)
//#define DC_MOTOR_MIN_THRUST 400
//#define SERVO_CCW_MAX 150
//#define SERVO_CW_MAX 1060
//
//#define SERVO1_TIM htim2
//#define SERVO2_TIM htim2
//#define SERVO3_TIM htim2
//#define SERVO4_TIM htim2
//
//#define SERVO1_CHA TIM_CHANNEL_1
//#define SERVO2_CHA TIM_CHANNEL_2
//#define SERVO3_CHA TIM_CHANNEL_3
//#define SERVO4_CHA TIM_CHANNEL_4
//
//#define DC1_TIM htim12
//#define DC1_CHA TIM_CHANNEL_1

int pwm_counter = 0;

long map(long x, long in_min, long in_max, long out_min, long out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
//--------------------SERVO-MOTOR--------------------//

void init_Servo()
{

	HAL_TIM_PWM_Start(&SERVO1_TIM, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&SERVO2_TIM, TIM_CHANNEL_2);

	HAL_TIM_PWM_Start(&SERVO2_TIM, TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&SERVO2_TIM, TIM_CHANNEL_4);
}

void servo1_pwm(float angle)
{
	long duty = map(angle, -90, 90, SERVO_CCW_MAX, SERVO_CW_MAX);
	__HAL_TIM_SetCompare(&SERVO2_TIM, SERVO1_CHA, duty);
}

void servo2_pwm(float angle)
{
	long duty = map(angle, -90, 90, SERVO_CCW_MAX, SERVO_CW_MAX);
	__HAL_TIM_SetCompare(&SERVO2_TIM, SERVO2_CHA, duty);
}

void servo3_pwm(float angle)
{
	long duty = map(angle, -90, 90, SERVO_CCW_MAX, SERVO_CW_MAX);
	__HAL_TIM_SetCompare(&SERVO3_TIM, SERVO3_CHA, duty);
}

void servo4_pwm(float angle)
{
	long duty = map(angle, -90, 90, SERVO_CCW_MAX, SERVO_CW_MAX);
	__HAL_TIM_SetCompare(&SERVO4_TIM, SERVO4_CHA, duty);
}

void servo1_pwm_raw(uint32_t angle)
{
	//	uint32_t angle_calculated = (uint32_t)(angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE);
	//	uint32_t angle_calculated = ((uint32_t)((angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE))) + SERVO_MIN_ANGLE;
	__HAL_TIM_SetCompare(&SERVO1_TIM, SERVO1_CHA, angle);
}
void servo2_pwm_raw(uint32_t angle)
{
	//	uint32_t angle_calculated = (uint32_t)(angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE);
	//	uint32_t angle_calculated = ((uint32_t)((angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE))) + SERVO_MIN_ANGLE;
	__HAL_TIM_SetCompare(&SERVO2_TIM, SERVO2_CHA, angle);
}
void servo3_pwm_raw(uint32_t angle)
{
	//	uint32_t angle_calculated = (uint32_t)(angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE);
	//	uint32_t angle_calculated = ((uint32_t)((angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE))) + SERVO_MIN_ANGLE;
	__HAL_TIM_SetCompare(&SERVO3_TIM, SERVO4_CHA, angle);
}

void servo4_pwm_raw(uint32_t angle)
{
	//	uint32_t angle_calculated = (uint32_t)(angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE);
	//	uint32_t angle_calculated = ((uint32_t)((angle/100)*(SERVO_MAX_ANGLE - SERVO_MIN_ANGLE))) + SERVO_MIN_ANGLE;
	__HAL_TIM_SetCompare(&SERVO4_TIM, SERVO4_CHA, angle);
}

void servo_movement_control()
{
	servo1_pwm(60);
	servo2_pwm(60);
	servo3_pwm(60);
	servo4_pwm(60);

	osDelay(1000);

	servo1_pwm(0);
	servo2_pwm(0);
	servo3_pwm(0);
	servo4_pwm(0);
	osDelay(1000);

	servo1_pwm(-60);
	servo2_pwm(-60);
	servo3_pwm(-60);
	servo4_pwm(-60);
	osDelay(1000);

	servo1_pwm(0);
	servo2_pwm(0);
	servo3_pwm(0);
	servo4_pwm(0);
	osDelay(1000);



	/*servo1_angle = 0;
	servo2_angle = 0;
	servo3_angle = 0;
	servo4_angle = 0;*/
}

void servo_reset_state()
{
	servo1_pwm(0);
	servo2_pwm(0);
	servo3_pwm(0);
	servo4_pwm(0);
	osDelay(200);
}
//---------------------DC-MOTOR---------------------//

void init_DC_Motor()
{

	HAL_TIM_PWM_Start(&DC1_TIM, DC1_CHA);
//	HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);
}

void configurate_ESC()
{
	osDelay(15000);

	DC_motor_thrust(100);

	osDelay(2000);
	DC_motor_thrust(0);
	osDelay(2000);
}
long duty1;
void DC_motor_thrust(float percentage)
{
	duty1 = map(percentage, 0, 100, DC_MOTOR_MIN_THRUST, DC_MOTOR_MAX_THRUST);
	__HAL_TIM_SetCompare(&DC1_TIM, DC1_CHA, duty1);
//	__HAL_TIM_SetCompare(&htim2, TIM_CHANNEL_2, duty1);
}
void DC_motor_thrust_raw(float percentage)
{
	__HAL_TIM_SetCompare(&DC1_TIM, DC1_CHA, percentage);
//	__HAL_TIM_SetCompare(&htim2, TIM_CHANNEL_2, percentage);
}

void DC_motor_shutdown()
{
	DC_motor_thrust_raw(400);
	//thrust = 0;
}

void system_emergency_shutdown()
{
	DC_motor_thrust_raw(400);
	//thrust = 0;
	//	HAL_Delay(HAL_MAX_DELAY);
}
//
// void DC_Motor_movement_control(){
//	ESC1_power(DC_MOTOR_MAX_POWER);
//	ESC2_power(DC_MOTOR_MAX_POWER);
//
//	HAL_Delay(500);
//	ESC1_power(DC_MOTOR_MIN_POWER);
//	ESC2_power(DC_MOTOR_MIN_POWER);
//	HAL_Delay(500);
//}

// void ESC1_pwm_scan(){
//	for(pwm_counter = 0;pwm_counter > 9999;pwm_counter += 500){
//		ESC1_power(pwm_counter);
//		osDelay(5000);
//	}
//
// }


