/*
 * aku_structure.h
 *
 *  Created on: Jan 30, 2024
 *      Author: Batuhan
 */

#ifndef INC_AKU_STRUCTURE_H_
#define INC_AKU_STRUCTURE_H_

#include "i2c.h"

/*----------MAIN-STRUCTURES----------*/
typedef struct Time
{
  uint32_t current;
  int prevTime;
  int liftoff;
  int apogee;
  int timeDifference;
  int container_seperation;
  int flight_time;
  int flight_time_offset;
  int landing;
} Time;

enum FlightStates
{
  START,
  AFTER_LIFTOFF,
  AFTER_BURNOUT,
  // AFTER_APOGEE,
  // Seperation????
  FREEFALL_STAGE,
  CONTROLLED_FLIGHT,
  TOUCHDOWN,
  LOST_OF_CONTROL_STAGE
};

enum Errors
{
  OK,
  ROCKET_SEPERATION_ERR,
  CONTAINER_SEPERATION_ERR,
  SPIN_ERR,
  BAROMETER_ERR,
  IMU_ERR
};
enum StabilizationFlag
{
  STABLE,
  UNSTABLE,
  CONTROL_LOST
};

typedef union
{
  float u32;
  char u8[4];
} float_to_u8;

typedef union
{
  int16_t u16;
  char u8[2];
} u16_to_u8;


/*----------DEVICE-STRUCTURES----------*/
typedef struct IMU_Device
{
  I2C_HandleTypeDef* i2c;
  uint8_t addr;
  uint8_t chip_id;
  uint8_t chip_id_reg;
  uint8_t set_offset;
  uint16_t offset_val;
  uint16_t empty_reg_val;
  uint8_t sys_status;
  uint8_t sys_err;
} IMU_Device;

typedef struct Barometer_Device
{
  I2C_HandleTypeDef* i2c;
  uint8_t addr;
  uint8_t chip_id;
  uint8_t chip_id_reg;
  uint16_t empty_reg_val;
  uint16_t base_press_caliber_val;
  uint8_t sys_status;
  uint8_t sys_err;
  uint8_t osr;
} Barometer_Device;

enum Device_Satate{
	DEV_ERR,
	DEV_OK
};

/*----------BAROMETER-STRUCTURES----------*/
typedef struct Barometer_Data
{
  float pressure;
  float base_pressure;
  float temperature;
  float altitude;
  float max_altitude;
  float diff_to_max;

  float time_diff;
  float vertical_velocity;

  float prev_time;
  float max_velocity_rocket;
  float max_velocity_payload;
  int8_t max_velocity_rocket_mach;
  int8_t max_velocity_payload_mach;
  float velocity_changing; // 1 increase | 0 decerase
} Barometer_Data;

typedef struct Altitude
{
  float pressure;
  float base_pressure;
  float temperature;;
  float altitude;
  float prev_altitude;
  float max_altitude;
  float diff_to_max;
  float vertical_velocity;
  float prev_vertical_velocity;
  float vertical_accel;


  uint32_t dataflow_rate;
  uint32_t prev_tick;
  uint32_t tick;

} Altitude;

typedef struct Velocity
{
  float time_diff;
  float vertical_velocity;

  float prev_time;
  float max_velocity_rocket;
  float max_velocity_payload;
  int8_t max_velocity_rocket_mach;
  int8_t max_velocity_payload_mach;
  float velocity_changing; // 1 increase | 0 decerase
} Velocity;

enum barometer_state
{
  TEMPERATURE_CALLBACK = 0,
  PRESSURE_CALLBACK

};

/*----------IMU-STRUCTURES----------*/

typedef struct Vector
{
  float x;
  float y;
  float z;
  float resultant;
} Vector;

typedef struct Euler
{
  float yaw;
  float roll;
  float pitch;
} Euler;

typedef struct IMU
{
 Vector accel;
  Vector gyro;
  Vector magno;
  Euler euler;

  Vector lineer_accel;
  Vector accel_G;
  uint32_t dataflow_rate1;
  uint8_t data_flow_flag;
  uint8_t dev_status;
  float z_velocity;
  float z_displacement;
  float prev_z_velocity;
  Vector prev_accel;

  uint32_t dataflow_rate;
  uint32_t servo_delta;
  uint32_t tick;
  uint32_t prev_tick;
} IMU;

typedef struct ServoAngle
{
  float srv1;
  float srv2;
  uint32_t tick;
  uint32_t control_rate;
} ServoAngle;

/*----------DATA-STRUCTURES----------*/

typedef struct Data_Struct
{
  float accel_x;
  float accel_y;
  float accel_z;
  float yaw;
  float pitch;
  float roll;
  float imu_dfr;
  float altitude;
  float pressure;


} Data_Struct;


#endif /* INC_AKU_STRUCTURE_H_ */
