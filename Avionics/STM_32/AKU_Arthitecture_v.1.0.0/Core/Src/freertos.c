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
#include "aku_config.h"
#include "aku_infra_imu.h"
#include "aku_infra_barometer.h"
#include "aku_structure.h"
#include "aku_infrastructure.h"
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
IMU* imu_ptr;
Altitude* altitude_ptr;

IMU* imu_ptr1;
Altitude* altitude_ptr1;
/* USER CODE END Variables */
osThreadId Read_SensorDataHandle;
osThreadId Flight_StatesHandle;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void Read_Sensor_Data_Task(void const * argument);
void Flight_States_Task(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/* GetIdleTaskMemory prototype (linked to static allocation support) */
void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize );

/* Hook prototypes */
void vApplicationStackOverflowHook(xTaskHandle xTask, signed char *pcTaskName);

/* USER CODE BEGIN 4 */
__weak void vApplicationStackOverflowHook(xTaskHandle xTask, signed char *pcTaskName)
{
   /* Run time stack overflow checking is performed if
   configCHECK_FOR_STACK_OVERFLOW is defined to 1 or 2. This hook function is
   called if a stack overflow is detected. */
}
/* USER CODE END 4 */

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
  /* definition and creation of Read_SensorData */
  osThreadDef(Read_SensorData, Read_Sensor_Data_Task, osPriorityHigh, 0, 1024);
  Read_SensorDataHandle = osThreadCreate(osThread(Read_SensorData), NULL);

  /* definition and creation of Flight_States */
  osThreadDef(Flight_States, Flight_States_Task, osPriorityHigh, 0, 1024);
  Flight_StatesHandle = osThreadCreate(osThread(Flight_States), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

}

/* USER CODE BEGIN Header_Read_Sensor_Data_Task */
/**
  * @brief  Function implementing the Read_SensorData thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_Read_Sensor_Data_Task */
void Read_Sensor_Data_Task(void const * argument)
{
  /* USER CODE BEGIN Read_Sensor_Data_Task */
	timer_init();
	init_IMU();
	init_Barometer();

  /* Infinite loop */
  for(;;)
  {
		altitude_ptr = read_Barometer();
		imu_ptr = read_IMU();
    osDelay(1);
  }
  /* USER CODE END Read_Sensor_Data_Task */
}

/* USER CODE BEGIN Header_Flight_States_Task */
/**
* @brief Function implementing the Flight_States thread.
* @param argument: Not used
* @retval None
*/
int a;
uint32_t tick;
/* USER CODE END Header_Flight_States_Task */
void Flight_States_Task(void const * argument)
{
  /* USER CODE BEGIN Flight_States_Task */

  /* Infinite loop */
  for(;;)
  {

    osDelay(1);
  }
  /* USER CODE END Flight_States_Task */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */
