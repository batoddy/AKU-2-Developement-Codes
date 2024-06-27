/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "aku_infra_barometer.h"
#include "aku_infra_imu.h"
#include "aku_infra_data.h"
#include "aku_structure.h"
#include "aku_infra_motor.h"
#include "aku_controller.h"
#include "aku_infrastructure.h"

#include "usbd_cdc_if.h"
#include "string.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */
Altitude* altitude_ptr;
IMU* imu_ptr;
ServoAngle *srv_angle_ptr;
/* USER CODE END Variables */
osThreadId Data_Read_TaskHandle;
osThreadId Led_TaskHandle;
osThreadId USB_TaskHandle;
osThreadId Servo_Control_THandle;
osThreadId Buzzer_TaskHandle;
osThreadId Data_Log_TaskHandle;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void Data_Read_Task_Entry(void const * argument);
void Led_Task_Entry(void const * argument);
void USB_Task_Entry(void const * argument);
void Servo_Control_Task_Entry(void const * argument);
void Buzzer_Task_Entry(void const * argument);
void Data_Log_Task_Entry(void const * argument);

extern void MX_USB_DEVICE_Init(void);
void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/* GetIdleTaskMemory prototype (linked to static allocation support) */
void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize );

/* USER CODE BEGIN GET_IDLE_TASK_MEMORY */
static StaticTask_t xIdleTaskTCBBuffer;
static StackType_t xIdleStack[configMINIMAL_STACK_SIZE];

void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize )
{
  *ppxIdleTaskTCBBuffer = &xIdleTaskTCBBuffer;
  *ppxIdleTaskStackBuffer = &xIdleStack[0];
  *pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;
  /* place for user code */
}
/* USER CODE END GET_IDLE_TASK_MEMORY */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* definition and creation of Data_Read_Task */
  osThreadDef(Data_Read_Task, Data_Read_Task_Entry, osPriorityHigh, 0, 512);
  Data_Read_TaskHandle = osThreadCreate(osThread(Data_Read_Task), NULL);

  /* definition and creation of Led_Task */
  osThreadDef(Led_Task, Led_Task_Entry, osPriorityLow, 0, 512);
  Led_TaskHandle = osThreadCreate(osThread(Led_Task), NULL);

  /* definition and creation of USB_Task */
  osThreadDef(USB_Task, USB_Task_Entry, osPriorityNormal, 0, 512);
  USB_TaskHandle = osThreadCreate(osThread(USB_Task), NULL);

  /* definition and creation of Servo_Control_T */
  osThreadDef(Servo_Control_T, Servo_Control_Task_Entry, osPriorityHigh, 0, 128);
  Servo_Control_THandle = osThreadCreate(osThread(Servo_Control_T), NULL);

  /* definition and creation of Buzzer_Task */
  osThreadDef(Buzzer_Task, Buzzer_Task_Entry, osPriorityIdle, 0, 128);
  Buzzer_TaskHandle = osThreadCreate(osThread(Buzzer_Task), NULL);

  /* definition and creation of Data_Log_Task */
  osThreadDef(Data_Log_Task, Data_Log_Task_Entry, osPriorityNormal, 0, 2048);
  Data_Log_TaskHandle = osThreadCreate(osThread(Data_Log_Task), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

}

/* USER CODE BEGIN Header_Data_Read_Task_Entry */
/**
  * @brief  Function implementing the Data_Read_Task thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_Data_Read_Task_Entry */
void Data_Read_Task_Entry(void const * argument)
{
  /* init code for USB_DEVICE */
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN Data_Read_Task_Entry */
  init_Barometer();
  init_IMU();
  init_Servo();
  /* Infinite loop */
  for(;;)
  {
	  imu_ptr = read_IMU();
	  altitude_ptr = read_Barometer();
	  srv_angle_ptr = servo_control(imu_ptr);
    osDelay(1);
  }
  /* USER CODE END Data_Read_Task_Entry */
}

/* USER CODE BEGIN Header_Led_Task_Entry */
/**
* @brief Function implementing the Led_Task thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Led_Task_Entry */
void Led_Task_Entry(void const * argument)
{
  /* USER CODE BEGIN Led_Task_Entry */
  /* Infinite loop */
  for(;;)
  {
	  led_blink_OK();
//	  led_blink_halted();
    osDelay(1);
  }
  /* USER CODE END Led_Task_Entry */
}

/* USER CODE BEGIN Header_USB_Task_Entry */
/**
* @brief Function implementing the USB_Task thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_USB_Task_Entry */
void USB_Task_Entry(void const * argument)
{
  /* USER CODE BEGIN USB_Task_Entry */

  /* Infinite loop */
  for(;;)
  {
	get_data(imu_ptr, altitude_ptr, srv_angle_ptr);

	transmit_usb_data_eulerNservo();

    osDelay(1);
  }
  /* USER CODE END USB_Task_Entry */
}

/* USER CODE BEGIN Header_Servo_Control_Task_Entry */
/**
* @brief Function implementing the Servo_Control_T thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Servo_Control_Task_Entry */
void Servo_Control_Task_Entry(void const * argument)
{
  /* USER CODE BEGIN Servo_Control_Task_Entry */
	init_Servo();
  /* Infinite loop */
  for(;;)
  {

	srv_angle_ptr = servo_control(imu_ptr);
    osDelay(1);
  }
  /* USER CODE END Servo_Control_Task_Entry */
}

/* USER CODE BEGIN Header_Buzzer_Task_Entry */
/**
* @brief Function implementing the Buzzer_Task thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Buzzer_Task_Entry */
void Buzzer_Task_Entry(void const * argument)
{
  /* USER CODE BEGIN Buzzer_Task_Entry */
  /* Infinite loop */
  for(;;)
  {
	  //buzzer_OK();
    osDelay(1);
  }
  /* USER CODE END Buzzer_Task_Entry */
}

/* USER CODE BEGIN Header_Data_Log_Task_Entry */
/**
* @brief Function implementing the Data_Log_Task thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Data_Log_Task_Entry */
void Data_Log_Task_Entry(void const * argument)
{
  /* USER CODE BEGIN Data_Log_Task_Entry */

	init_SD();
  /* Infinite loop */
  for(;;)
  {
	  write_SD();
    osDelay(1);
  }
  /* USER CODE END Data_Log_Task_Entry */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */
