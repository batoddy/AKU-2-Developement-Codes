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
/* USER CODE END Variables */
osThreadId defaultTaskHandle;
osThreadId Task1Handle;
osThreadId USB_TaskHandle;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void StartDefaultTask(void const * argument);
void StartTask1(void const * argument);
void StartTask03(void const * argument);

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
  /* definition and creation of defaultTask */
  osThreadDef(defaultTask, StartDefaultTask, osPriorityNormal, 0, 512);
  defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

  /* definition and creation of Task1 */
  osThreadDef(Task1, StartTask1, osPriorityHigh, 0, 512);
  Task1Handle = osThreadCreate(osThread(Task1), NULL);

  /* definition and creation of USB_Task */
  osThreadDef(USB_Task, StartTask03, osPriorityIdle, 0, 512);
  USB_TaskHandle = osThreadCreate(osThread(USB_Task), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

}

/* USER CODE BEGIN Header_StartDefaultTask */
/**
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void const * argument)
{
  /* init code for USB_DEVICE */
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN StartDefaultTask */
  init_Barometer();
  init_IMU();
  /* Infinite loop */
  for(;;)
  {
	  /*HAL_GPIO_WritePin(BNO_RST_GPIO_Port, BNO_RST_Pin, GPIO_PIN_RESET);
	  // osDelay(20);
	  // HAL_GPIO_WritePin(BNO_RST_GPIO_Port, BNO_RST_Pin, GPIO_PIN_SET);
	  // osDelay(20);*/
	  imu_ptr = read_IMU();
	  altitude_ptr = read_Barometer();
    osDelay(1);
  }
  /* USER CODE END StartDefaultTask */
}

/* USER CODE BEGIN Header_StartTask1 */
/**
* @brief Function implementing the Task1 thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTask1 */
void StartTask1(void const * argument)
{
  /* USER CODE BEGIN StartTask1 */
  /* Infinite loop */
  for(;;)
  {
	  //HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4, GPIO_PIN_SET);
	  	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_3, GPIO_PIN_SET);
	  	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_2, GPIO_PIN_RESET);
	  	  osDelay(500);
	  	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_2, GPIO_PIN_SET);
	  	  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_3, GPIO_PIN_RESET);
	  	  osDelay(500);
    osDelay(1);
  }
  /* USER CODE END StartTask1 */
}

/* USER CODE BEGIN Header_StartTask03 */
/**
* @brief Function implementing the USB_Task thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTask03 */
void StartTask03(void const * argument)
{
  /* USER CODE BEGIN StartTask03 */
	char* usb_data = "Hello World!!!";
	//init_SD();
  /* Infinite loop */
  for(;;)
  {
	  CDC_Transmit_FS(usb_data, strlen(usb_data));
	 // write_SD();
    osDelay(100);
  }
  /* USER CODE END StartTask03 */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */
